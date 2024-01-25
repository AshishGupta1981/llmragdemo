import streamlit as st
from langchain.schema import(SystemMessage, HumanMessage, AIMessage)
from llm import query

def init_page() -> None:
  st.set_page_config(
    page_title="History Chatbot"
  )
  st.header("History Chatbot")
  st.sidebar.title("Options")

def init_messages() -> None:
  clear_button = st.sidebar.button("Clear Conversation", key="clear")
  if clear_button or "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages = [
      SystemMessage(
        content="""You are a helpful AI assistant. Reply your answer in based on following information.
        
        Busting the myths and misconceptions about electric vehicles. New petrol and diesel only cars will no longer be sold in the UK from 2035, and the US is aiming for half of all new vehicle sales to be electric by 2030. So, before long, its likely that far more of us will be behind the wheel of an electric vehicle (EV).There are a number of questions and concerns people have about EVs, and just as many misconceptions that are making motorists think twice. Here we address some of the most common EV myths.
        
        National Grid EV van seen from behind in a field with electricity pylons and a wind turbine in the background.
        Myth 1: The electricity grid won’t be able to handle the increase in EVs
        There are two aspects to whether the electricity grid can manage lots of EVs being plugged in at once:Will there be enough electricity be available to charge EVs?
 
        Do the electricity grid's wires have enough capacity for charging EVs?
        It’s important to remember that this is a managed transition; the shift to EVs is happening gradually – not overnight. In England and Wales we’re connecting more and more renewable energy sources to the grid to supply us with clean electricity; for example, the growth in offshore wind farms means that wind power will adequately meet the future demand for electrifying transport, and we’re constantly upgrading our electricity networks to be better equipped to carry this cleaner power.
        """
      )
    ]

def get_answer(prompt) -> str:
  return query(prompt)

def get_current_prompt()-> None:
    prompt = ""
    messages = st.session_state.get("messages", [])
    for message in messages: 
        if isinstance(message, SystemMessage):
            prompt += message.content
            prompt += "\n"
        elif isinstance(message, AIMessage):
            prompt += "Answer :" +message.content
            prompt += "\n"
        elif isinstance(message, HumanMessage):
            prompt += "Question :" +message.content
            prompt += "\n"
    return prompt

def main() -> None:
  init_page()
  init_messages()

  if user_input := st.chat_input("Input your history question!"):
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.spinner("Bot is typing ..."):
      updated_prompt = get_current_prompt()
      answer = get_answer(updated_prompt)
      print(answer)
    st.session_state.messages.append(AIMessage(content=answer))

    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
             with st.chat_message("user"):
                st.markdown(message.content)

if __name__ == "__main__":
  main()