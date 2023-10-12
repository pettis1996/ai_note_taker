# FastAPI 
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """

@app.get("/home", response_class=RedirectResponse)
async def redirect_homepage():
    return RedirectResponse("/")

@app.get("/main", response_class=FileResponse)
async def home_from_file():
    return FileResponse("./index.html")

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}