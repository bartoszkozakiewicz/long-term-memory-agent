from langchain_core.prompts import ChatPromptTemplate

facts_keys_retriever_prompts = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a tool that is responsible for retrieving things that are potentially needed to search about user's life, facts about him and his friends."            "You are given a message from the user and need to retrieve all relevant information mentioned in this message."
            "Your task is to list all potential facts that can be researched further based on the message content."
            "For example, if the user mentions a friend, you should friend name and some relevant informations that where in that message that can be looked up."
            # "Example of message: 'I was with my friend John yesterday, we were talking about his new job.'"
            # "Output: ['John', 'John's new job']"
            " You have to output information in given format: {format_instructions}"
            "Message: {message}"
            "Output: "
        )
    ]
)