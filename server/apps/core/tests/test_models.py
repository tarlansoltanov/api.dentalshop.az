import pytest
from django.utils import timezone
from freezegun import freeze_time

from server.apps.core.models import CoreModel
from server.apps.core.tests.models import InheritedModel

pytestmark = pytest.mark.django_db


class TestCoreModel:
    """Test CoreModel."""

    @pytest.fixture(scope="class")
    def core_model(self):
        """Core model."""
        return CoreModel

    @pytest.fixture(scope="class")
    def inherited_model(self):
        """Inherited model."""
        return InheritedModel

    def test_model_name(self, inherited_model):
        """Test if InheritedModel name is correct."""
        assert inherited_model.__name__ == "InheritedModel"

    def test_core_model_is_abstract(self, core_model):
        """Test if CoreModel is abstract."""
        assert core_model._meta.abstract is True

    def test_inherited_model_is_subclass_of_core_model(self, inherited_model, core_model):
        """Test if InheritedModel is subclass of CoreModel."""
        assert issubclass(inherited_model, core_model) is True

    def test_inherited_model_is_not_abstract(self, inherited_model):
        """Test if InheritedModel is not abstract."""
        assert inherited_model._meta.abstract is False

    def test_inherited_model_created_at(self, inherited_model):
        """Test if created_at is in InheritedModel."""
        assert hasattr(inherited_model, "created_at") is True

    def test_inherited_model_created_at_sets_on_creation(self, inherited_model):
        """Test if created_at sets on creation."""
        obj = inherited_model.objects.create()
        assert obj.created_at is not None

    def test_inherited_model_updated_at(self, inherited_model):
        """Test if updated_at is in InheritedModel."""
        assert hasattr(inherited_model, "updated_at") is True

    def test_inherited_model_updated_at_updates_on_save(self, inherited_model):
        """Test if updated_at updates on save."""
        instance = inherited_model.objects.create()
        updated_at = instance.updated_at

        with freeze_time(timezone.now() + timezone.timedelta(days=1)):
            instance.save()

        assert instance.updated_at > updated_at

    def test_inherited_model_ordering(self, inherited_model):
        """Test if the ordering is correct."""
        inherited_model.objects.create()

        with freeze_time(timezone.now() + timezone.timedelta(days=1)):
            inherited_model.objects.create()

        objects = inherited_model.objects.all()
        assert objects[0].updated_at > objects[1].updated_at
