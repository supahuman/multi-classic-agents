# tools/summarizer.py

from langchain_openai import ChatOpenAI

def summarize_email(email_content):
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        summary = llm.invoke(f"Summarize the following email:\n\n{email_content}")
        return summary.content if hasattr(summary, "content") else str(summary)
    except Exception as e:
        return f"An error occurred: {e}"
