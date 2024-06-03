### Prerequisites

- Python 3.10 or later.

  - Requirements libraries installed (`pip install -r requirements.txt`).

- Milvus
  - Milvus server running (refer to the [Milvus installation guide](https://milvus.io/docs/v2.0.x/install_standalone-docker.md) - I've used docker-compose).
  - Attu GUI for milvus (refer to the [Attu installation](https://github.com/zilliztech/attu/releases/tag/v2.3.8))

### Environment process

1. **Requirements**
   - 'pip install -r requirements.txt'
   - 'pip install .' (In folder with setup to install project package)

### Overview

This system uses Milvus, a highly scalable, distributed vector database, to store and search through vector embeddings of textual data. It's particularly useful for applications like similarity search, recommendation systems, and more. The system reads data from a CSV file, generates vector embeddings for textual data, and then inserts these embeddings into a Milvus collection for efficient similarity searches.

### Components

1. **MilvusStoreWithClient**: This class manages the Milvus database operations, including creating collections, inserting data, and searching through the collections.

2. **EmbeddingGenerator**: A placeholder for generating vector embeddings from text. Currently, it generates random embeddings but is intended to be replaced with a model-based generator (e.g., using OpenAI's Ada for generating embeddings).

### Setup and Usage

1. **Preparing the Environment**

   Ensure Milvus is running and accessible. Install all required Python libraries mentioned in the prerequisites.

2. **Loading and Preparing Data**

   Place your data file in the `data` directory and ensure it's in CSV format. The data file should have a column for textual data that you want to generate embeddings for (e.g., product descriptions).

3. **Generating Embeddings**

   - The provided `EmbeddingGenerator` class currently generates random embeddings. To make this system production-ready, you should implement an actual embedding generation process, such as using a pre-trained model from OpenAI.

   - **TODO**: Implement a model-based embedding generator, such as OpenAI's Ada, to replace the `EmbeddingGenerator`'s `generate` method. This will significantly improve the quality of search results.

4. **Creating a Milvus Collection**

   - To create a new Milvus collection for storing embeddings, use the `make_collection` method from the `MilvusStoreWithClient` class.

   - **Important**: If you need to recreate the collection (e.g., to clear existing data during development), use the `recreate_collection` method instead.

5. **Inserting Data into Milvus**

   After creating a collection, you can insert the prepared data from your CSV file using the `insert_data_from_csv` method. This method will read your CSV file, generate embeddings for each row, and insert them into your Milvus collection.

6. **Searching in Milvus**

   Use the `search` method to perform similarity searches within your collection. You can specify the search parameters according to your requirements (e.g., limiting the number of results or specifying a filter).

### Example Usage

```python
COLLECTION_NAME = "your_collection_name"
csv_file_path = "data/your_data_file.csv"

# Initialize the Milvus store with the path to your CSV data file
milvus_store = MilvusStoreWithClient(csv_file_path=csv_file_path)

# Optionally, recreate the collection to clear existing data
milvus_store.recreate_collection(COLLECTION_NAME)

# Create the collection if it doesn't exist
milvus_store.make_collection(COLLECTION_NAME)

# Insert data from the CSV file into the Milvus collection
milvus_store.insert_data_from_csv(COLLECTION_NAME)

# Perform a search (customize this part as needed)
results = milvus_store.search(COLLECTION_NAME)
print(results)
```
