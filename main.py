import uvicorn
from fastapi import FastAPI
import logging
import logging.config
import os
from datetime import datetime

from db import SessionLocal, get_db_session
from apis import router as main_router
from apis.user import router as user_router
from apis.cry import router as cry_router
from apis.pet import router as pet_router

# 로깅 설정 파일 경로 지정 (절대 경로 사용을 권장)
LOGGING_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'logging.conf')

# logs 디렉토리가 없으면 생성
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 로깅 설정 로드
try:
    logging.config.fileConfig(
        LOGGING_CONFIG_FILE, disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.debug("Logging is configured successfully.")
except Exception as e:
    print(f"Failed to configure logging: {e}")

app = FastAPI()

app.include_router(main_router)
app.include_router(user_router)
app.include_router(cry_router)
app.include_router(pet_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7701)
# uvicorn main:app --host 0.0.0.0 --port 7701 --reload
