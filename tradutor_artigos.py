import requests
from bs4 import BeautifulSoup
from langchain_openai.chat_models.azure import AzureChatOpenAI


def extract_text_from_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        text = soup.get_text(separator=" ")
        # Limpar texto
        lines = (line.strip() for line in text.splitlines())
        parts = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_clean = "\n".join(part for part in parts if part)
        return text_clean
    else:
        print(f"Failed to retrieve the URL. Status code: {response.status_code}")
        return None


client = AzureChatOpenAI(
    azure_endpoint="URL_ENDPOINT",
    api_key="KEY",
    api_version="2024-02-15-preview",
    deployment_name="gpt-4o-mini",
    max_retries=0,
)


def translate_article(text, lang):
    messages = [
        ("system", "Você Atua como tradutor de textos"),
        ("user", f"Traduza o {text} para o idioma {lang} e responda em marksown"),
    ]

    response = client.invoke(messages)
    print(response.content)
    return response.content


url = "https://dev.to/kenakamu/azure-open-ai-in-vnet-3alo"
text = extract_text_from_url(url)
article = translate_article(text, "pt-br")

print(article)
