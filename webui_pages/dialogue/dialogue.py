import streamlit as st
from webui_pages.utils import *
# 删除 streamlit-chatbox 导入
# from streamlit_chatbox import *
from streamlit_modal import Modal
from datetime import datetime
import os
import re
import time
from configs import (TEMPERATURE, HISTORY_LEN, PROMPT_TEMPLATES,
                     DEFAULT_KNOWLEDGE_BASE, DEFAULT_SEARCH_ENGINE, SUPPORT_AGENT_MODEL)
from server.knowledge_base.utils import LOADER_DICT
import uuid
from typing import List, Dict

# 添加自定义CSS，修改对话布局
def apply_custom_css():
    # 使用CSS进行基本样式设置
    st.markdown("""
    <style>
    /* 主聊天消息容器的通用设置 */
    div[data-testid="stChatMessage"] {
        display: flex !important;
        margin-bottom: 0.3rem !important;
        align-items: flex-start; /* 垂直方向顶部对齐 */
        gap: 0.5rem; /* 头像和内容的间距 */
    }

    /* --- AI 消息样式 --- */
    /* AI 消息内容：无气泡 */
    div[data-testid="stChatMessageContent"][aria-label="Chat message from assistant"] {
        background-color: transparent !important;
        padding: 0px !important;
    }

    /* --- 用户 消息样式 --- */
    /* 用户消息容器: 整体形成一个气泡，并推到右边 */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        flex-direction: row-reverse; /* 头像在右 */
        background-color: #F1F3F4 !important; /* 统一的浅灰色背景 */
        border-radius: 10px !important;
        padding: 0.5rem !important; /* 内边距，包裹头像和文本 */
    }

    /* 用户消息内容: 透明化，因为它已经在父容器的气泡里了 */
    div[data-testid="stChatMessageContent"][aria-label="Chat message from user"] {
        background-color: transparent !important;
        padding: 0 !important;
        text-align: right; /* 文本右对齐，靠近头像 */
    }

    /* --- 通用文本样式 --- */
    .stChatMessageContent p {
        margin-bottom: 0.3rem !important;
        line-height: 1.3 !important;
    }

    .stChatMessageContent {
        font-size: 0.95rem !important;
    }

    .stExpander {
        margin-top: 0.3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = uuid.uuid4().hex

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "默认对话"

# 替代chat_box的功能
def get_messages_history(history_len: int) -> List[Dict]:
    """
    获取历史对话记录
    """
    if history_len <= 0 or not st.session_state["messages"]:
        return []
    
    # 返回指定数量的历史消息，格式为[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    history = st.session_state["messages"][-history_len*2:] if history_len > 0 else st.session_state["messages"]
    
    # 删除debug历史记录
    # st.session_state["debug_history"] = history
    
    return history

def user_say(content: str):
    """
    添加用户消息到对话历史
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.session_state["messages"].append({"role": "user", "content": content})

def ai_say(content: str, docs: List[str] = None):
    """
    添加AI消息到对话历史
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if docs:
        full_content = content + "\n\n" + "\n\n".join(docs)
        st.session_state["messages"].append({"role": "assistant", "content": content, "docs": docs})
    else:
        st.session_state["messages"].append({"role": "assistant", "content": content})

def display_messages():
    """
    显示所有对话消息
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            with st.chat_message("user", avatar=os.path.join("img", "user.png")):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar=os.path.join("img", "ai.png")):
                # 使用write代替markdown，避免markdown格式化
                st.write(message["content"])
                # 如果有文档引用，则显示
                if "docs" in message and message["docs"]:
                    with st.expander("知识库匹配结果", expanded=False):
                        for doc in message["docs"]:
                            st.write(doc)

def clear_history():
    """
    清空对话历史
    """
    st.session_state["messages"] = []

@st.cache_data
def upload_temp_docs(files, _api: ApiRequest) -> str:
    return _api.upload_temp_docs(files).get("data", {}).get("id")

