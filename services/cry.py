from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
import os
import re
import shutil
from uuid import uuid4
from datetime import datetime
import random


class CryService:
    def _init__(self, model):
        self.model = model
