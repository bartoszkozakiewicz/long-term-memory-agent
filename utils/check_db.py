import json
import sqlite3
from tokens_counter import count_tokens


class CheckpointerController:
    def __init__(self, path="../checkpoints.sqlite"):
        self.path = path
        self.conn = sqlite3.connect(self.path)

    def __enter__(self):
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_type == Exception:
            raise Exception("Exception occured: ", exc_val)


def check_db():
    with CheckpointerController() as cursor:
        cursor.execute("SELECT checkpoint FROM checkpoints ORDER BY thread_ts DESC LIMIT 1")
        last_row = cursor.fetchone()

        data_str = last_row[0].decode('utf-8')
        parsed_json = json.loads(data_str)

        messages = parsed_json["channel_values"]["messages"]
        friends_family = parsed_json["channel_values"]["friends_family"]
        weekly_events = parsed_json["channel_values"]["weekly_events"]  

        try:
            basic_info = parsed_json["channel_values"]["basic_user_info"]  
        except KeyError:
            print("No basic user info found")
            basic_info = None

        num_of_messages = len(messages)

        print("Messages: ",num_of_messages)
        print("Friends and Family: ",friends_family)
        print("Weekly events: ",weekly_events)
        print("Basic user info: ",basic_info)

        num_of_tokens_used = [{"message_num":idx+1, 
                               "total_tokens":mess["kwargs"]["response_metadata"]["token_usage"]["total_tokens"]} 
                               for idx, mess in enumerate(messages) if mess["id"][-1] == "AIMessage"] 
        
        print("Num of tokens used per steps: ",num_of_tokens_used)
        print("All tokens: ",sum([mess["total_tokens"] for mess in num_of_tokens_used]))

        print("Messages 1: ",messages[0], "X: ", count_tokens(str(parsed_json["channel_values"]["messages"][0])), "\n\n")
        # print("Messages 2 : ",parsed_json["channel_values"]["messages"][1])
        # print("Message 1 - type : ",parsed_json["channel_values"]["messages"][1]["id"][-1], "\n\n")
        # print("Message 3 ",parsed_json["channel_values"]["messages"][2], "\n\n")


check_db()

