# Document Summarizer

A Streamlit web application that summarizes content from websites and YouTube videos using the Groq API and LangChain.

## Features

- Summarize content from any website URL
- Summarize YouTube video transcripts (requires English subtitles)
- Clean and simple user interface
- Support for both article and video content

## Prerequisites

- Python 3.8 or higher
- Groq API key ([Get it here](https://console.groq.com))
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/document-summarizer.git
cd document-summarizer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and go to `http://localhost:8501`

3. Enter your Groq API key in the sidebar

4. Paste a URL (website or YouTube video) and click "SUMMARIZE"

## Required Environment Variables

- `GROQ_API_KEY`: Your Groq API key

## Notes

- For YouTube videos, English subtitles must be available
- The summary length is set to 750 words by default
- Website summarization works best with article-style content

## Troubleshooting

1. If you get a YouTube transcript error:
   - Make sure the video has English subtitles
   - Try a different video

2. If you get an API key error:
   - Verify your Groq API key is valid
   - Check your internet connection

3. If the website content isn't loading:
   - Make sure the URL is accessible
   - Check if the website allows content scraping
