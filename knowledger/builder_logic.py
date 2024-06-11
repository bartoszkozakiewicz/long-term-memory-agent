from knowledger.sql_database.sql_manipulations import SQLDatabase

class BuilderKnowledgeLogic:

    @staticmethod
    def update_sql_database(table_name, update_values, condition):
        SQLDatabase.update_data(table_name, update_values, condition)
        return
    
    @staticmethod
    def insert_sql_database(table_name, data):
        SQLDatabase.insert_data(table_name, data)
        return
    
    @staticmethod
    def insert_vs_database(collection_name, data):
        #TODO: Implement this method
        return