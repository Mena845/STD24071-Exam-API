from fastapi import FastAPI, Request, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse, PlainTextResponse, JSONResponse
import base64;

app = FastAPI()

# Q1
@app.get("/ping")
def ping():
    return "pong"

# Q2
@app.get("/home")
def home():
    html_content = """
    <html>
            <h1>Welcome home!</h1>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# Q3

@app.exception_handler(StarletteHTTPException)
async  def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return HTMLResponse(
            content="""
            <html>
                <body><h1>404 NOT FOUND</h1></body>
            </html>
            """,
            status_code=404,
        )
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Q4

class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime
posts_db = []
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(new_posts: List[Post]):
    posts_db.extend(new_posts)
    return posts_db

# Q5
posts_db: List[Post] = []
@app.get("/posts", response_model=List[Post])
def get_posts():
    return posts_db

# Q6
@app.put("/posts", response_model=List[Post])
def update_or_add_posts(new_posts: List[Post]):
    for new_post in new_posts:
        for i, post in enumerate(posts_db):
            if post.title == new_post.title:
                posts_db[i] = new_post
                break
        else:
            posts_db.append(new_post)
    return posts_db


# bonus
@app.get("/ping")
def ping():
    return "pong"

@app.get("/ping/auth")
def ping_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Non autorisé")

    encoded_credentials = auth_header.split(" ")[1]

    try:
        decoded_bytes = base64.b64decode(encoded_credentials)
        decoded_str = decoded_bytes.decode("utf-8")
        username, password = decoded_str.split(":", 1)
    except Exception:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    if username == "admin" and password == "123456":
        return PlainTextResponse(content="pong")
    else:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

