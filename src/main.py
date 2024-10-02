import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from posts.router import router as post_router
from auth.router import router as auth_router

app = FastAPI(
    title="Trading App"
)

#app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(post_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)