# apis/cry.py
from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime

from auth.auth_bearer import JWTBearer
from services.cry import cry_service
from schemas.cry import *
from db import get_db_session
from error.exceptions import *
from error.handler import handle_http_exceptions

router = APIRouter(
    prefix="/cry",
    tags=["cry"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreateCryOutput)
@handle_http_exceptions
async def create_cry_endpoint(
        create_cry_input: CreateCryInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreateCryOutput:
    cry = await cry_service.create_cry(db, create_cry_input, user_id).to_korean()
    return CreateCryOutput(cry=cry, success=True, message="Cry created successfully")


@router.get("/cry/{cry_id}", dependencies=[Depends(JWTBearer())], response_model=GetCryOutput)
@handle_http_exceptions
def get_cry_endpoint(
        cry_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetCryOutput:
    cry = cry_service.get_cry_by_id(db, cry_id, user_id).to_korean()
    return GetCryOutput(cry=cry, success=True, message="Cry fetched successfully")


@router.get("/pet/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=GetPetCriesOutput)
@handle_http_exceptions
def get_pet_cries_endpoint(
        pet_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetPetCriesOutput:
    cries = cry_service.get_all_cries_by_pet(db, pet_id, user_id)
    for i in range(len(cries)):
        cries[i] = cries[i].to_korean()
    return GetPetCriesOutput(cries=cries, success=True, message="Cries fetched successfully")


@router.get("/search/state", dependencies=[Depends(JWTBearer())], response_model=GetCriesWithStateOutput)
@handle_http_exceptions
def get_pets_with_state_endpoint(
        pet_id: int = Query(..., description="ID of the pet"),
        query_state: str = Query(..., description="State to filter cries"),
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetCriesWithStateOutput:
    cries = cry_service.get_pets_with_state(
        db, pet_id, query_state, user_id)
    for i in range(len(cries)):
        cries[i] = cries[i].to_korean()
    return GetCriesWithStateOutput(cries=cries, success=True, message="Cries fetched successfully")


@router.get("/search/time", dependencies=[Depends(JWTBearer())], response_model=GetCriesBetweenTimeOutput)
@handle_http_exceptions
def get_pets_between_time_endpoint(
        pet_id: int = Query(..., description="ID of the pet"),
        start_time: datetime = Query(...,
                                     description="Start time in ISO format"),
        end_time: datetime = Query(..., description="End time in ISO format"),
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetCriesBetweenTimeOutput:
    cries = cry_service.get_pets_between_time(
        db, pet_id, start_time, end_time, user_id)
    for i in range(len(cries)):
        cries[i] = cries[i].to_korean()
    return GetCriesBetweenTimeOutput(cries=cries, success=True, message="Cries fetched successfully")


@router.get("/inspect", dependencies=[Depends(JWTBearer())])
@handle_http_exceptions
def inspect_cry_endpoint(
        pet_id: int = Query(..., description="ID of the pet"),
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())):
    inspect_result = cry_service.inspect_cry(db, pet_id, user_id)
    return {"success": True, "message": "Cry inspected successfully", "result": inspect_result}


@router.post("/predict", dependencies=[Depends(JWTBearer())])
@handle_http_exceptions
async def predict_cry_endpoint(
        file: UploadFile = File(...),
        pet_id: int = Query(..., description="ID of the pet"),
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> PredictCryOutput:
    if file == None or not file.filename.endswith(".wav"):
        raise WavFileNotFoundError("Wav file not found")
    cry = await cry_service.predict_cry(db, file, pet_id, user_id)
    return PredictCryOutput(cry=cry, success=True, message="Cry predicted successfully")


@router.put("/{cry_id}", dependencies=[Depends(JWTBearer())], response_model=UpdateCryOutput)
@handle_http_exceptions
def update_cry_endpoint(
        cry_id: int,
        update_cry_input: UpdateCryInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateCryOutput:
    cry = cry_service.update_cry(
        db, cry_id, update_cry_input, user_id).to_korean()
    return UpdateCryOutput(cry=cry, success=True, message="Cry updated successfully")


@router.delete("/{cry_id}", dependencies=[Depends(JWTBearer())], response_model=DeleteCryOutput)
@handle_http_exceptions
def delete_cry_endpoint(
        cry_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteCryOutput:
    cry_service.delete_cry(db, cry_id, user_id)
    return DeleteCryOutput(success=True, message="Cry deleted successfully")
