import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from posts.router import router as post_router
from user.router import router as auth_router
from subscriber.router import router as sub_router
import betterlogging as bl


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting server")


setup_logging()

app = FastAPI(title="Trading App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(auth_router)
app.include_router(sub_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
