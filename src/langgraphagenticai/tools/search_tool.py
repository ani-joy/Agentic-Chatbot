from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch

def get_tools():
    """
    Return the list to tools to be used in the chatbot
    """
    tools=[TavilySearch(k=2)]
    return tools

def create_tool_node (tools):
    """
    create aand return toolnode for the graph
    """
    return ToolNode(tools=tools)