import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


def auth_middleware(get_response):
    def middleware(request):
        if request.path not in [
            "/register/",
            "/auth/login/",
        ]:
            # Renders request
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()

            token = request.COOKIES.get("jwt")

            if not token:
                # Checks is JWT token is present
                response.data = {"message": "No auth token"}
                return response
            try:
                # Checks if JWT token has expired
                jwt.decode(token, "secret", algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                response.data = {"message": "Expired auth token"}
                return response

        return get_response(request)

    return middleware
