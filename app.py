from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import streamlit as st
import validators
import nltk
from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Function to validate the API Key
def validate_api_key(groq_api_key):
    try:
        llm = ChatGroq(model = "gemma2-9b-it",
                    groq_api_key = groq_api_key)
        # Making a test query to validate API Key
        message = [
            ("system","Just say hello"),
            ("human", "test connection")
        ]
        llm.invoke(message)
        return True
    except Exception as e:
        print(e)
        return False

## getting the video id
def extract_video_id(url):
    video_id = None
    # Check for various YouTube URL formats
    if "youtube.com/watch?v=" in url:
        video_id = url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
    return video_id


## getting the youtube transcript
def get_youtube_transcript(url):    
    try:
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("Could not extract video ID from URL")
        
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages = ['en-GB', 'en', 'en-US']) ## added some more languages for transcripts
        
        # Combine all transcript text
        transcript_text = " ".join([entry['text'] for entry in transcript_list])
        
        # Create a Document object compatible with LangChain
        doc = Document(
            page_content=transcript_text,
            metadata={"source": url}
        )
        
        return [doc]  # Return as list to match loader.load() format
    
    except Exception as e:
        st.error(f"Could not retrieve a transcript for the video, This is most likely caused by: Subtitles are disabled for this video")
        st.error(f"error: {str(e)}")
        return None

## Making prompt and initializing the model

map_prompt_template = """
Write a summary of the following content in less than 750 words:
content : {text}
"""
combine_prompt_template = """
Provide the final summary of the entire content
with these important points. Add a suitable, professional and more 
crisp title.
Points : {text}
"""
map_prompt = PromptTemplate(
    input_variables = ["text"],
    template = map_prompt_template
    )
combine_prompt = PromptTemplate(
    input_variables = ["text"],
    template = combine_prompt_template
    )


# streamlit app
st.set_page_config(page_title = "Document Summarizer", page_icon = "🌐")
st.title("Document Summarizer")

# getting API Key
groq_api_key = st.sidebar.text_input("TYPE YOUR GROQ API KEY⬇️⬇️ ",placeholder = "GROQ API Key", type = "password")

if not groq_api_key or not validate_api_key(groq_api_key):
    st.sidebar.error("PLEASE ENTER A VALID API KEY")
else:
    st.sidebar.success("VALIDATED GROQ API KEY✅")
    llm = ChatGroq(groq_api_key = groq_api_key,
               model = "gemma2-9b-it")
    chain = load_summarize_chain(llm = llm,
                             chain_type = "map_reduce",
                             map_prompt = map_prompt,
                             combine_prompt = combine_prompt,
                             verbose = True
                             )

    
    url = st.text_input("Type the URL", label_visibility = "collapsed")
    if st.button("SUMMARIZE"):
        ## validating the inputs
        if not url.strip():
            st.error("Please provide URL")
        elif not validators.url(url):
            st.error("Please provide a VALID URL")
        else:
            try:
                with st.spinner("Loading🔃.."):
                    ## loading the website or yt video data
                    if "youtube.com" in url or "youtu.be" in url:
                        data = get_youtube_transcript(url)
                    else:
                        loader = UnstructuredURLLoader(urls = [url],
                                                       ssl_verify = False, ## For allowing only secure URLs
                                                       headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chroma/116.0.0.0 Safari/537.36)"} 
                                                       ## header contains which all websites we can allow
                                                       )
                        data = loader.load()
                    if data:
                        splitter = RecursiveCharacterTextSplitter(chunk_size = 2000,
                                            chunk_overlap = 200)
                        docs = splitter.split_documents(data)
                        summary = chain.run(docs)

                        st.success(summary)                      
                                                        
            except Exception as e:
                st.error(e)
                print(e)
