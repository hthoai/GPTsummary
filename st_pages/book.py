import fitz
import streamlit as st

from components.mermaid import show_diagram
from components.summarizer import Summarizer
from resources.prompts import get_book_system_prompt


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    full_text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf_doc:
        for page_num in range(len(pdf_doc)):
            page = pdf_doc.load_page(page_num)
            full_text += page.get_text()

    return full_text


st.header("Book Summary")
llm = st.session_state.llm
language = st.session_state.language
system_prompt = get_book_system_prompt(language)
summarizer = Summarizer(llm=llm, system_prompt=system_prompt, language=language)

doc = st.file_uploader("Upload PDF", accept_multiple_files=False, type="pdf")

full_text = ""
if doc:
    full_text = extract_text_from_pdf(doc)

if st.button("Summarize", key="summarize_book"):
    if "book_summary" in st.session_state:
        del st.session_state["book_summary"]
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
