from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router: APIRouter = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory="app/templates")