def parse_command(text: str, modal: Modal) -> bool:
    if m := re.match(r"/([^\s]+)\s*(.*)", text):
        cmd, name = m.groups()
        name = name.strip()
        
        if cmd == "help":
            modal.open()
        elif cmd == "new":
            if not name:
                i = 1
                while True:
                    name = f"会话{i}"
                    if name not in st.session_state.get("conversation_ids", {}):
                        break
                    i += 1
            
            if "conversation_ids" not in st.session_state:
                st.session_state["conversation_ids"] = {}
                
            if name in st.session_state["conversation_ids"]:
                st.error(f"该会话名称 '{name}' 已存在")
                time.sleep(1)
            else:
                st.session_state["conversation_ids"][name] = uuid.uuid4().hex
                st.session_state["current_chat"] = name
                st.session_state["messages"] = []
        elif cmd == "del":
            if "conversation_ids" not in st.session_state:
                st.session_state["conversation_ids"] = {}
                
            if name not in st.session_state["conversation_ids"] and not name:
                st.error(f"无效的会话名称：'{name}'")
                time.sleep(1)
            elif len(st.session_state["conversation_ids"]) <= 1:
                st.error("这是最后一个会话，无法删除")
                time.sleep(1)
            else:
                if name in st.session_state["conversation_ids"]:
                    st.session_state["conversation_ids"].pop(name, None)
                    if st.session_state.get("current_chat") == name:
                        st.session_state["current_chat"] = list(st.session_state["conversation_ids"].keys())[0]
        elif cmd == "clear":
            clear_history()
        return True
    return False

