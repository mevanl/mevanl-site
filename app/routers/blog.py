from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
from app.internal.markdown_util import load_markdown_file

BLOG_DIR: Path = Path("content/blog")

router: APIRouter = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_blog(request: Request) -> HTMLResponse:
    posts: list[dict[str, str]] = []

    # grab only the markdown files
    for file in BLOG_DIR.glob("*.md"):
        name: str = file.stem
        post: dict[str, str | dict[str, str]] = load_markdown_file(file)
        meta = post["metadata"] if isinstance(post["metadata"], dict) else {}

        posts.append({
            "name": name,
            "title": meta.get("title", name),
            "date": meta.get("date", ""), 
            "summary": meta.get("summary", "")
        })

    # sort by date
    posts.sort(key=lambda p: p.get("date") or "", reverse=True)

    return templates.TemplateResponse("blog.html", {"request": request, "posts": posts})

@router.get("/{post_name}", response_class=HTMLResponse)
async def get_post(request: Request, post_name: str) -> HTMLResponse:
    path: Path = BLOG_DIR / f"{post_name}.md"

    if not path.exists():
        raise HTTPException(status_code=404, detail="post not found")

    post: dict[str, str | dict[str, str]] = load_markdown_file(path)

    return templates.TemplateResponse("post.html", {"request": request, "name": post_name, "post": post})