from pathlib import Path
import trafilatura
from bs4 import BeautifulSoup

def load_html(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # extract main content, excluding nav/footer
    raw_text = trafilatura.extract(html_content, include_links=False, include_images=False, favor_precision=True)
    
    if not raw_text:
        soup = BeautifulSoup(html_content, "html.parser")
        # Remove nav, footer, script, style
        for element in soup(["nav", "footer", "script", "style", "header", "aside"]):
            element.decompose()
        raw_text = soup.get_text(separator="\n", strip=True)
        
    metadata = {}
    return raw_text, "html", "en", metadata
