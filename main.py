from friendLogic.graph.graph import talkGraph
from uuid import uuid4
from friendLogic.utils import print_event

def main(config: dict[str, dict[str, str]]):

    graph = talkGraph().builder()
    printed = set()

    q1 =  "Hello how are you today?"
    q2 =  "Do you know how old am I?"
    q3 =  "According to documents that I've sent, how many countries where listed in there?"
    q4 =  "According to documents that I've sent, how many countries where listed in there? Also find out my age."

    events = graph.stream({"messages":("user",q4)},config=config, stream_mode="values") # config=config,
    for event in events:
        print_event(event,printed)

if __name__ == "__main__":
    config = {
        "configurable":{
            "thread_id":str(uuid4())
        }
    }

    main(config)