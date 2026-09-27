import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}


def extract_article_text(url):
    """
    Download an article and extract readable paragraph text.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(f"⚠️ Could not fetch article: {error}")
        return ""

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    # Remove elements that usually contain noise
    for element in soup(
        ["script", "style", "nav", "footer", "header"]
    ):
        element.decompose()

    paragraphs = soup.find_all("p")

    text_parts = []

    for paragraph in paragraphs:
        text = paragraph.get_text(
            " ",
            strip=True,
        )

        if len(text) >= 40:
            text_parts.append(text)

    article_text = "\n".join(text_parts)

    return article_text