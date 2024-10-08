import logging

import uvicorn
from fastapi import FastAPI
from posts.router import router as post_router
from auth.router import router as auth_router
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

app.include_router(post_router)
app.include_router(auth_router)
app.include_router(sub_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
