from server.apps.core.models import CoreModel


class InheritedModel(CoreModel):
    """Inherited model."""

    class Meta(CoreModel.Meta):
        """Meta."""

        verbose_name = "Object"
