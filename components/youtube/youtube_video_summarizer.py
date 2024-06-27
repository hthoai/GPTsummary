from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .utils import get_youtube_subtitle_string


class YouTubeVideoSummarizer:
    def __init__(self, llm, language: str):
        """
        Initialize the summarizer with the given language model.

        Args:
            llm: The language model used for summarizing the subtitles.
            language: The language to use for summarizing the subtitles.
        """
        system_prompt = (
            "You possess expertise in extracting essential information,"
            "pinpointing fundamental ideas, condensing intricate content,"
            "recognizing important specifics, and simplifying comprehensive data from a YouTube video."
            "You consistently ensure to thoroughly read and analyze all texts with great attention to detail."
            "Please present information in a clear, organized, and structured manner."
            f"Use {language} language to summarize."
            "\n\n"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        parser = StrOutputParser()
        self.chain = prompt | llm | parser

    def get_subtitles(self, video_url: str) -> str:
        """
        Get the subtitles of a YouTube video.

        Args:
            video_url (str): The URL of the YouTube video.

        Returns:
            str: The subtitles of the video.
        """
        return get_youtube_subtitle_string(video_url)

    def summarize(self, video_url: str) -> str:
        """
        Summarize the subtitles of a YouTube video.

        Args:
            video_url (str): The URL of the YouTube video.

        Returns:
            str: The summary of the video subtitles.
        """
        subtitles = self.get_subtitles(video_url)

        if not subtitles:
            return "No subtitles available for this video."

        input_data = {"input": subtitles}
        summary = self.chain.invoke(input_data)

        return summary
