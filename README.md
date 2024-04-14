# UnofficialWolf Street Chatbot
[![Real-time Wolf Street Article Updater](https://github.com/benfwalla/BenThompsonChatbot/actions/workflows/check_for_latest_articles.yml/badge.svg?event=schedule)](https://github.com/benfwalla/BenThompsonChatbot/actions/workflows/check_for_latest_articles.yml)

## 🎈 [Use on Streamlit now!](https://unofficial-wolfstreet-chatbot.streamlit.app/)
![WolfStreet Chatbot](img/WolfStreet%20Chatbot%20_%20Streamlit.jpeg)

## What does this bot know?
The bot knows about Wolf Richter, Wolf Street, and the [Wolf Street](https://wolfstreet.com/) articles listed in [data.json](data.json). 
The oldest known article dates back to 05 Apr 2024.

## How was this bot built?
- Wolf Street articles were saved as markdown files, split into smaller chunks, and embedded in a [Chroma](https://www.trychroma.com/) database.
- On (almost) every query, the bot embeds your query, identifies the 7 most similar article chunks and 0-3 most relevant article summaries and places them into GPT's context to answer your question. This technique is known as *[Retreival-Augmented Generation (RAG)](https://stackoverflow.blog/2023/10/18/retrieval-augmented-generation-keeping-llms-relevant-and-current/)*.
- RAG is far from perfect! I used the open-sourced [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model to create the embeddings. I used it because it's free (I'm cheap) and has [good speed and performance](https://huggingface.co/blog/mteb) for what you're getting.
- I removed all those markdown Wolf Street articles from this repo out of respect to Wolf Richter.

### [data.py](data.py)
data.py is a mess of a codebase that shows how I retrieved, chunked, and embedded the Wolf Street articles

### [chatbot.py](chatbot.py)
chatbot.py is the UI logic for the Streamlit chatbot.

### [chatbot_helper.py](chatbot_helper.py)
chatbot_helper.py is the helper functions for the Streamlit chatbot. This is where the magic happens with the GPT chat completions.

## Who built this bot?
This bot was built by [Gordon Weakliem](https://github.com/gweakliem). He's been a Wolf Street reader for about 4 years and donates to the site. He wanted to learn more about AI chatbots and RAG and this code was forked from the [StratecheryChatbot](https://unofficial-stratechery-chatbot.streamlit.app/), a GPT bot that uses RAG to answer questions about the Stratechery weblog.

_Disclaimer: This app is not affiliated with, endorsed by, or approved by Wolf Richter or Wolf Street._