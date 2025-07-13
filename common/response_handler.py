from rest_framework.response import Response
from rest_framework import status


class ResponseHandler:
    
    @staticmethod
    def handle_200_success(response):
        """
        Handle 200 success reponse.
        """
        return Response(response, status=status.HTTP_200_OK)
    
    @staticmethod
    def handle_400_error(response):
        """
        Handle 400 Bad Request error response.
        """
        return Response({
            'error': str(response) if response else '400 Bad Request: The request could not be understood or was missing required parameters.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def handle_404_error():
        """
        Handle 404 Not Found error response.
        """
        return Response({
            'error': '404 Not Found: The specified resource is not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def handle_403_error():
        """
        Handle 403 Permission Denied error.
        """
        return Response({
            'error': '403 Permission Denied: No permission to access the resource.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def handle_401_error():
        """
        Handle 401 Unauthorized error response.
        """
        return Response({
            'error': '401 Unauthorized: Authorization information is missing or invalid.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def handle_500_error(request, exception):
        """
        Handle 500 Internal Server Error response.
        """
        # Log error details
        error_log = {
            'method': request.method,
            'url': request.get_full_path(),
            'params': request.query_params,
            'post': request.data,
            'error': str(exception),
            'stack': str(exception.__traceback__)
        }
        
        print(error_log)
        
        return Response({
            'error': '500 Internal Server Error: Something went wrong. Please contact the support team.',
            'log': error_log
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)