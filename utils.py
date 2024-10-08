import streamlit as st
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_openai import ChatOpenAI

from config import settings


def sidebar_options():
    """Sidebar options for the app."""
    # Sidebar for model selection
    st.sidebar.title("Model Selection")
    model_provider = st.sidebar.selectbox(
        "Choose Model Provider", ["Gemini", "Yi", "Groq"]
    )

    if model_provider == "Gemini":
        model_name = st.sidebar.selectbox(
            "Choose Model", ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-1.5-pro-exp-0801"]
        )
        safety_settings = safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE
        }
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=settings.GOOGLE_API_KEY,
            safety_settings=safety_settings
        )
    elif model_provider == "Yi":
        model_name = st.sidebar.selectbox("Choose Model", ["yi-large"])
        llm = ChatOpenAI(
            model="yi-large",
            temperature=0,
            api_key=settings.YI_API_KEY,
            base_url=settings.YI_BASE_URL,
        )
    elif model_provider == "Groq":
        model_name = st.sidebar.selectbox(
            "Choose Model", ["llama3-70b-8192", "mixtral-8x7b-32768"]
        )
        llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=settings.GROQ_API_KEY,
            base_url=settings.GROQ_BASE_URL,
        )

    st.session_state.llm = llm

    # Sidebar for language selection
    st.sidebar.title("Language Selection")
    language = st.sidebar.selectbox(
        "Choose Language", ["English", "Vietnamese", "Chinese", "Japanese"], index=0
    )
    st.session_state.language = language
