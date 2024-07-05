import streamlit as st

from components.mermaid import show_diagram
from components.summarizer import Summarizer


def summarize_youtube_video(summarizer: Summarizer):
    """Summarize the subtitles of a YouTube video."""

    video_url = st.text_input("Enter the YouTube video URL")
    if st.button("Summarize", key="summarize_video"):
        with st.spinner("Summarizing..."):
            text = summarizer.get_subtitles(video_url)
            if not text:
                st.warning("No subtitles available for this video.")
            else:
                summary = summarizer.summarize(text)
                st.session_state.video_summary = summary

    if "video_summary" in st.session_state:
        st.subheader("Summary")
        st.write(st.session_state.video_summary)

        st.subheader("Diagram")
        if st.button("Generate Diagram", key="video_generate_diagram"):
            with st.spinner("Generating diagram..."):
                show_diagram(
                    llm=summarizer.llm,
                    language=summarizer.language,
                    text=st.session_state.video_summary,
                )
