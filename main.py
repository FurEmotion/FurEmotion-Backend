import uvicorn
from fastapi import FastAPI
import logging
import logging.config

from db import SessionLocal, get_db_session
from apis import router as main_router
from apis.user import router as user_router
from apis.cry import router as cry_router
from apis.pet import router as pet_router

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI()

app.include_router(main_router)
app.include_router(user_router)
app.include_router(cry_router)
app.include_router(pet_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7701)
# uvicorn main:app --host 0.0.0.0 --port 7701 --reload