def dialogue_page(api: ApiRequest, is_lite: bool = False):
    # 应用自定义CSS，修改对话布局
    apply_custom_css()
    
    # 确保所有需要的session_state变量都已初始化
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    if "current_chat" not in st.session_state:
        st.session_state["current_chat"] = "默认对话"
    
    if "conversation_ids" not in st.session_state:
        st.session_state["conversation_ids"] = {}
    
    # 使用.get访问，避免访问不存在的键
    current_chat = st.session_state.get("current_chat", "默认对话")
    
    # 确保当前对话在conversation_ids中存在
    if current_chat not in st.session_state["conversation_ids"]:
        st.session_state["conversation_ids"][current_chat] = uuid.uuid4().hex
    
    conversation_id = st.session_state["conversation_ids"][current_chat]
    st.session_state.setdefault("file_chat_id", None)

    default_model = "shuzhiqihuang"
    st.session_state.setdefault("cur_llm_model", default_model)
    
    # 初始化selected_kb变量，确保它始终存在
    if "selected_kb" not in st.session_state:
        st.session_state["selected_kb"] = "zhenjiu"
    
    # 初始化selected_kb_name变量，确保它始终存在
    if "selected_kb_name" not in st.session_state:
        st.session_state["selected_kb_name"] = "针灸专家"

    # 欢迎消息
    # if len(st.session_state.get("messages", [])) == 0:
    #     st.toast(
    #         # f"欢迎使用 [`数智岐黄`](https://chattcm.ecnu.edu.cn/lingdan/) ! \n\n"
    #         # f"当前运行的模型`{default_model}`, 您可以开始提问了."
    #     )

    modal = Modal("自定义命令", key="cmd_help", max_width="500")
    if modal.is_open():
        with modal.container():
            cmds = [
                "/help - 显示帮助",
                "/new [名称] - 创建新对话",
                "/del [名称] - 删除对话",
                "/clear - 清空当前对话历史"
            ]
            st.write("\n\n".join(cmds))

    with st.sidebar:
        show_conversation_select_box = False

        if show_conversation_select_box:
            conv_names = list(st.session_state["conversation_ids"].keys())
            index = 0
            if current_chat in conv_names:
                index = conv_names.index(current_chat)
            conversation_name = st.selectbox("当前会话：", conv_names, index=index)
            st.session_state["current_chat"] = conversation_name
            conversation_id = st.session_state["conversation_ids"][conversation_name]

        dialogue_modes = ["智能问答", "领域专家问答"]
        selected_mode = st.radio("请选择对话模式：", dialogue_modes, index=0, key="dialogue_mode")

        index_prompt = {
            "智能问答": "llm_chat",
            "领域专家问答": "knowledge_base_chat",
        }

        temperature = 0.7
        history_len = 20  # 增加历史长度，从3改为20
        
        # 删除调试函数
        # def show_debug_info(info, title="Debug信息"):
        #     with st.expander(title, expanded=False):
        #         st.write(info)

        def on_kb_change():
            try:
                selected_kb = filtered_kb_list[kb_names.index(st.session_state.get("selected_kb_name", "针灸专家"))]
                st.session_state["selected_kb"] = selected_kb
                st.toast(f"已加载知识库： {kb_dict[selected_kb]}")
            except (ValueError, IndexError, KeyError) as e:
                st.error(f"选择知识库时出错: {str(e)}")

        if selected_mode == "领域专家问答":
            with st.expander("专家切换", True):
                kb_dict = {
                    "zhenjiu": "针灸专家",
                    "diquyuntong": "奥欣桐专家",
                    "hangtianyixue": "航天医学专家",
                    "laozi":"老子量子思维专家"
                }
                try:
                    kb_list = api.list_knowledge_bases()
                    filtered_kb_list = [kb for kb in kb_list if kb in kb_dict.keys()]
                    kb_names = [kb_dict[kb] for kb in filtered_kb_list]

                    index = 0
                    if "zhenjiu" in filtered_kb_list:
                        index = filtered_kb_list.index("zhenjiu")

                    selected_kb_name = st.selectbox(
                        "请选择领域专家：",
                        kb_names,
                        index=index,
                        on_change=on_kb_change,
                        key="selected_kb_name",
                    )

                    # 无论如何都更新selected_kb，确保它总是有效
                    try:
                        selected_kb = filtered_kb_list[kb_names.index(st.session_state.get("selected_kb_name", "针灸专家"))]
                        st.session_state["selected_kb"] = selected_kb
                    except (ValueError, IndexError):
                        # 如果出现任何错误，使用默认值
                        if filtered_kb_list:
                            st.session_state["selected_kb"] = filtered_kb_list[0]
                        else:
                            st.session_state["selected_kb"] = "zhenjiu"
                except Exception as e:
                    st.error(f"加载知识库列表失败: {str(e)}")
                    st.session_state["selected_kb"] = "zhenjiu"

    # 显示历史消息
    display_messages()

    chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter"

    # 删除调试信息显示
    # if "debug_history" in st.session_state:
    #     show_debug_info(f"历史记录数量: {len(st.session_state.debug_history)}\n历史记录: {st.session_state.debug_history}", "历史记录调试信息")

    if prompt := st.chat_input(chat_input_placeholder, key="prompt"):
        if parse_command(text=prompt, modal=modal):
            st.rerun()
        else:
            history = get_messages_history(history_len)
            # 添加用户消息
            user_say(prompt)
            
            # 显示用户消息
            with st.chat_message("user", avatar=os.path.join("img", "user.png")):
                st.markdown(prompt)
                
            try:
                if selected_mode == "智能问答":
                    if len(history) == 0:
                        first_prompt = "你是一个由华东师范大学联合上海中医药大学等多家科研单位共同研发的中西医融合医药问答大模型。你的名字是'数智岐黄-灵丹'，能够提供中医、西医及两者结合的专业医药咨询。" + prompt
                        # 调整第一次对话的提示
                        full_prompt = first_prompt
                    else:
                        full_prompt = prompt
                    
                    # 显示思考中的消息
                    with st.chat_message("assistant", avatar=os.path.join("img", "ai.png")):
                        thinking_placeholder = st.empty()
                        thinking_placeholder.markdown("正在思考...")
                    
                    text = ""
                    message_id = ""

                    # 确保使用的是session_state中的历史记录
                    r = api.chat_chat(full_prompt,
                                      history=history,
                                      conversation_id=conversation_id,
                                      model=default_model,
                                      temperature=temperature)
                    
                    # 接收流式回复
                    for t in r:
                        if error_msg := check_error_msg(t):
                            st.error(error_msg)
                            break
                        text += t.get("text", "")
                        # 使用write代替markdown展示正在生成的回答
                        thinking_placeholder.write(text)
                        message_id = t.get("message_id", "")

                    # 更新最终回复
                    thinking_placeholder.write(text)
                    
                    # 保存AI回复到历史记录
                    ai_say(text)
                    
                    # 删除反馈按钮（赞和踩）
                    # col1, col2 = st.columns([1, 10])
                    # with col1:
                    #     st.button("👍", key=f"thumbs_up_{message_id}")
                    # with col2:
                    #     st.button("👎", key=f"thumbs_down_{message_id}")

                elif selected_mode == "领域专家问答":
                    with st.chat_message("assistant", avatar=os.path.join("img", "ai.png")):
                        thinking_placeholder = st.empty()
                        
                        search_query = prompt
                        # 如果有历史对话，先进行问题改写
                        if history:
                            thinking_placeholder.markdown("正在分析问题，请稍候...")
                            
                            history_text = "\n".join([f'{m["role"]}: {m["content"]}' for m in history])
                            rephrase_prompt_template = (
                                '根据对话历史和后续问题，请将后续问题改写成一个独立的、无需参考对话历史就能理解的问题。请不要回答问题，只需改写。如果后续问题本身已经很清晰，则无需改写，直接返回原问题即可。\n\n'
                                '对话历史：\n'
                                '{history}\n\n'
                                '后续问题：{question}\n\n'
                                '独立问题：'
                            )
                            rephrase_prompt = rephrase_prompt_template.format(history=history_text, question=prompt)

                            rephrased_question = ""
                            # 使用低温进行改写，保证输出稳定性
                            response_iterator = api.chat_chat(rephrase_prompt, history=[], model=default_model, temperature=0.0)
                            
                            has_error = False
                            for chunk in response_iterator:
                                if error_msg := check_error_msg(chunk):
                                    st.error(error_msg)
                                    has_error = True
                                    break
                                rephrased_question += chunk.get("text", "")
                            
                            if not has_error:
                                search_query = rephrased_question.strip()

                        # 使用改写后的问题进行知识库查询
                        thinking_placeholder.write(f"正在查询知识库 `{st.session_state.get('selected_kb', 'zhenjiu')}` ...")
                        docs_placeholder = st.empty()

                        text = ""
                        docs = []
                        
                        for d in api.knowledge_base_chat(search_query,
                                                       knowledge_base_name=st.session_state.get("selected_kb", "zhenjiu"),
                                                       top_k=5,
                                                       history=history,
                                                       model=default_model,
                                                       temperature=temperature):
                            if error_msg := check_error_msg(d):
                                st.error(error_msg)
                            elif chunk := d.get("answer"):
                                text += chunk
                                thinking_placeholder.write(text)
                            elif doc_list := d.get("docs"):
                                docs = doc_list
                                with docs_placeholder.expander("知识库匹配结果", expanded=False):
                                    for doc in doc_list:
                                        st.write(doc)
                        
                        # 保存AI回复和文档到历史记录
                        ai_say(text, docs)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                thinking_placeholder.write("抱歉，处理您的请求时出现了错误。")
                ai_say("抱歉，处理您的请求时出现了错误。")

    now = datetime.now()
    with st.sidebar:
        cols = st.columns(2)
        
        # 导出聊天记录
        if cols[0].button("导出记录", use_container_width=True):
            chat_export = []
            for msg in st.session_state.get("messages", []):
                if msg["role"] == "user":
                    chat_export.append(f"## 用户\n{msg['content']}\n")
                else:
                    content = msg["content"]
                    if "docs" in msg and msg["docs"]:
                        content += "\n\n### 知识库匹配\n" + "\n\n".join(msg["docs"])
                    chat_export.append(f"## AI\n{content}\n")
            
            st.download_button(
                "下载MD文件",
                "".join(chat_export),
                file_name=f"{now:%Y-%m-%d %H.%M}_对话记录.md",
                mime="text/markdown",
            )
        
        # 清空对话
        if cols[1].button("清空对话", use_container_width=True):
            clear_history()
            st.rerun()

    with st.sidebar:
        disclaimer = '<div style="font-size: 10px; text-align: center; color: gray;">*本网站提供的服务内容和出现的信息（包括但不限于智能问答，方剂推荐、用药推荐等信息）均只作为参考，您须对任何自主决定的行为负责。</div>'
        st.write(disclaimer, unsafe_allow_html=True)

    st.sidebar.markdown(
"""
<!-- 在免责声明上方添加一些空白空间 -->
<div style="height: 10px;"></div>

<!-- 创建一个免责声明链接，点击跳转到具体的网页 -->
<div style="text-align: center;">
    <a href="https://chattcm.ecnu.edu.cn/demo#/admin/disclaimer" target="_blank" style="text-decoration: none; color: gray;">免责声明</a>
</div>
""",
unsafe_allow_html=True
)