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
    En el blog quiero que sugieras donde deberian ir imagenes y que deberian aparecer en ellas. deja el blog como esta, pero añade un texto en el siguiente formato en cada sitio que consideres que deberia ir una imagen:

_(Imagen sugerida: Aqui tu sugerencia.)_"""


    # Wait for a brief moment to ensure the page loads
    time.sleep(3)  # Adjust the sleep time as needed

    # Copy text to clipboard
    copy_to_clipboard(prompt)

    print(f"Copied text to clipboard: {prompt}")


if __name__ == "__main__":
    process_file()


