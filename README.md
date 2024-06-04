### Prerequisites

- Python 3.10 or later.
- Milvus
  - Milvus server running (refer to the [Milvus installation guide](https://milvus.io/docs/v2.0.x/install_standalone-docker.md) - I've used docker-compose).
  - Attu GUI for milvus (refer to the [Attu installation](https://github.com/zilliztech/attu/releases/tag/v2.3.8))

### Environment process

1. **Requirements**

   - `pip install -r requirements.txt`
   - `pip install .` (In folder with setup to install project package)

2. **Starting milvus vectorstore**
   - `docker-compose -f milvus-compose.yml up -d` (In folder with compose which is - vectorstore)
   - To see vectorstores in GUI start attu desktop app with Milvus address: 127.0.0.1:19530

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

3. **Creating a Milvus Collection**

   - To create a new Milvus collection for storing embeddings, use the `make_collection` method from the `MilvusStoreWithClient` class.

   - **Important**: If you need to recreate the collection (e.g., to clear existing data during development), use the `recreate_collection` method instead.

4. **Inserting Data into Milvus**

   After creating a collection, you can insert the prepared data from your CSV file using the `insert_data_from_csv` method. This method will read your CSV file, generate embeddings for each row, and insert them into your Milvus collection.

5. **Searching in Milvus**

   Use the `search` method to perform similarity searches within your collection. You can specify the search parameters according to your requirements (e.g., limiting the number of results or specifying a filter).
