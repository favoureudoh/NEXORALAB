from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from auth import decode_access_token
import models

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ── DASHBOARD PAGE ──
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    # Read token from cookie
    token = request.cookies.get("access_token")

    # No token means not logged in
    if not token:
        return RedirectResponse(url="/login", status_code=302)

    # Decode the token to get the email
    payload = decode_access_token(token)

    if not payload:
        return RedirectResponse(url="/login", status_code=302)

    email = payload.get("sub")

    if not email:
        return RedirectResponse(url="/login", status_code=302)

    # Find the member in the database
    member = db.query(models.Member).filter(models.Member.email == email).first()

    # Member not found
    if not member:
        return RedirectResponse(url="/login", status_code=302)

    # All good — show the dashboard
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "first_name": member.first_name,
            "last_name": member.last_name,
            "username": member.username,
            "email": member.email,
            "joined_at": member.joined_at,
        },
    )
