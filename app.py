from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils import ALERTS_TEMPLATES, valid_url
import requests


app = FastAPI()

templates = Jinja2Templates(directory="templates/", autoescape=False)


@app.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/", response_class=HTMLResponse)
def unshorten(request: Request, url: str = Form("")):
    if not valid_url(url):
        return templates.TemplateResponse(
            "index.html",
            context={
                "request": request,
                "final_text": ALERTS_TEMPLATES["error"].format("Not a valid LINK"),
            },
        )

    try:
        session = requests.Session()
        response = session.head(url, allow_redirects=True)
        if response.status_code == 200:
            link = response.url
            return templates.TemplateResponse(
                "index.html",
                context={
                    "request": request,
                    "final_text": ALERTS_TEMPLATES["success"].format(link, link, link),
                },
            )
        else:
            return templates.TemplateResponse(
                "index.html",
                context={
                    "request": request,
                    "final_text": ALERTS_TEMPLATES["error"].format(
                        f"Status Code: {response.status_code}"
                    ),
                },
            )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            context={
                "request": request,
                "final_text": ALERTS_TEMPLATES["error"].format(e),
            },
        )
