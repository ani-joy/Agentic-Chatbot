import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json

# # class DisplayResultStreamlit:
# #     def __init__(self,usecase,graph,user_message):
# #         self.usecase=usecase
# #         self.graph=graph
# #         self.user_message=user_message

# #     def display_result_on_ui(self):
# #         usecase = self.usecase
# #         graph=self.graph
# #         user_message=self.user_message
# #         print(user_message)
# #         if not user_message:
# #             st.info("Please type a message to start the chat.")
# #             return
# #         if usecase=="Basic Chatbot":
# #             for event in graph.stream({'messages':("user",user_message)}):
# #                 print(event.values())
# #                 for value in event.values():
# #                     print(value['messages'])
# #                     with st.chat_message("user"):
# #                         st.write(user_message)
# #                     with st.chat_message("assistant"):
# #                         st.write(value["messages"].content)

# #         elif usecase=="chatbot with web":
# #             initial_state={"messages": [user_message]}
# #             # initial_state = {"messages": [HumanMessage(content=user_message)]}
# #             res=graph.invoke(initial_state)
# #             for message in res['messages']:
# #                 if type(message)==HumanMessage:
# #                     with st.chat_message("user"):
# #                         st.write(message.content)
# #                 elif type(message)==ToolMessage:
# #                     with st.chat_message("ai"):
# #                         st.chat_message("Tool call start")
# #                         st.write(message.content)
# #                         st.write("tool call end")
# #                 elif type(message)==AIMessage and message.content:
# #                     with st.chat_message("assistant"):
# #                         st.write(message.content)


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if not user_message:
            st.info("Please type a message to start the chat.")
            return

        # 🟦 Display user message
        with st.chat_message("user"):
            st.write(user_message)

        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages': ("user", user_message)}):
                for value in event.values():
                    messages = value.get("messages")
                    if isinstance(messages, list):
                        for msg in messages:
                            with st.chat_message("assistant"):
                                # Handle both dict and object cases
                                if hasattr(msg, "content"):
                                    st.write(msg.content)
                                else:
                                    st.write(str(msg))
                    else:
                        with st.chat_message("assistant"):
                            st.write(messages)

        elif usecase == "chatbot with web":
            initial_state = {"messages": [("user", user_message)]}
            res = graph.invoke(initial_state)

            for msg in res.get("messages", []):
                if isinstance(msg, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(msg.content)
                elif isinstance(msg, ToolMessage):
                    with st.chat_message("assistant"):
                        st.markdown("🛠️ **Tool Output:**")
                        st.write(msg.content)
                elif isinstance(msg, HumanMessage):
                    with st.chat_message("user"):
                        st.write(msg.content)
