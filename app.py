import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Page settings
st.set_page_config(
    page_title="AbbasBot AI",
    page_icon="🤖"
)

# RizviBot AI heading
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <h1 style="margin-bottom: 5px;">🤖 AbbasBot AI</h1>
        <p style="font-size: 18px; color: #777; margin-top: 0;">
            Your AI Assistant
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Gemini API key
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(
            content="You are RizviBot AI, a helpful and friendly AI assistant."
        )
    ]

# Display previous messages
for message in st.session_state.chat_history:

    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)

    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

# User input
user_input = st.chat_input("Write your question")

if user_input:

    # Add user message
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    st.chat_message("user").write(user_input)

    # Get AI response
    response = llm.invoke(
        st.session_state.chat_history
    )

    # Extract text from response
    if isinstance(response.content, str):
        answer = response.content
    else:
        answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict)
        )

    # Save AI response
    st.session_state.chat_history.append(
        AIMessage(content=answer)
    )

    # Display AI response
    st.chat_message("assistant").write(answer)
