"""TEMPLATE: logging configured once at startup. Use logger = logging.getLogger(__name__) in every module."""
import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        stream=sys.stdout,          # containers: log to stdout, the platform collects it
        force=True,                 # replace any handlers set by libraries
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)   # silence noisy libraries


if __name__ == "__main__":
    setup_logging()
    log = logging.getLogger(__name__)
    log.info("started")
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("calculation failed")   # .exception() includes the traceback
