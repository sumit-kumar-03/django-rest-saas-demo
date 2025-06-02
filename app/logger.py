import logging


def setup_custom_logger():

    # log formate
    formatter = logging.Formatter(
        fmt=(
            "%(levelname)s | %(asctime)s | Process: %(process)d | Thread: %(threadName)s | "
            "Module: %(module)s | File: %(filename)s | Function: %(funcName)s | Line: %(lineno)d | "
            "Message: %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # logger setup  and logging level set to DEBUG it can adjust accordingly
    logger = logging.getLogger("TRI Orchestrator Logger !!!")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


logger = setup_custom_logger()
logger.info("Logger set up successfully")
