import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_PATH = PROJECT_ROOT / "app.log"


def init_logging():
    logging.basicConfig(
        filename=str(LOG_PATH),
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
        encoding="utf-8",
        filemode="w",
    )


logger = logging.getLogger(__name__)
