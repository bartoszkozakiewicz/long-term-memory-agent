import logging
import time
from random import random

from pinecone_text.sparse import BM25Encoder
from pymilvus import DataType, MilvusClient, Collection, AnnSearchRequest, RRFRanker, connections
from embedding_generator import EmbeddingGenerator

logging.basicConfig(level=logging.INFO)


class MilvusStoreWithClient:
    def __init__(self, client_uri: str = "http://localhost:19530", csv_file_path: str = "data/products.csv"):
        self.client = MilvusClient(uri=client_uri)
        self.bm25 = BM25Encoder()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _prepare_schema():
        schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=1536)
        schema.add_field(field_name="sparse_vector",  datatype=DataType.SPARSE_FLOAT_VECTOR)
        return schema
    @staticmethod
    def _prepare_index():
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(field_name="embedding", index_type="AUTOINDEX", metric_type="L2")
        index_params.add_index(field_name="sparse_vector",index_name="sparse_inverted_index", index_type="SPARSE_INVERTED_INDEX", metric_type="IP", params={"drop_ratio_build": 0.2}) #Inner Product
        return index_params

    def bm25_encode(self, text):
        list_sparse = self.bm25.encode_documents(text)
        dict_sparse = dict(zip(list_sparse['indices'], list_sparse['values']))
        # print("dict sparse: ",dict_sparse)
        return dict_sparse
    

    def describe_collection(self, collection_name: str):
        return (self.client.describe_collection(collection_name),self.client.list_collections())
    
    def make_collection(self, collection_name: str):
        self.client.create_collection(
            collection_name=collection_name,
            schema=self._prepare_schema(),
            index_params=self._prepare_index(),
        )
        return


    def recreate_collection(self, collection_name: str):
        if self.client.has_collection(collection_name):
            logging.info(f"Dropping existing collection: {collection_name}")
            self.client.drop_collection(collection_name)
            while self.client.has_collection(collection_name):
                time.sleep(1)

        logging.info(f"Creating collection: {collection_name}")
        self.make_collection(collection_name)

    # def insert_data_from_csv(self, collection_name: str, hybrid:bool = False):
    #     prepared_data = self.csv_loader.prepare_data(hybrid=hybrid)
    #     self.logger.info(f"Inserting {len(prepared_data)} records into collection")
    #     self.client.insert(collection_name=collection_name, data=prepared_data)
    #     time.sleep(5000)
    #     return 


    def hybrid_search(self,        
        collection_name: str,
        query: list = None,
        fixed_filter: str = None,
        limit: int = 2,
        output_fields: list = None):

        connections.connect(alias="default")
        collection = Collection(name=collection_name)
        # collection.load()
        # print(len(EmbeddingGenerator().generate(query)))
        res = collection.hybrid_search(
            output_fields=["id", "price","cat_level_4", "cat_level_5", "url","specification","all_variants"],
            reqs=[
                AnnSearchRequest(
                    data=[EmbeddingGenerator().generate(query)], ## Dense vectors
                    anns_field="embedding", # Field name of the vectors
                    param={"metric_type": "L2"},
                    limit=limit,
                ),
                AnnSearchRequest(
                    data=[self.bm25_encode(query)], ## Sparse vector
                    anns_field="sparse_vector", # Field name of the vectors
                    param={"metric_type": "IP", "params": {"drop_ratio_search": 0.2,}},
                    limit=limit,
                )
            ],
            rerank=RRFRanker(),
            limit = limit
        )

        print("Odpowiedź hybrid search: ", res)
        return res


if __name__ == "__main__":
    # creating collection
    COLLECTION_NAME_HYBRID = "hybrid40_morele_pl"
    COLLECTION_NAME = "new_morele_pl"
    milvus_store = MilvusStoreWithClient(csv_file_path="data/products.csv")
    # use only when you want to create a new collection with the same name (data clearing)
    # milvus_store.recreate_collection(COLLECTION_NAME)
    # use otherwise
    # | for different websites it would be good idea to create a new collection for each website
    # milvus_store.make_collection(COLLECTION_NAME)
    # insert new data but be careful to no create too many duplicates
    # milvus_store.insert_data_from_csv(COLLECTION_NAME)


    #KLASYCZNA
    # milvus_store.make_collection(COLLECTION_NAME)
    # milvus_store.insert_data_from_csv(COLLECTION_NAME, hybrid=False)
    # searched_values = milvus_store.search(COLLECTION_NAME, query="szukam zabawek dla dziecka")
    # print( "searched values: ", searched_values)

    #HYBRYDA
    # milvus_store.make_collection(COLLECTION_NAME_HYBRID)   
    # milvus_store.insert_data_from_csv(COLLECTION_NAME_HYBRID, hybrid=True)
    searched_values = milvus_store.hybrid_search(COLLECTION_NAME_HYBRID, query="szukam zabawek dla dziecka")
    print( "searched values: ", searched_values)

    # print(milvus_store.describe_collection(COLLECTION_NAME_HYBRID))
