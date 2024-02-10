from drf_spectacular.utils import OpenApiResponse

from server.apps.core.logic.serializers import BadRequestSerializer, ErrorSerializer

BAD_REQUEST = OpenApiResponse(
    description="The request data was invalid.",
    response=BadRequestSerializer,
)

UNAUTHORIZED = OpenApiResponse(
    description="Authentication failed. Check your credentials.",
    response=ErrorSerializer,
)

FORBIDDEN = OpenApiResponse(
    description="You don't have permission to perform this action.",
    response=ErrorSerializer,
)

NOT_FOUND = OpenApiResponse(
    description="The requested resource was not found.",
    response=ErrorSerializer,
)
