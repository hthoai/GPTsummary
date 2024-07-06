import streamlit as st

from components.mermaid import show_diagram
from components.summarizer import Summarizer
from resources.prompts import get_webpage_summary_prompt

st.header("Document/Webpage Summary")
llm = st.session_state.llm
language = st.session_state.language
system_prompt = get_webpage_summary_prompt(language)
summarizer = Summarizer(llm=llm, system_prompt=system_prompt, language=language)

text = None
doc_input = st.text_area("Enter document text or URL(s)")
if st.button("Summarize", key="summarize_doc"):
    if "doc_summary" in st.session_state:
        del st.session_state["doc_summary"]
    with st.spinner("Summarizing..."):
        if not doc_input:
            st.warning("Please enter some text or URL(s) to summarize.")
        else:
            text = summarizer.get_doc_string(doc_input)
            if text:
                summary = summarizer.summarize(text)
                st.session_state.doc_summary = summary

if "doc_summary" in st.session_state:
    st.subheader("Summary")
    st.write(st.session_state.doc_summary)

    st.subheader("Diagram")
    if st.button("Generate Diagram", key="doc_generate_diagram"):
        with st.spinner("Generating diagram..."):
            show_diagram(
                llm=summarizer.llm,
                language=summarizer.language,
                text=st.session_state.doc_summary,
            )
