from drf_yasg import openapi

ERROR_SCHEMA = openapi.Schema(
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
)

BAD_REQUEST = openapi.Response(
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

UNAUTHORIZED = openapi.Response(
    description="Authentication failed. Check your credentials.",
    schema=ERROR_SCHEMA,
)

FORBIDDEN = openapi.Response(
    description="You don't have permission to perform this action.",
    schema=ERROR_SCHEMA,
)

NOT_FOUND = openapi.Response(
    description="The requested resource was not found.",
    schema=ERROR_SCHEMA,
)
