from fastapi import status

from app.exceptions.api_exception import APIException


class InvalidAttractionID(APIException):

    def __init__(self):
        super().__init__(
            detail="Invalid attraction ID", error_code=status.HTTP_400_BAD_REQUEST
        )


class AttractionNotFound(APIException):

    def __init__(self):
        super().__init__(
            detail="The requested attraction does not exist",
            error_code=status.HTTP_400_BAD_REQUEST,
        )


class PlanNotFound(APIException):

    def __init__(self):
        super().__init__(
            detail="The requested plan does not exist",
            error_code=status.HTTP_400_BAD_REQUEST,
        )
