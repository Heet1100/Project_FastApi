from http import HTTPStatus

from fastapi import APIRouter, status

healthcheck_router = APIRouter(tags=["Health Check"])


@healthcheck_router.get("/healthcheck", status_code=status.HTTP_200_OK)
def healthcheck():
    return status.HTTP_200_OK
