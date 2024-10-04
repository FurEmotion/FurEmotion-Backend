# error/handler.py
import logging
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

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# HTTP 예외를 처리하는 데코레이터 함수 정의
def handle_http_exceptions(func: Callable) -> Callable:
    # 비동기 함수용 래퍼 함수 정의
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        try:
            # logger.info(
            #     f"Calling async function: {func.__name__} with args: {args}, kwargs: {kwargs}")
            # 원본 비동기 함수 실행
            result = await func(*args, **kwargs)
            # logger.info(
            #     f"Async function {func.__name__} executed successfully")
            return result
        except (ValidationError, NegativeAgeError, InvalidSpeciesError,
                DuplicateUidError, DuplicateEmailError) as ve:
            # 400 오류 처리 (잘못된 요청): 유효성 검사 오류 등
            logger.error(f"400 Bad Request: {str(ve)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
        except UnauthorizedError as ue:
            # 403 오류 처리 (권한 없음): 접근 권한이 없는 경우
            logger.error(f"403 Forbidden: {str(ue)}", exc_info=True)
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(ue))
        except (PetNotFoundError, CryNotFoundError, UserNotFoundError) as pnfe:
            # 404 오류 처리 (찾을 수 없음): 해당 리소스를 찾지 못한 경우
            logger.error(f"404 Not Found: {str(pnfe)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=str(pnfe))
        except Exception as e:
            # 500 오류 처리 (서버 내부 오류): 일반적인 예외 처리
            logger.error(f"500 Internal Server Error: {e}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    # 동기 함수용 래퍼 함수 정의
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        try:
            # logger.info(
            #     f"Calling sync function: {func.__name__} with args: {args}, kwargs: {kwargs}")
            # 원본 동기 함수 실행
            result = func(*args, **kwargs)
            # logger.info(f"Sync function {func.__name__} executed successfully")
            return result
        except (ValidationError, NegativeAgeError, InvalidSpeciesError,
                DuplicateUidError, DuplicateEmailError) as ve:
            # 400 오류 처리 (잘못된 요청): 유효성 검사 오류 등
            logger.error(f"400 Bad Request: {str(ve)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
        except UnauthorizedError as ue:
            # 403 오류 처리 (권한 없음): 접근 권한이 없는 경우
            logger.error(f"403 Forbidden: {str(ue)}", exc_info=True)
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(ue))
        except (PetNotFoundError, CryNotFoundError, UserNotFoundError) as pnfe:
            # 404 오류 처리 (찾을 수 없음): 해당 리소스를 찾지 못한 경우
            logger.error(f"404 Not Found: {str(pnfe)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=str(pnfe))
        except Exception as e:
            # 500 오류 처리 (서버 내부 오류): 일반적인 예외 처리
            logger.error(f"500 Internal Server Error: {e}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    # 함수가 비동기인지 동기인지에 따라 적절한 래퍼를 반환
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
