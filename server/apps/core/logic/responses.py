from drf_yasg import openapi

TOKEN_NOT_VALID = openapi.Response(
    description="Token is invalid or expired",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Error message",
                example="Token is invalid or expired",
            ),
            "code": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Error code",
                example="token_not_valid",
            ),
        },
    ),
)

INVALID_REQUEST_DATA = openapi.Response(
    description="The request data was invalid.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "field_name": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="List of errors for the field.",
            ),
        },
    ),
)
