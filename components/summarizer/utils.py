import re
from typing import Optional

import validators
from langchain_community.document_loaders import WebBaseLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled


def extract_video_id_from_url(url):
    video_id_pattern = r'(?:v=|/v/|youtu\.be/|/embed/|/e/)([^?&"\'>]+)'
    match = re.search(video_id_pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")


def find_transcript(
    transcript_list, languages: list[str], manually_created: bool = True
) -> Optional[str]:
    """Find a transcript in the specified languages.

    Args:
        transcript_list: The list of available transcripts.
        languages (list[str]): The list of language codes to search for.
        manually_created (bool): Whether to search for manually created transcripts.

    Returns:
        Optional[str]: The transcript string if found, otherwise None.
    """
    for lang in languages:
        try:
            if manually_created:
                transcript = transcript_list.find_manually_created_transcript([lang])
            else:
                transcript = transcript_list.find_transcript([lang])
            return get_transcript_string(transcript)
        except (NoTranscriptFound, TranscriptsDisabled):
            continue
    return None


def get_transcript_string(transcript):
    return " ".join([item["text"] for item in transcript.fetch()])


def get_youtube_subtitle_string(video_url: str) -> str:
    """Return the most appropriate subtitle as a string for a YouTube video.

    Args:
        video_url (str): The URL of the YouTube video.
    """
    video_id = extract_video_id_from_url(video_url)
    if not video_id:
        return ""

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except (NoTranscriptFound, TranscriptsDisabled):
        return ""

    # Define the order of languages to search for transcripts
    languages_priority = [
        # Manually created
        (["en"], True),
        (["en-US"], True),
        (["en-UK"], True),
        (["en-GB"], True),
        (["vi"], True),
        # Auto-generated
        (["en"], False),
        (["vi"], False),
    ]

    for languages, manually_created in languages_priority:
        transcript = find_transcript(transcript_list, languages, manually_created)
        if transcript:
            return transcript

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
