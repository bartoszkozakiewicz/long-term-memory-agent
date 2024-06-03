import logging
import time
from random import random

from embedding_generator import EmbeddingGenerator
from pymilvus import DataType, MilvusClient, Collection, AnnSearchRequest, RRFRanker, connections

logging.basicConfig(level=logging.INFO)


class MilvusStoreWithClient:
    def __init__(self, client_uri: str = "http://localhost:19530",):
        self.client = MilvusClient(uri=client_uri)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _prepare_schema():
        schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=1536)
        return schema
    @staticmethod
    def _prepare_index():
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(field_name="embedding", index_type="AUTOINDEX", metric_type="L2")
        return index_params
    
    def make_collection(self, collection_name: str):
        self.client.create_collection(
            collection_name=collection_name,
            schema=self._prepare_schema(),
            index_params=self._prepare_index(),
        )

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
        for row in data:
                for column in row:
                    if column == "content":
                        row["embedding"] = EmbeddingGenerator().generate(row[column])
                        break

        self.logger.info(f"Inserting {len(data)} records into collection")
        self.client.insert(collection_name=collection_name, data=data)
        return 

    def search(
        self,
        collection_name: str,
        query: list = None,
        fixed_filter: str = None,
        limit: int = 100,
        output_fields: list = None,
        search_params: dict = None,
    ):
        
        assert collection_name is not None, "Collection name must be provided"
        assert query is not None, "Query must be provided"
        data = EmbeddingGenerator().generate(query)

        if output_fields is None:
            output_fields=["id", "content", "person", "category", "creation_date"]

        
        return self.client.search(
            collection_name=collection_name,
            data=[data],
            filter=fixed_filter,
            limit=limit,
            output_fields=output_fields,
            # search_params=search_params,
        )


if __name__ == "__main__":
    # creating collection
    COLLECTION_NAME = "classic_test"
    milvus_store = MilvusStoreWithClient()

    datax = [{"content": "I love pizza", "person": "John", "category": "food", "creation_date": "2024-06-01"},]
    datax2 = [{"content": "I was on Podsiadło concert", "person": "John", "category": "event", "creation_date": "2024-06-01"},]
    # milvus_store.create_vs_with_testdata(collection_name=COLLECTION_NAME,data=datax+datax2)

    # searched_values = milvus_store.search(COLLECTION_NAME, query="pizza")

    searched_values = milvus_store.search(COLLECTION_NAME, query="los", fixed_filter="category == 'event'")
    print( "searched values: ", searched_values)
