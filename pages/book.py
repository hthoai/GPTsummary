import fitz
import streamlit as st

from components.mermaid import show_diagram
from components.summarizer import Summarizer


def summarize_book(summarizer: Summarizer):
    doc = st.file_uploader("Upload PDF", accept_multiple_files=False, type="pdf")

    if doc:
        # Open the PDF file
        with fitz.open(stream=doc.read(), filetype="pdf") as pdf_doc:
            # Extract all text from the PDF
            full_text = ""
            for page_num in range(len(pdf_doc)):
                page = pdf_doc.load_page(page_num)
                full_text += page.get_text()

    if st.button("Summarize", key="summarize_book"):
        with st.spinner("Summarizing..."):
            if not full_text:
                st.warning("Can't extract text from PDF.")
            else:
                summary = summarizer.summarize(full_text)
                st.session_state.book_summary = summary

    if "book_summary" in st.session_state:
        st.subheader("Summary")
        st.write(st.session_state.book_summary)

        st.subheader("Diagram")
        if st.button("Generate Diagram", key="book_generate_diagram"):
            with st.spinner("Generating diagram..."):
                show_diagram(
                    llm=summarizer.llm,
                    language=summarizer.language,
                    text=st.session_state.book_summary,
                )
