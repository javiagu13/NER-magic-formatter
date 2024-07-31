import sys
import pyperclip
import time

def process_file():
    # Add your file processing code here
     
    def open_website(url):
        webbrowser.open(url)

    def copy_to_clipboard(text):
        pyperclip.copy(text)

    # Example usage
    url = "https://www.chatgpt.com"
    prompt = """
    Please give just the faq part updated with the following styles:

    faq-container
    faq-item
    faq-question
    faq-answer
    dropdown-icon
    .faq-item.active .dropdown-icon
    .faq-item.active .faq-answer
    .faq-item.active .faq-question

This is an example of the structure:
      <div class="blog-subtitle">FAQS TITLE HERE</div>
        <div class="faq-container">
            <div class="faq-item">
                <div class="faq-question">
                   HERE THE QUESTION
                    <span class="dropdown-icon">▼</span>
                </div>
                <div class="faq-answer">
                    HERE THE ANSWER
                </div>
            </div>
            <div class="faq-item">
                <div class="faq-question">
                    HERE THE QUESTION...
    
    """


    # Wait for a brief moment to ensure the page loads
    time.sleep(3)  # Adjust the sleep time as needed

    # Copy text to clipboard
    copy_to_clipboard(prompt)

    print(f"Copied text to clipboard: {prompt}")


if __name__ == "__main__":
    process_file()


