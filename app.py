from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests, re


app = FastAPI()

templates = Jinja2Templates(directory="templates/", autoescape=False)

ALERTS_TEMPLATES = {
    "error": """<div
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
        role="alert"
      >
        <strong class="font-bold">Error Encountered!</strong>
        <span class="block sm:inline">{}</span>
        <span class="absolute top-0 bottom-0 right-0 px-4 py-3">
          <svg
            class="fill-current h-6 w-6 text-red-500"
            role="button"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
          >
            <title>Close</title>
          </svg>
        </span>
      </div>""",
    "success": """<div
        class="bg-green-100 rounded-lg py-5 px-6 mb-3 text-base text-green-700 inline-flex items-center w-full"
        role="alert"
      >
        <svg
          aria-hidden="true"
          focusable="false"
          data-prefix="fas"
          data-icon="check-circle"
          class="w-4 h-4 mr-2 fill-current"
          role="img"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 512 512"
        >
          <path
            fill="currentColor"
            d="M504 256c0 136.967-111.033 248-248 248S8 392.967 8 256 119.033 8 256 8s248 111.033 248 248zM227.314 387.314l184-184c6.248-6.248 6.248-16.379 0-22.627l-22.627-22.627c-6.248-6.249-16.379-6.249-22.628 0L216 308.118l-70.059-70.059c-6.248-6.248-16.379-6.248-22.628 0l-22.627 22.627c-6.248 6.248-6.248 16.379 0 22.627l104 104c6.249 6.249 16.379 6.249 22.628.001z"
          ></path>
        </svg>
        Success - UnShortened
        <a href="{}" class="font-bold text-green-800">&nbsp; Link</a>
      </div>

      <div
        class="bg-indigo-100 rounded-lg py-2 px-6 text-indigo-700 flex items-center"
        role="alert"
      >
      <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="chevron-circle-right" class="w-4 h-4 mr-2 fill-current" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
    <path fill="currentColor" d="M256 8c137 0 248 111 248 248S393 504 256 504 8 393 8 256 119 8 256 8zm113.9 231L234.4 103.5c-9.4-9.4-24.6-9.4-33.9 0l-17 17c-9.4 9.4-9.4 24.6 0 33.9L285.1 256 183.5 357.6c-9.4 9.4-9.4 24.6 0 33.9l17 17c9.4 9.4 24.6 9.4 33.9 0L369.9 273c9.4-9.4 9.4-24.6 0-34z"></path>
  </svg>
       <a href="{}" > {}</a>
       
      </div>
      """,
}


@app.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/", response_class=HTMLResponse)
def unshorten(request: Request, url: str = Form("")):
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
