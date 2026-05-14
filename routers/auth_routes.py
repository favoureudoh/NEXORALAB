from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from auth import hash_password, verify_password, create_access_token
import models

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ── REGISTER PAGE ──
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


@router.post("/register")
def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):

    # Check if email is already taken
    existing_email = (
        db.query(models.Member).filter(models.Member.email == email).first()
    )

    if existing_email:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "An account with that email already exists"},
        )

    # Check if username is already taken
    existing_username = (
        db.query(models.Member).filter(models.Member.username == username).first()
    )

    if existing_username:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "That username is already taken"},
        )

    # Hash the password then save the new member
    new_member = models.Member(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=hash_password(password),
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return RedirectResponse(url="/login?registered=true", status_code=302)


# ── LOGIN PAGE ──
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, registered: str = None):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"registered": registered}
    )


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # Find member by email
    member = db.query(models.Member).filter(models.Member.email == email).first()

    # Wrong email or wrong password
    if not member or not verify_password(password, member.password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password"},
        )

    # Create token and set it as a cookie
    token = create_access_token(data={"sub": member.email})

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)
    return response


# ── LOGOUT ──
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response
