from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_basic_type
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import Direction


class ImageFieldSchema(OpenApiSerializerFieldExtension):
    target_class = "server.apps.core.logic.fields.ImageField"

    def map_serializer_field(self, auto_schema: AutoSchema, direction: Direction):
        if direction == "response":
            return build_basic_type(OpenApiTypes.STR)

        return auto_schema._map_serializer_field(self.target, direction, bypass_extensions=True)
