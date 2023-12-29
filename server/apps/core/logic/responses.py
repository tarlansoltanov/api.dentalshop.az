from drf_yasg import openapi

UNAUTHORIZED = openapi.Response(
    description="Authentication failed. Check your credentials.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Error message",
            ),
            "code": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Error code",
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
