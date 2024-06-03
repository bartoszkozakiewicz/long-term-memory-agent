import logging
import time
from random import random

from pinecone_text.sparse import BM25Encoder
from pymilvus import DataType, MilvusClient, Collection, AnnSearchRequest, RRFRanker, connections
from embedding_generator import EmbeddingGenerator

logging.basicConfig(level=logging.INFO)


class MilvusStoreWithClient:
    def __init__(self, client_uri: str = "http://localhost:19530"):
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
        print("dict sparse: ",dict_sparse)
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


    def create_vs_with_testdata(self, collection_name: str, data: list[dict]):
        self.make_collection(collection_name)
        print("Collection created")
        self.insert_data(collection_name, data)
        print("Data inserted")
        return 

    def insert_data(self, collection_name: str, data: list[dict]):
        '''
        prepared_data: list of dictionaries with keys corresponding to the fields in the collection

        fields: id, content, person, category, creation_date...
        '''
        #For testing purposes...
        self.bm25.fit([ele["content"] for ele in data])
        for row in data:
            for column in row:
                if column == "content":
                    row["embedding"] = EmbeddingGenerator().generate(row[column])
                    row["sparse_vector"] = self.bm25_encode(row[column])
                    break

        self.logger.info(f"Inserting {len(data)} records into collection")
        self.client.insert(collection_name=collection_name, data=data)
        return 

    
    def hybrid_search(self,        
        collection_name: str,
        query: list = None,
        fixed_filter: str = None,
        limit: int = 2,
        output_fields: list = None):
        self.bm25.fit([query])

        connections.connect(alias="default")
        collection = Collection(name=collection_name)

        if output_fields is None:
            output_fields=["id", "content", "person", "category", "creation_date"]
        # collection.load()
        res = collection.hybrid_search(
            filter =fixed_filter,
            output_fields=output_fields,
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
    milvus_store = MilvusStoreWithClient()
    # use only when you want to create a new collection with the same name (data clearing)
    # milvus_store.recreate_collection(COLLECTION_NAME)

    #KLASYCZNA
    # milvus_store.make_collection(COLLECTION_NAME)
    # print( "searched values: ", searched_values)


    # ---- TUTAJ BYŁO
    # searched_values = milvus_store.hybrid_search(COLLECTION_NAME_HYBRID, query="szukam zabawek dla dziecka")
    # print( "searched values: ", searched_values)

    # ---------------- TESTING

    # print(milvus_store.describe_collection("test"))
    datax = [{"content": "I love pizza", "person": "John", "category": "food", "creation_date": "2024-06-01"},]
    datax2 = [{"content": "I was on Podsiadło concert", "person": "John", "category": "event", "creation_date": "2024-06-01"},]
    # milvus_store.create_vs_with_testdata(collection_name="test",data=datax)
    # milvus_store.insert_data(collection_name="test",data=datax2)


    milvus_store.hybrid_search("test", query="los", fixed_filter="category == 'event'")