import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import config

class LoadStreamlitUI:
    def __init__(self):
        self.config=config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=" "+self.config.get_page_title(),layout="wide")
        st.header(" "+ self.config.get_page_title())
        st.session_state.timeframe=''
        st.session_state.IsFetchButtonClicked=False


        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["Selected_llm"]=st.selectbox("Select LLM", llm_options)

            if self.user_controls["Selected_llm"]=="Groq":
                model_options=self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("API Key", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("pls enter a valid api key")

            if self.user_controls["Selected_llm"]=="OpenAI":
                model_options=self.config.get_openai_model_options()
                self.user_controls["selected_openai_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"]=st.text_input("API Key", type="password")

                if not self.user_controls["OPENAI_API_KEY"]:
                    st.warning("pls enter a valid api key")

            ##usecase selection
            self.user_controls["selected_usecase"]=st.selectbox("Selected_usecase",usecase_options)

            if self.user_controls["selected_usecase"]=="chatbot with web" or self.user_controls["selected_usecase"]=="AI News":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY_API_Key", type="password")


            if self.user_controls["selected_usecase"]=="AI News":
                st.subheader("AI NEWS Explorer")

                with st.sidebar:
                    time_frame= st.selectbox(
                        "Select Time frame",
                        ["Daily","Weekly","Monthly"],
                        index=0
                    )
                if st.button("fetch latest AI News",use_container_width=True):
                    st.session_state.IsFetchButtonClicked=True
                    st.session_state.timeframe=time_frame


            
        return self.user_controls


