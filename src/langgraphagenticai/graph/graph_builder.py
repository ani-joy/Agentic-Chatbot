from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END
from src.langgraphagenticai.nodes.basic_chat_bot_node import BasicChatBotNode


class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chtabot graph using langgraph.
        this method initializes a chatbot node using the 'BasicChatBotNode' class
        and integrates it into the graph. The Chatbot node is set as bothe entry and exit point of the graph
        """
        self.basic_chatbot_node=BasicChatBotNode(self.llm)


        self.graph_builder.add_node("Chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"Chatbot")
        self.graph_builder.add_edge("Chatbot",END)

    def setup_graph(self,usecase: str):
        """
        Sets up the graph for the selected use case
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        return self.graph_builder.compile()