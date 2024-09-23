from rest_framework.response import Response
from rest_framework import status

def success_response(data=None, message="Operation successful", status_code=status.HTTP_200_OK):
    return Response({
        "status": "success",
        "message": message,
        "data": data
    }, status=status_code)

def error_response(message="An error occurred", status_code=status.HTTP_400_BAD_REQUEST, errors=None):
    return Response({
        "status": "error",
        "message": message,
        "errors": errors
    }, status=status_code)
