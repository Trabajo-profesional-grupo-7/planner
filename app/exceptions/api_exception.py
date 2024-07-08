class APIException(Exception):
    error_code: str
    detail: str

    def __init__(self, error_code, detail):
        self.error_code = error_code
        self.detail = detail
