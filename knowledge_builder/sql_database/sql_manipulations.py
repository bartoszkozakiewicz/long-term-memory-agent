from connector import Connector
from typing import Optional

class SQLDatabase:


    @classmethod
    def _select_relationship_info(cls,person1_name:Optional[str]=None, person2_name:Optional[str]=None, type:Optional[str]=None):
        with Connector() as cursor:
            params = []
            query = """
            SELECT 
                p1.person_id AS person_1_id, 
                p1.first_name AS person_1_first_name, 
                p1.last_name AS person_1_last_name, 
                p2.person_id AS person_2_id, 
                p2.first_name AS person_2_first_name, 
                p2.last_name AS person_2_last_name, 
                r.relationship_id, 
                r.relationship_description, 
                r.relationship_type, 
                r.actual
            FROM 
                Person p1
            JOIN 
                Relationships r ON p1.person_id = r.person_id
            JOIN 
                Person p2 ON r.related_person_id = p2.person_id
            WHERE 
                p1.first_name = %s
            """

            params.append(person1_name)
            if person2_name:
                query += " AND p2.first_name = %s"
                params.append(person2_name)
            if type:
                query += " AND r.relationship_type = %s"
                params.append(type)  

            cursor.execute(query, tuple(params))
            result = cursor.fetchall()

        print("Relationship selected result", result)
        return result
    
    @classmethod
    def _select_basic_info(cls,
                        first_name:Optional[str]=None, 
                        last_name:Optional[str]=None, 
                        called:Optional[str]=None, 
                        gender:Optional[str]=None):
         
        with Connector() as cursor:
            params = []
            query = ("SELECT * FROM Person WHERE 1=1")#  first_name, last_name, called, description_about, date_of_birth, age, gender

            if first_name:
                query += " AND first_name = %s"
                params.append(first_name)
            if last_name:
                query += " AND last_name = %s"
                params.append(last_name)
            if called:
                query += " AND called = %s"
                params.append(called)
            if gender:
                query += " AND gender = %s"
                params.append(gender)

            cursor.execute(query, tuple(params))#
            result = cursor.fetchall()

        print("Person basic information result", result)
        return result


    @staticmethod
    def select_relationship_info(person1_name:Optional[str]=None, person2_name:Optional[str]=None, type:Optional[str]=None):
        result = SQLDatabase._select_relationship_info(person1_name, person2_name, type)
        return result
    
    @staticmethod
    def select_people_facts( 
                    first_name:Optional[str]=None, 
                    last_name:Optional[str]=None, 
                    called:Optional[str]=None, 
                    gender:Optional[str]=None,
                    category:Optional[str]=None):
        '''In the future category probably will be a list of categories, but for now it is a string.'''
        result = SQLDatabase._select_basic_info(first_name, last_name, called, gender)
        return result
    

    def update_data(self, table_name, update_values, condition):
            # Update usage example
            update_values = {
                'salary': 60000,
                'to_date': '2024-12-31'
            }
            condition = {
                'emp_no': 1,
                'from_date': '2020-01-01'
            }
            with Connector() as cursor:
                set_clause = ", ".join([f"{k} = %({k})s" for k in update_values.keys()])
                where_clause = " AND ".join([f"{k} = %({k})s" for k in condition.keys()])
                update_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

                # Combine the update_values and condition dictionaries for the parameters
                params = {**update_values, **condition}
                cursor.execute(update_query, params)

    @staticmethod
    def insert_data(table_name, data):
        with Connector() as cursor:
            add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

            data_salary = {
            'emp_no': "test",
            'salary': 50000,
            'from_date': "test",
            'to_date': "tetetest",
            }
            cursor.execute(add_salary, data_salary)


if __name__ =="__main__":
    db = SQLDatabase()
    db.select_people_facts(first_name="John")