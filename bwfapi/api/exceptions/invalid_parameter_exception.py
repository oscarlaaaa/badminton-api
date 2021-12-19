from fastapi import HTTPException

class InvalidParameterException(HTTPException):
    pass