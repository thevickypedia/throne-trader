import logging


def default_logger() -> logging.Logger:
    """Generates a default console logger.

    Returns:
        logging.Logger:
        Logger object.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        fmt=logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - [%(processName)s:%(module)s:%(lineno)d] - %(funcName)s - %(message)s'
        )
    )
    logger.addHandler(hdlr=handler)
    return logger
