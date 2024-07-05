from typing import Tuple

import streamlit as st

from components.summarizer import Summarizer
from pages import summarize_book, summarize_doc, summarize_youtube_video
from resources.prompts import (
    get_book_system_prompt,
    get_webpage_summary_prompt,
    get_youtube_system_prompt,
)
from utils import sidebar_options


def create_summarizers(
    llm: object, language: str
) -> Tuple[Summarizer, Summarizer, Summarizer]:
    """
    Create summarizers for different types of content.

    Args:
        llm (object): The language model object.
        language (str): The language for summarization.

    Returns:
        Tuple[Summarizer, Summarizer, Summarizer]: Summarizers for YouTube, books, and documents.
    """
    youtube_summarizer = Summarizer(
        llm=llm, system_prompt=get_youtube_system_prompt(language), language=language
    )
    book_summarizer = Summarizer(
        llm=llm, system_prompt=get_book_system_prompt(language), language=language
    )
    doc_summarizer = Summarizer(
        llm=llm, system_prompt=get_webpage_summary_prompt(language), language=language
    )
    return youtube_summarizer, book_summarizer, doc_summarizer


if __name__ == "__main__":
    st.set_page_config(page_title="GPTsummary", layout="wide")

    llm, language = sidebar_options()
    youtube_summarizer, book_summarizer, doc_summarizer = create_summarizers(
        llm, language
    )

    # Create tabs for different summarization options
    document_tab, video_tab, book_tab = st.tabs(
        ["📝 Document", "📹 YouTube Video", "📚 Book"]
    )

    with document_tab:
        summarize_doc(doc_summarizer)

    with video_tab:
        summarize_youtube_video(youtube_summarizer)

    with book_tab:
        summarize_book(book_summarizer)
