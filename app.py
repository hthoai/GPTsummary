import fitz
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from config import settings
from pages import summarize_youtube_video

st.set_page_config(page_title="GPTsummary", layout="wide")

# Initialize session state
for key in [
    "document_summary",
    "document_translated_summary",
    "video_summary",
    "video_translated_summary",
]:
    if key not in st.session_state:
        st.session_state[key] = None

# Sidebar for model selection
st.sidebar.title("Model Selection")
model_provider = st.sidebar.selectbox("Choose Model Provider", ["Gemini", "Yi", "Groq"])

if model_provider == "Gemini":
    model_name = st.sidebar.selectbox(
        "Choose Model", ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest"]
    )
    llm = ChatGoogleGenerativeAI(
        model=model_name, temperature=0, google_api_key=settings.GOOGLE_API_KEY
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

# Sidebar for language selection
st.sidebar.title("Language Selection")
language = st.sidebar.selectbox(
    "Choose Language", ["English", "Vietnamese", "Chinese", "Japanese"], index=0
)

document_tab, video_tab, book_tab = st.tabs(
    ["📝 Document", "📹 YouTube Video", "📚 Book"]
)

with video_tab:
    summarize_youtube_video(llm=llm, language=language)

with book_tab:
    original_doc = st.file_uploader(
        "Upload PDF", accept_multiple_files=False, type="pdf"
    )
    text_lookup = st.text_input("Look for", max_chars=1000)

    if original_doc:
        with fitz.open(stream=original_doc.getvalue()) as doc:
            page_number = st.sidebar.number_input(
                "Page number", min_value=1, max_value=doc.page_count, value=1, step=1
            )
            page = doc.load_page(page_number - 1)

            if text_lookup:
                areas = page.search_for(text_lookup)

                for area in areas:
                    page.add_rect_annot(area)

                pix = page.get_pixmap(dpi=120).tobytes()
                st.image(pix, use_column_width=True)
