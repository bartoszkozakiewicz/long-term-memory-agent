from friendLogic.graph.graph import talkGraph
from uuid import uuid4

def main(config: dict[str, dict[str, str]]):

    graph = talkGraph().builder()
    print("Graph built")

    q1 =  "Hello how are you today?"
    q2 =  "Do you know how old am I?"
    q3 =  "According to documents that I've sent, how many countries where listed in there?"
    q4 =  "According to documents that I've sent, how many countries where listed in there? Also find out my age."

    events = graph.stream({"messages":("user",q4)},config=config, stream_mode="values") # config=config,
    for event in events:
        print("Event Occured: \n", event)

if __name__ == "__main__":
    config = {
        "configurable":{
            "thread_id":str(uuid4())
        }
    }

    main(config)