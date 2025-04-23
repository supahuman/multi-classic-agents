# main.py

from langchain_tools.gmail_tool import check_gmail, send_email

if __name__ == "__main__":
    print("Testing Gmail integration...")

    # Test checking Gmail
    print(check_gmail.invoke({}))

    # Test sending an email
    print(send_email.invoke({
        "to": "example@example.com",
        "subject": "Test Email",
        "body": "This is a test email."
    }))
