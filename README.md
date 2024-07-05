
<p align="center">
    <h1 align="center">GPTsummary</h1>
</p>
<p align="center">
    <em>Summarizes content from various sources (YouTube videos, books, and webpages and generates visual diagrams to represent the summarized information.</em>
</p>

## Features

- Summarize content from: YouTube videos, PDF books, texts and web pages.
- Generate visual diagrams (using Mermaid) based on summaries

## Setup

1. Clone the repository
2. Install dependencies:

```sh
   pip install -r requirements.txt
```

3. Set up environment variables in .env file (see config.py for required variables)

## Usage

Run the Streamlit app:

```
streamlit run app.py --client.showSidebarNavigation=False 
```

## Repository Structure

```sh
└── GPTsummary/
    ├── app.py
    ├── components/
    │   ├── mermaid/
    │   ├── summarizer/
    ├── pages/
    │   ├── __init__.py
    │   ├── book.py
    │   ├── document.py
    │   └── youtube_video.py
    ├── resources/
    ├── utils.py
    ├── config.py
    └── requirements.txt
```
