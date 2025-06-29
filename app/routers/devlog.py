from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
from app.internal.markdown_util import load_markdown_file 

DEVLOG_DIR: Path = Path("content/devlog")

router: APIRouter = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_projects(request: Request) -> HTMLResponse:

    projects: list[str] = [p.name for p in DEVLOG_DIR.iterdir() if p.is_dir()]
    return templates.TemplateResponse("devlogs.html", {"request": request, "projects": projects})

@router.get("/{project}/", response_class=HTMLResponse)
async def list_devlogs(request: Request, project: str) -> HTMLResponse: 
    project_dir: Path = DEVLOG_DIR / project

    if not project_dir.exists() or not project_dir.is_dir():
        raise HTTPException(status_code=404, detail="project not found")
    
    posts: list[dict[str, str]] = []
   
    for file in project_dir.glob("*.md"):
        name: str = file.stem
        post: dict[str, str | dict[str, str]] = load_markdown_file(file)
        meta = post["metadata"] if isinstance(post["metadata"], dict) else {}
    
        posts.append({
            "name": name,
            "title": meta.get("title", name),
            "date": meta.get("date", ""),
            "summary": meta.get("summary", "")
            })

    posts.sort(key=lambda p: p.get("date") or "", reverse=True)

    return templates.TemplateResponse("devlog_project.html", {
        "request": request,
        "project": project,
        "posts": posts
    })


@router.get("/{project}/{post_name}", response_class=HTMLResponse)
async def get_devlog_post(request: Request, project: str, post_name: str) -> HTMLResponse: 
    post_path: Path = DEVLOG_DIR / project / f"{post_name}.md"

    if not post_path.exists():
        raise HTTPException(status_code=404, detail="devlog not found")

    post: dict[str, str | dict[str, str]] = load_markdown_file(post_path)

    return templates.TemplateResponse("post.html", {
        "request": request,
        "project": project, 
        "name": post_name,
        "post": post, 
    })
