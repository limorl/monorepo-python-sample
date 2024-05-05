import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    if len(logger.handlers) > 0:
        # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
        # `.basicConfig` does not execute. Thus we set the level directly.
        logger.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)
    return logger
