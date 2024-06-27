import streamlit as st

from components.mermaid import show_diagram
from components.youtube import YouTubeVideoSummarizer


def summarize_youtube_video(llm, language):
    # st.header("YouTube Video")
    video_url = st.text_input("Enter the YouTube video URL")
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            st.session_state.summary = YouTubeVideoSummarizer(
                llm=llm, language=language
            ).summarize(video_url)

    if "summary" in st.session_state:
        st.subheader("Summary")
        st.write(st.session_state.summary)

        st.subheader("Diagram")
        if st.button("Generate Diagram"):
            with st.spinner("Generating diagram..."):
                show_diagram(llm=llm, language=language, text=st.session_state.summary)
