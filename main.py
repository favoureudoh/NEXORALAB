from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from database import engine, Base
from routers import auth_routes, dashboard_routes

# Create all tables in MySQL if they don't exist yet
Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance
app = FastAPI()

# Mount the static folder so CSS and JS files are accessible
app.mount("/static", StaticFiles(directory="static"), name="static")

# Tell FastAPI where the HTML templates are
templates = Jinja2Templates(directory="templates")

# Register all auth routes (register, login, logout)
app.include_router(auth_routes.router)

# Register dashboard routes
app.include_router(dashboard_routes.router)


# ── LANDING PAGE ──
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
