from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .utils import get_doc_string, get_youtube_subtitle_string


class Summarizer:
    def __init__(self, llm, system_prompt: str, language: str):
        """
        Initialize the summarizer with the given language model.

        Args:
            llm: The language model used for summarizing.
            system_prompt: The system prompt to use for summarizing.
            language: The language to use for summarizing.
        """
        self.language = language
        self.llm = llm

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        parser = StrOutputParser()
        self.youtube_chain = prompt | llm | parser

    def get_subtitles(self, video_url: str) -> str:
        """
        Get the subtitles of a YouTube video.

        Args:
            video_url (str): The URL of the YouTube video.

        Returns:
            str: The subtitles of the video.
        """
        return get_youtube_subtitle_string(video_url)

    def get_doc_string(self, text: str) -> str:
        """Get text from a document/url(s)."""
        return get_doc_string(text)

    def summarize(self, text: str) -> str:
        """
        Summarize the subtitles of a YouTube video.

        Args:
            text (str): The text to summarize.

        Returns:
            str: The summary of the video subtitles.
        """
        input_data = {"input": text}
        summary = self.youtube_chain.invoke(input_data)

        return summary
