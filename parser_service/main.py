import asyncio
import logging

import betterlogging as bl

from workers.hh.ParserHH import ParserHH
from workers.reporter.Reporter import Reporter


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting server")

async def main():
    reporter = Reporter()
    parser_hh = ParserHH(reporter=reporter)
    await asyncio.gather(parser_hh.start_pooling(), reporter.check_updates())


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
    #dev
