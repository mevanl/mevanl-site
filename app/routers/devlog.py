from fastapi import APIRouter, Request
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
    return templates.TemplateResponse("devlog.html", {"request": request, "projects": projects})

@router.get("/{project}/", response_class=HTMLResponse)
async def list_devlogs(request: Request, project: str) -> HTMLResponse: 
    project_dir: Path = DEVLOG_DIR / project

    if not project_dir.exists() or not project_dir.is_dir():
        return HTMLResponse("Project not found", status_code=404)
    
    # get devlog project post names
    posts: list[str] = []
    for file in project_dir.glob("*.md"):
        name: str = file.stem 
        posts.append(name)

    return templates.TemplateResponse("devlog_project.html", {"request": request, "project": project, "posts": posts})

@router.get("/{project}/{post_name}", response_class=HTMLResponse)
async def get_devlog_post(request: Request, project: str, post_name: str) -> HTMLResponse: 
    post_path: Path = DEVLOG_DIR / project / f"{post_name}.md"

    if not post_path.exists():
        return HTMLResponse("Devlog not found", status_code=404)

    post: dict[str, str] = load_markdown_file(post_path)

    return templates.TemplateResponse("post.html", {
        "request": request,
        "project": project, 
        "name": post_name,
        "post": post, 
    })
