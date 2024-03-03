import streamlit as st
# Assuming pc is previously imported and initialized as your model's API client
from predibase import PredibaseClient
from dotenv import load_dotenv
pc = PredibaseClient(token="pb_VA6FVAxdW4avyeA7SWUTSw")

# Initialize your fine-tuned model with the adapter
def get_ft_llm():
    llm = pc.LLM("pb://deployments/mistral-7b-instruct")
    adapter = pc.get_model('Krishi', 4)
    ft_llm = llm.with_adapter(adapter)
    return ft_llm

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Handle user input and generate responses using the fine-tuned model
def handle_userinput(user_question, ft_llm):
    result  = ft_llm.prompt(f"{user_question}.")
    response1  = result.response
    st.session_state.conversation_history.append((user_question,response1))

def display_conversation():
    for user_question, response in st.session_state.conversation_history:
        # User message
        st.markdown(f"<div class='message user'>{user_question}</div>", unsafe_allow_html=True)
        # Bot response
        st.markdown(f"<div class='message bot'>{response}</div>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Kissan ", page_icon=":books:") 
    st.title("Scheme Chatbot")
    st.header("Ask me anything about schemes")

    css = """
    <style>
        .message { padding: 10px; margin: 10px 0; border-radius: 10px; color: white; }
        .user { background-color: #000000; }
        .bot { background-color: #000000; }
        .stTextInput>div>div>input { margin-bottom: 20px; }
        .css-1siy2j7 { padding-top: 0!important; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    ft_llm = get_ft_llm()
    user_question = st.chat_input("Ask me anything")
    if user_question:
        handle_userinput(user_question, ft_llm)
        display_conversation()

if __name__ == '__main__':
    main()