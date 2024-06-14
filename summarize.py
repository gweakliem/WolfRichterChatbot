from langchain.text_splitter import MarkdownHeaderTextSplitter
from openai import OpenAI
from pprint import pprint
import dotenv

dotenv.load_dotenv()

MODEL = "gpt-4o"  # "gpt-4-turbo"

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
]


def summarize_article(article_title, markdown_content):
    """Summarizes the content of a given markdown string using OpenAI's GPT-3.5 model and map-reduce approach"""
    if "* * *" in markdown_content:
        markdown_content = "".join(markdown_content.split("* * *")[:-1])

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, strip_headers=False
    )
    section_splits = markdown_splitter.split_text(markdown_content)

    openai_client = OpenAI()

    section_summaries = []
    for i, section in enumerate(section_splits):
        section_content = section.page_content
        section_header = list(section.metadata.values())[-1]
        section_completion = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"Summarize the following snippet of a Wolf Street article in markdown. "
                    f"Be concise and objective, with 3-5 sentences per section. Return a plain text paragraph, no formatting or new lines: {section_content}",
                }
            ],
        )
        section_summary = (
            section_header + ": " + section_completion.choices[0].message.content
        )
        section_summaries.append(section_summary)
        print(f"({i + 1}/{len(section_splits)}): {section_summary}")

    section_summaries = "\n".join(section_summaries)
    article_completion = openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"The following is a set of summaries from a Wolf Street article split by its sections: {section_summaries} "
                f"Take these and place it in a packaged, paragraph summary about the article. "
                f"In the event of an interview, intuit what the name abbreviations are from the section headers and use their names. "
                f"Mention the name of every section. The summary should use all the points mentioned below. "
                f"Return plain text paragraph, no formatting and no new lines.",
            }
        ],
    )
    print("Full summary: " + article_completion.choices[0].message.content + "\n\n")
    return article_completion.choices[0].message.content


def analyze_image(image_url):
    # call_openai()
    openai_client = OpenAI()
    img_sum = openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"The image in this link may contain a graph. If it does, extract the data from"
                        f"this image into a table. Create a row for each label on the Y axis. Do not"
                        f"interpolate any rows that are not indicated on the X axis. Use the text"
                        f"embedded in the image to extract a title for the graph and units for the Y axis."
                        f"Do not include any other explanatory information",
                    },
                    {"type": "image_url", "image_url": {"url": f"{image_url}"}},
                ],
            }
        ],
    )
    return img_sum.choices[0].message.content
