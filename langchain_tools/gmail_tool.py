# langchain_tools/gmail_tool.py

from langchain.tools import tool
from agents.gmail_agent import GmailAgent

gmail_agent = GmailAgent()

@tool
def check_gmail():
    """Checks unread Gmail messages and returns summaries of top 5 emails."""
    return gmail_agent.get_unread_emails()

@tool
def send_email(to: str, subject: str, body: str):
    """Sends an email using Gmail."""
    return gmail_agent.send_email(to, subject, body)
