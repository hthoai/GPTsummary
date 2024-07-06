import streamlit as st

from utils import sidebar_options

if __name__ == "__main__":
    st.set_page_config(
        page_title="GPTsummary", layout="wide", page_icon="resources/summary.png"
    )
    sidebar_options()

    # Create pages
    document_page = st.Page(
        page="st_pages/document.py",
        title="Document",
        icon=":material/article:",
    )
    video_page = st.Page(
        page="st_pages/youtube_video.py",
        title="YouTube Video",
        icon=":material/smart_display:",
    )
    book_page = st.Page(
        page="st_pages/book.py",
        title="Book",
        icon=":material/book:",
    )

    page = st.navigation([video_page, document_page, book_page])

    page.run()
