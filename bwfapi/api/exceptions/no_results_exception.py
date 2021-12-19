from fastapi import HTTPException

class NoResultsException(HTTPException):
    pass