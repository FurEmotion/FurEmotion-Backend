import os
from dotenv import load_dotenv
from typing import Optional

from constants.path import PROJECT_DIR


class Env:
    def __init__(self):
        load_dotenv(os.path.join(PROJECT_DIR, ".env"))

    def get(self, key: str) -> Optional[str]:
        return os.environ.get(key)


env = Env()
