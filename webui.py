import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages.dialogue.dialogue import dialogue_page
from webui_pages.knowledge_base.knowledge_base import knowledge_base_page
import os
import sys
from configs import VERSION
from server.utils import api_address


api = ApiRequest(base_url=api_address())

if __name__ == "__main__":
    is_lite = "lite" in sys.argv

    st.set_page_config(
        "灵丹",
        os.path.join("img", "shuzhilogo-ball.jpg"),
        initial_sidebar_state="auto",
        layout="wide",
        menu_items={
            'About': f"""欢迎使用 数智岐黄医药大语言模型 V2.0.0！"""
        }
    )
    
    # 确保会话状态不被重置
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []
    
    if 'chat_initialized' not in st.session_state:
        st.session_state['chat_initialized'] = False
        # 在第一次加载时初始化聊天
        st.session_state['chat_initialized'] = True

    pages = {
        "灵丹 (ChatTCM)": {
            "icon": "chat",
            "func": dialogue_page,
        },
        # "知识库管理": {
        #     "icon": "hdd-stack",
        #     "func": knowledge_base_page,
        # },
    }


    ##添加返回按钮
    with st.sidebar:
        st.sidebar.markdown(
        """
        <!-- 假设我们要设计一个与上面界面风格匹配的超链接 -->
<a href="https://chattcm.ecnu.edu.cn/" target="_self" style="color: #ffffff; background-color: #165DFF; padding: 5px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin: 0px 0;position: relative; top: -85px;font-size:15px">返回</a >
        """,
        unsafe_allow_html=True
    )

        st.image(
            os.path.join(
                "img",
                "shuzhilogo-3.png"
            ),
            width=None
        )
        st.caption(
            f"""<p align="right">当前版本：V.1.0.0</p>""",
            unsafe_allow_html=True,
        )
        options = list(pages)
        icons = [x["icon"] for x in pages.values()]

        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,
        )

    # if selected_page in pages:
    #     pages[selected_page]["func"](api=api, is_lite=is_lite)
    dialogue_page(api = api,is_lite=is_lite)