import base64
import re
from bs4 import BeautifulSoup
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 


def extract_email_body(payload):
    """Extracts and cleans email body from Gmail payload, prefers plain text, falls back to HTML."""
    body = ""

    # Get the body content from parts or main body
    if 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')
            data = part.get('body', {}).get('data', '')
            if data:
                decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                if mime_type == 'text/plain':
                    body = decoded
                    break  # Prefer plain text
                elif mime_type == 'text/html' and not body:
                    body = BeautifulSoup(decoded, 'html.parser').get_text()
    else:
        data = payload.get('body', {}).get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    # Clean up the text to remove extra spaces, URLs, and non-ASCII characters
    body = re.sub(r'\s+', ' ', body)  # Collapse whitespace
    body = re.sub(r'http\S+', '', body)  # Remove raw URLs
    body = re.sub(r'[^\x00-\x7F]+', ' ', body)  # Remove non-ASCII characters
    body = body.strip()

    return body

def extract_links(text):
    """Extracts all clean URLs from the original text."""
    return re.findall(r'https?://[^\s"<>]+', text)

def summarize_text(text):
    """Uses an LLM to summarize the text in 2–3 concise sentences."""
    llm = OpenAI(temperature=0.3)
    prompt = (
        "Summarize the following email content into 2-3 concise sentences. "
        "Focus on the core message, product highlights, or actions required:\n\n"
        f"{text}"
    )
    return llm.invoke(prompt)

def clean_email_content(payload):
    """Processes email payload into clean summary and links."""
    raw_text = extract_email_body(payload)
    summary = summarize_text(raw_text)
    links = extract_links(raw_text)
    
    return {
        'summary': summary.strip(),
        'links': links
    }

def clean_html_content(html_content):
    """Cleans the provided HTML content and removes any unwanted sections."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove unwanted parts like footer, unsubscribe links, etc.
    for unwanted_tag in soup(['footer', 'a', 'div', 'span', 'style']):
        unwanted_tag.decompose()

    # Clean the remaining text
    cleaned_text = soup.get_text(separator=' ', strip=True)

    # Further clean up by removing extra spaces and non-ASCII characters
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Collapse whitespace
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', cleaned_text)  # Remove non-ASCII characters

    return cleaned_text

# Example of usage:
# Assuming 'payload' is the Gmail message payload you've received

payload = {}  # This would be the actual payload you're working with
cleaned_email = clean_email_content(payload)

# For cleaning an HTML string directly
html_content = "<html> <body> ... </body> </html>"  # Replace with actual HTML content
cleaned_html = clean_html_content(html_content)

print(cleaned_email)
print(cleaned_html)
