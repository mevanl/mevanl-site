from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import homepage, blog, devlog


app: FastAPI = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# templating
templates: Jinja2Templates = Jinja2Templates(directory="app/templates")

# 404 route
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

# routers
app.include_router(homepage.router)
app.include_router(blog.router, prefix="/blog")
app.include_router(devlog.router, prefix="/devlogs")

