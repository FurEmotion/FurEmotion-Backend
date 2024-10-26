# error/handler.py
from fastapi import HTTPException
from typing import Any, Callable
import functools
import asyncio
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from error.exceptions import *
from log import logger


def handle_http_exceptions(func: Callable) -> Callable:

    # 비동기 함수용 래퍼 함수
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        try:
            logger.info(
                f"Calling async function: {func.__name__} with args: {args}, kwargs: {kwargs}")
            result = await func(*args, **kwargs)
            logger.info(
                f"Async function {func.__name__} executed successfully")
            return result
        except (ValidationError, NegativeAgeError, InvalidSpeciesError,
                DuplicateUidError, DuplicateEmailError, WrongCryOfSpeciesError, WavFileNotFoundError) as ve:
            logger.error(f"400 Bad Request: {str(ve)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
        except (UnauthorizedError, WrongFileTypeError) as ue:
            logger.error(f"403 Forbidden: {str(ue)}", exc_info=True)
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(ue))
        except (PetNotFoundError, CryNotFoundError, UserNotFoundError) as pnfe:
            logger.error(f"404 Not Found: {str(pnfe)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=str(pnfe))
        except Exception as e:
            logger.error(f"500 Internal Server Error: {e}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    # 동기 함수용 래퍼 함수
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        try:
            logger.info(
                f"Calling sync function: {func.__name__} with args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Sync function {func.__name__} executed successfully")
            return result
        except (ValidationError, NegativeAgeError, InvalidSpeciesError,
                DuplicateUidError, DuplicateEmailError, WrongCryOfSpeciesError) as ve:
            logger.error(f"400 Bad Request: {str(ve)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
        except (UnauthorizedError, WrongFileTypeError) as ue:
            logger.error(f"403 Forbidden: {str(ue)}", exc_info=True)
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(ue))
        except (PetNotFoundError, CryNotFoundError, UserNotFoundError) as pnfe:
            logger.error(f"404 Not Found: {str(pnfe)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=str(pnfe))
        except Exception as e:
            logger.error(f"500 Internal Server Error: {e}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    # 함수가 비동기인지 동기인지에 따라 적절한 래퍼를 반환
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
