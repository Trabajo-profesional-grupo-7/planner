from fastapi import HTTPException, status


class APIException(HTTPException):
    error_code: status
    detail: str

    def __init__(self, error_code, detail):
        self.error_code = error_code
        self.detail = detail

    def __str__(self):
        return f"{self.__class__.__name__}(status_code={self.error_code}, detail={self.detail})"
