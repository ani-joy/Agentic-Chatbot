import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.LLMS.openaillm import OpenAILLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit 

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
    
    if st.session_state.IsFetchButtonClicked:
        user_message=st.session_state.timeframe
    else:
        user_message= st.chat_input("enter yoour message")
    

    try:
            selected_provider=user_input.get("Selected_llm")
            # obj_llm_config=GroqLLM(user_controls_input=user_input)
            # obj_llm_config=OpenAILLM(user_controls_input=user_input)
            # model=obj_llm_config.get_llm_model()
        # obj_llm_config_openai=OpenAILLM(user_controls_input=user_input)
            if selected_provider == "Groq":
                obj_llm_config = GroqLLM(user_controls_input=user_input)
            elif selected_provider == "OpenAI":
                obj_llm_config = OpenAILLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return


            # if not model:
            #     st.error("Error:LLM model could not be initialized")
            #     return 
            usecase=user_input.get("selected_usecase")
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                print(user_message)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: Graph set up failed- {e}")
                return
        
    except Exception as e:
        st.error(f"Error: Graph set up failed- {e}")
        return