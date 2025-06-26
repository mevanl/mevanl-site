import markdown
import yaml
from pathlib import Path

def load_markdown_file(path: Path) -> dict[str, str | dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        content: str = f.read()
    
    metadata: dict = {}
    body: str = content
    
    # get metadata 
    if content.startswith("---"):
        try:
            _, frontmatter, body = content.split("---", maxsplit=2)
            metadata = yaml.safe_load(frontmatter.strip()) or {}
        except Exception:
            metadata = {}
            body = content 
    
    html: str = markdown.markdown(body, extensions=["fenced_code", "codehilite"])

    return {"html": html, "raw": body, "metadata": metadata} 