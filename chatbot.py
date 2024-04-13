import random
import time
import streamlit as st
from chatbot_helper import (SYSTEM_MESSAGE, NUM_ARTICLES, MOST_RECENT_ARTICLE_TITLE, MOST_RECENT_ARTICLE_DATE,
                            MOST_RECENT_ARTICLE_URL, create_chat_completion_with_rag)
from openai import OpenAI

st.set_page_config(
    page_title="WolfStreet Chatbot",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("styles/styles.css") as css:
    css_content = css.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

# SIDEBAR
APP_DESCRIPTION = f"""
- It is *not* approved by Wolf Richter or any Wolf Street affiliates.
"""

openai_client = OpenAI()
with st.sidebar:
    gpt_model = st.selectbox('Select a Model', ('gpt-3.5-turbo', 'gpt-4-turbo-preview'))
    st.divider()
    with st.expander("What does this bot know?"):
        st.write(f"The bot knows about Wolf Richter, [Wolf Street](https://wolfstreet.com/), and the {NUM_ARTICLES} most recent Wolf Street articles. The oldest known article dates back to Nov 8, 2023. **It was last updated on {MOST_RECENT_ARTICLE_DATE}.**")
    with st.expander("How was this bot built?"):
        st.write(f"""
        - You can find the code **[here](https://github.com/gweakliem/WolfRichterChatbot)**.
        - WolfStreet articles were saved as markdown files, split into smaller chunks, and embedded in a [Chroma](https://www.trychroma.com/) database.
        - On (almost) every query, the bot embeds your query, identifies the 7 most similar article chunks, and places them into GPT's context to answer your question. This technique is known as *[Retreival-Augmented Generation (RAG)](https://stackoverflow.blog/2023/10/18/retrieval-augmented-generation-keeping-llms-relevant-and-current/)*.
        - I used the open-sourced [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model to create the embeddings. I used it because it's free (I'm cheap) and has [good speed and performance](https://huggingface.co/blog/mteb) for what you're getting.
        """)
    with st.expander("Why did you use RAG to retrieve the articles?"):
        st.write(f"""
        Imagine trying to copy & paste all Wolf Street articles into ChatGPT... you'll get an error! This is because GPT's _context_ can only fit so much.
        RAG solves this by being a simple search engine: based on the user's text, RAG finds the most similar chunks of text from all Wolf Street articles. We then
        copy & paste those into GPT's context. RAG is far from perfect! That is why I augmented my RAG approach by inserting [metadata about Wolf Street](https://github.com/gweakliem/WolfRichterChatbot/blob/master/chatbot_helper.py#L49) and relevant [pre-summarized articles](https://github.com/gweakliem/WolfRichterChatbot/blob/master/data.json) into context.
        
        As context windows increase (Gemini 1.5 [can fit 700,000 words in its context](https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#context-window)), RAG will likely become [a historic solution](https://medium.com/@erisco_and/the-end-of-retrieval-augmented-generation-emerging-architectures-signal-a-shift-fdf0aad74d50).
        But for now, it makes my solution more cost effective.
        """)
    with st.expander("Why did you use GPT as the LLM?"):
        st.write(f"""
        GPT's [Functional calling](https://platform.openai.com/docs/guides/function-calling) is a genuine product differentior from other LLM APIs. It helped me perform RAG much more efficiently by allowing me to manipulate my article querying based on the user's question.\n
        Anthropic's Claude [also has function calling](https://docs.anthropic.com/claude/docs/functions-external-tools) that I should check out.
        """)
    with st.expander("Who built this bot?"):
        st.write("This bot was built by [Gordon Weakliem](https://github.com/gweakliem). He's been a Wolf Street reader for about 4 years and while Wolf Street has no paywall, he has [contributed voluntarily](https://wolfstreet.com/how-to-donate-to-wolf-street/) and encourages you to do the same if you find Wolf's articles useful. He wanted to experiment with RAG and LLMtraining and was inspired by the [BenThompsonChatbot](https://github.com/benfwalla/BenThompsonChatbot), an experimantel RAG approach using Ben Thompson's Newsletters.")
    st.divider()
    st.caption("_Disclaimer: This app is not affiliated with, endorsed by, or approved by Wolf Richter or Wolf Street._")
    st.caption(f"Last updated: {MOST_RECENT_ARTICLE_DATE}")
    st.caption(f"Most recent known article: [{MOST_RECENT_ARTICLE_TITLE}]({MOST_RECENT_ARTICLE_URL}) ({MOST_RECENT_ARTICLE_DATE})")

# CHATBOT
st.title("Wolf Richter Wolf Street Chatbot")
st.caption(f"_Ask me anything about Wolf Street! I'm have knowledge on the {NUM_ARTICLES} most recent articles._")


def add_message_and_respond(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner(""):
            stream = create_chat_completion_with_rag(prompt,
                                                     [{"role": msg["role"], "content": msg["content"]} for msg in
                                                      st.session_state.messages],
                                                     gpt_model)
        if type(stream) is str:
            def stream_data():
                for word in stream.split():
                    yield word + " "
                    time.sleep(random.uniform(0.01, 0.03))

            st.write_stream(stream_data())
            response = stream
        else:
            response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


button_container = st.empty()
button_string = ""
with button_container:
    col1, col2 = st.columns(2, gap="small")
    questions = [
        "What does Wolf think about inflation in the United States?",
        "Provide the key points in Wolf Street's analysis of the most recent CPI report",
        "What is the likely floor on the Federal Reserve Bank's balance sheet?",
        f"Summarize \"{MOST_RECENT_ARTICLE_TITLE}\""
    ]
    with col1:
        if st.button(questions[0], use_container_width=True):
            button_string = questions[0]
        if st.button(questions[1], use_container_width=True):
            button_string = questions[1]
    with col2:
        if st.button(questions[2], use_container_width=True):
            button_string = questions[2]
        if st.button(questions[3], use_container_width=True):
            button_string = questions[3]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if button_string:
    button_container.empty()
    add_message_and_respond(button_string)

if prompt := st.chat_input(placeholder="Message WolfStreetBot..."):
    button_container.empty()
    add_message_and_respond(prompt)
