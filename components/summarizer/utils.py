import re
from typing import Optional

import validators
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled


def get_youtube_subtitle_string(video_url: str) -> str:
    """Return the most appropriate subtitle as a string for a YouTube video.

    Args:
        video_url (str): The URL of the YouTube video.
    """
    try:
        loader = YoutubeLoader.from_youtube_url(
            video_url,
            language=["en", "en-US", "en-UK", "en-GB", "vi", "ja", "ko", "zh-Hans","zh-Hant"],
        )
        transcript = loader.load().page_content

        return transcript
    except (NoTranscriptFound, TranscriptsDisabled):
        return ""


def check_input_type(input_str):
    # Check if input is a single URL
    line = input_str.strip()
    if validators.url(line):
        return line, "url"

    # Check if input is a list of URLs
    lines = input_str.strip().split("\n")
    lines = [line.strip() for line in lines]
    if all(validators.url(line) for line in lines):

        return lines, "urls"

    # If not a URL or list of URLs, consider it as text
    return input_str, "text"


def get_doc_string(input_str):
    res, input_type = check_input_type(input_str)

    if input_type == "url":
        loader = WebBaseLoader(res)
        docs = loader.load()
        res = docs[0].page_content
    elif input_type == "urls":
        loader = WebBaseLoader(res)
        docs = loader.load()
        res = "\n\n".join([doc.page_content for doc in docs])

    return res
