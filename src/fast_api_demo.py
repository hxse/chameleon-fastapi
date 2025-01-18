from typing import Union

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, HTMLResponse
import uvicorn

from pathlib import Path


app = FastAPI()


@app.get("/fig_data/{symbol}/{mode}/{period}/{file_name}", response_class=HTMLResponse)
async def read_items(symbol: str, mode: str, period: str, file_name: str):
    file_path = Path(f"/app/src/fig_data/{symbol}/{mode}/{period}/{file_name}")
    with open(file_path, "rb") as f:
        data = f.read()
    return data


@app.get("/")
def main():
    return {"Hello": "World"}


if __name__ == "__main__":
    print("run fast_api")
    uvicorn.run("fast_api_demo:app", host="0.0.0.0", port=2197)
