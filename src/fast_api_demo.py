from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
from bokeh.embed import server_document
from plot.bokeh_server import get_csv_list, get_route_name


import sys

dirPath = sys.argv[1]

templates = Jinja2Templates(directory="src/templates")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1:5006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/fig_data/{symbol}/{mode}/{period}/{file_name}", response_class=HTMLResponse)
async def read_items(symbol: str, mode: str, period: str, file_name: str):
    file_path = Path(f"/app/src/fig_data/{symbol}/{mode}/{period}/{file_name}")
    with open(file_path, "rb") as f:
        data = f.read()
    return data


@app.get("/bokeh/{name}")
async def get_bokeh(request: Request, name: str):
    bokeh_api = "http://127.0.0.1:5006"
    script = server_document(url=f"{bokeh_api}/{name}")
    return templates.TemplateResponse(
        "bokeh.html", {"request": request, "bokeh_script": script}
    )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    global dirPath
    arr = get_csv_list(dirPath)
    res = [get_route_name(i) for i in arr]
    url_arr = ["/bokeh" + "/" + i for i in res]
    return templates.TemplateResponse(
        "index.html", {"request": request, "url_arr": url_arr}
    )


if __name__ == "__main__":
    print("run fast_api")
    uvicorn.run("fast_api_demo:app", host="127.0.0.1", port=2197)
