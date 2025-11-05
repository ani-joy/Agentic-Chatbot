import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI

def load_langgrapg_agenticai_app():
    """
    loads and runs the agentic ai appliciation with streamlit ui.
    this function initializs te ui, handels user inputs ,configure llm models,
    sets up the graph based on  the selected usecase, and displayes the uotput while
    implementing exception handling for robustness

    """

    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("error:failed to load user input from ui")
        return 
    
    user_message= st.chat_input("enter yoour message")