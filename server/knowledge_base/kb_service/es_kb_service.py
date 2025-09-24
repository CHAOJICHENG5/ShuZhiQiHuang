from typing import List
import os
import shutil
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from elasticsearch_dsl import Search
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from configs import KB_ROOT_PATH, EMBEDDING_MODEL, EMBEDDING_DEVICE, CACHED_VS_NUM
from server.knowledge_base.kb_service.base import KBService, SupportedVSType
from server.utils import load_local_embeddings
from elasticsearch import Elasticsearch,BadRequestError
from configs import logger
from configs import kbs_config

class ESKBService(KBService):

    def do_init(self):
        self.kb_path = self.get_kb_path(self.kb_name)
        self.index_name = self.kb_path.split("/")[-1]
        self.IP = kbs_config[self.vs_type()]['host']
        self.PORT = kbs_config[self.vs_type()]['port']
        self.user = kbs_config[self.vs_type()].get("user",'')
        self.password = kbs_config[self.vs_type()].get("password",'')
        self.dims_length = kbs_config[self.vs_type()].get("dims_length",None)
        self.embeddings_model = load_local_embeddings(self.embed_model, EMBEDDING_DEVICE)
        
        # 初始化ES客户端
        try:
            if self.user and self.password:
                self.es_client_python = Elasticsearch(
                    f"http://{self.IP}:{self.PORT}",
                    basic_auth=(self.user, self.password),
                    verify_certs=False,
                    timeout=30,
                    max_retries=3,
                    retry_on_timeout=True
                )
            else:
                raise ValueError("ES必须配置用户名和密码")
            
            # 检查连接
            if not self.es_client_python.ping():
                raise ConnectionError("无法连接到Elasticsearch")
            
            # 检查索引是否存在
            if not self.es_client_python.indices.exists(index=self.index_name):
                try:
                    # 创建索引
                    self.es_client_python.indices.create(
                        index=self.index_name,
                        ignore=400  # 忽略已存在的错误
                    )
                except Exception as e:
                    logger.error(f"创建索引失败: {str(e)}")
                    raise
                
            # 初始化 langchain ES store
            self.db_init = ElasticsearchStore(
                es_url=f"http://{self.IP}:{self.PORT}",
                index_name=self.index_name,
                query_field="context",
                vector_query_field="dense_vector",
                embedding=self.embeddings_model,
                es_user=self.user,
                es_password=self.password
            )
            
        except Exception as e:
            logger.error(f"Elasticsearch 初始化失败: {str(e)}")
            raise

    @staticmethod
    def get_kb_path(knowledge_base_name: str):
        return os.path.join(KB_ROOT_PATH, knowledge_base_name)

    @staticmethod
    def get_vs_path(knowledge_base_name: str):
        return os.path.join(ESKBService.get_kb_path(knowledge_base_name), "vector_store")

    def do_create_kb(self):
        if os.path.exists(self.doc_path):
            if not os.path.exists(os.path.join(self.kb_path, "vector_store")):
                os.makedirs(os.path.join(self.kb_path, "vector_store"))
            else:
                logger.warning("directory `vector_store` already exists.")

    def vs_type(self) -> str:
        return SupportedVSType.ES

    def _load_es(self, docs, embed_model):
        # 将docs写入到ES中
        try:
            # 连接 + 同时写入文档
            if self.user != "" and self.password != "":
                self.db = ElasticsearchStore.from_documents(
                        documents=docs,
                        embedding=embed_model,
                        es_url= f"http://{self.IP}:{self.PORT}",
                        index_name=self.index_name,
                        distance_strategy="COSINE",
                        query_field="context",
                        vector_query_field="dense_vector",
                        verify_certs=False,
                        es_user=self.user,
                        es_password=self.password
                    )
            else:
                self.db = ElasticsearchStore.from_documents(
                        documents=docs,
                        embedding=embed_model,
                        es_url= f"http://{self.IP}:{self.PORT}",
                        index_name=self.index_name,
                        distance_strategy="COSINE",
                        query_field="context",
                        vector_query_field="dense_vector",
                        verify_certs=False)
        except ConnectionError as ce:
            print(ce)
            print("连接到 Elasticsearch 失败！")
            logger.error("连接到 Elasticsearch 失败！")
        except Exception as e:
            logger.error(f"Error 发生 : {e}")
            print(e)
    # #原始融合方法，vector和bm25各取分数前三名，然后拼接在一起，vector的结果拼接在bm25的前面
    # def do_search(self, query: str, top_k: int, score_threshold: float):
    #     """结合 BM25 和向量相似性进行文本搜索"""
    #     # 执行向量相似性搜索
    #     vector_search_results = self.db_init.similarity_search_with_score(query=query, k=3)

    #     vector_docs = []
    #     for doc, score in vector_search_results:
    #         doc_id = doc.metadata.get("id", None)
    #         vector_docs.append((doc, score, doc_id, "vector"))

    #     # 执行 BM25 搜索
    #     bm25_search = Search(using=self.es_client_python, index=self.index_name).query("match", context=query)
    #     bm25_search = bm25_search[0:3]  # 控制返回结果的数量为前 3 个
    #     bm25_response = bm25_search.execute()

    #     bm25_docs = []
    #     for hit in bm25_response.hits.hits:
    #         document_dict = hit["_source"].to_dict()  # Convert AttrDict to a regular dict
    #         score = hit["_score"]
    #         doc_id = hit["_id"]
    #         metadata = document_dict.get("metadata", {})
    #         document = Document(page_content=document_dict.get("context"), metadata=metadata)
    #         bm25_docs.append((document, score, doc_id, "bm25"))

    #     # 按 BM25 得分排序
    #     bm25_docs = sorted(bm25_docs, key=lambda x: x[1], reverse=True)

    #     # 合并结果，将向量相似性结果放在前面，BM25 结果接在后面
    #     docs = vector_docs + bm25_docs

    #     # 过滤出加权分数大于阈值的结果
    #     # filtered_docs = [doc for doc in docs if doc[1] > score_threshold]

    #     # 输出调试信息，查看各自的检索分数
    #     for doc in docs:  # 想进行阈值筛选的话将 docs 改为 filtered_docs
    #         print(f"Source: {doc[3]}, Score: {doc[1]}, ID: {doc[2]}")

    #     # 返回前 top_k 个结果
    #     return docs[:top_k]
    
    
    ##交替排列
    def do_search(self, query: str, top_k: int, score_threshold: float):
        """结合 BM25 和向量相似性进行文本搜索"""
        # 执行向量相似性搜索
        vector_search_results = self.db_init.similarity_search_with_score(query=query, k=3)

        vector_docs = []
        for doc, score in vector_search_results:
            doc_id = doc.metadata.get("id", None)
            vector_docs.append((doc, score, doc_id, "vector"))

        # 执行 BM25 搜索
        bm25_search = Search(using=self.es_client_python, index=self.index_name).query("match", context=query)
        bm25_search = bm25_search[0:3]  # 控制返回结果的数量为前 3 个
        bm25_response = bm25_search.execute()

        bm25_docs = []
        for hit in bm25_response.hits.hits:
            document_dict = hit["_source"].to_dict()  # Convert AttrDict to a regular dict
            score = hit["_score"]
            doc_id = hit["_id"]
            metadata = document_dict.get("metadata", {})
            document = Document(page_content=document_dict.get("context"), metadata=metadata)
            bm25_docs.append((document, score, doc_id, "bm25"))

        # 按 BM25 得分排序
        bm25_docs = sorted(bm25_docs, key=lambda x: x[1], reverse=True)

        # 交替合并向量相似性结果和 BM25 结果
        merged_docs = []
        max_length = max(len(vector_docs), len(bm25_docs))
        for i in range(max_length):
            if i < len(vector_docs):
                merged_docs.append(vector_docs[i])
            if i < len(bm25_docs):
                merged_docs.append(bm25_docs[i])

        # 过滤出加权分数大于阈值的结果
        # filtered_docs = [doc for doc in merged_docs if doc[1] > score_threshold]

        # 输出调试信息，查看各自的检索分数
        for doc in merged_docs:  # 想进行阈值筛选的话将 merged_docs 改为 filtered_docs
            print(f"Source: {doc[3]}, Score: {doc[1]}, ID: {doc[2]}")

        # 返回前 top_k 个结果
        return merged_docs[:top_k]
        

    def del_doc_by_ids(self, ids: List[str]) -> bool:
        for doc_id in ids:
            try:
                self.es_client_python.delete(index=self.index_name,
                                            id=doc_id,
                                            refresh=True)
            except Exception as e:
                logger.error(f"ES Docs Delete Error! {e}")

    def do_delete_doc(self, kb_file, **kwargs):
        if self.es_client_python.indices.exists(index=self.index_name):
            # 从向量数据库中删除索引(文档名称是Keyword)
            query = {
                "query": {
                    "term": {
                        "metadata.source.keyword": kb_file.filepath
                    }
                }
            }
            # 注意设置size，默认返回10个。
            search_results = self.es_client_python.search(body=query, size=50)
            delete_list = [hit["_id"] for hit in search_results['hits']['hits']]
            if len(delete_list) == 0:
                return None
            else:
                for doc_id in delete_list:
                    try:
                        self.es_client_python.delete(index=self.index_name,
                                                     id=doc_id,
                                                     refresh=True)
                    except Exception as e:
                        logger.error(f"ES Docs Delete Error! {e}")

            # self.db_init.delete(ids=delete_list)
            #self.es_client_python.indices.refresh(index=self.index_name)


    def do_add_doc(self, docs: List[Document], **kwargs):
        '''向知识库添加文件'''
        print(f"server.knowledge_base.kb_service.es_kb_service.do_add_doc 输入的docs参数长度为:{len(docs)}")
        print("*"*100)
        self._load_es(docs=docs, embed_model=self.embeddings_model)
        # 获取 id 和 source , 格式：[{"id": str, "metadata": dict}, ...]
        print("写入数据成功.")
        print("*"*100)
        
        if self.es_client_python.indices.exists(index=self.index_name):
            file_path = docs[0].metadata.get("source")
            query = {
                "query": {
                    "term": {
                        "metadata.source.keyword": file_path
                    }
                }
            }
            search_results = self.es_client_python.search(body=query)
            if len(search_results["hits"]["hits"]) == 0:
                raise ValueError("召回元素个数为0")
        info_docs = [{"id":hit["_id"], "metadata": hit["_source"]["metadata"]} for hit in search_results["hits"]["hits"]]
        return info_docs




    def do_clear_vs(self):
        """从知识库删除全部向量"""
        if self.es_client_python.indices.exists(index=self.kb_name):
            self.es_client_python.indices.delete(index=self.kb_name)


    def do_drop_kb(self):
        """删除知识库"""
        # self.kb_file: 知识库路径
        if os.path.exists(self.kb_path):
            shutil.rmtree(self.kb_path)


