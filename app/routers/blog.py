from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
from app.internal.markdown_util import load_markdown_file

BLOG_DIR: Path = Path("content/blog")

router: APIRouter = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_blog(request: Request) -> HTMLResponse:
    #posts: list[dict[str, str]] = []
    posts: list[str] = []

    # grab only the markdown files
    for file in BLOG_DIR.glob("*.md"):
        name: str = file.stem

        # we only want the name for now 
        # post: dict[str, str] = load_markdown_file(file)
        #posts.append({"name": name, "html": post["html"]}) 

        posts.append(name)
    
    return templates.TemplateResponse("blog.html", {"request": request, "posts": posts})

@router.get("/{post_name}", response_class=HTMLResponse)
async def get_post(request: Request, post_name: str) -> HTMLResponse:
    path: Path = BLOG_DIR / f"{post_name}.md"

    if not path.exists():
        # TODO: have a 404.html to be fancy 
        return HTMLResponse("Post not found", status_code=404)

    post: dict[str, str] = load_markdown_file(path)

    return templates.TemplateResponse("post.html", {"request": request, "name": post_name, "post": post})