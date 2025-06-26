import markdown
from pathlib import Path

def load_markdown_file(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as f:
        content: str = f.read()
    html: str = markdown.markdown(content, extensions=["fenced_code", "codehilite"])
    return {"html": html, "raw": content} 