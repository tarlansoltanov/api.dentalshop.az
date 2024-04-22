import pytest
from django.db import connection
from django.utils import timezone
from freezegun import freeze_time

from server.apps.core.models import OrderableModel, SlugModel, TimeStampedModel


@pytest.fixture(scope="class")
def inherited_model(core_model):
    """Inherited model."""

    class InheritedModel(core_model):
        """Inherited model."""

        class Meta(core_model.Meta):
            verbose_name = "Object"
            db_table = f"inherited_model_{core_model._meta.db_table}"

    return InheritedModel


@pytest.fixture
def inherited_model_with_table(transactional_db, inherited_model):
    """Inherited model with table."""
    if inherited_model._meta.db_table in connection.introspection.table_names():
        return inherited_model

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(inherited_model)

    return inherited_model


class TestTimeStampedModel:
    """Test TimeStampedModel."""

    @pytest.fixture(scope="class")
    def core_model(self):
        """Core model fixture."""
        return TimeStampedModel

    def test_model_name(self, inherited_model, core_model):
        """Test if InheritedModel name is correct."""
        assert inherited_model._meta.db_table == f"inherited_model_{core_model._meta.db_table}"

    def test_model_is_abstract(self, core_model):
        """Test if TimeStampedModel is abstract."""
        assert core_model._meta.abstract is True

    def test_inherited_model_is_subclass_of_model(self, inherited_model, core_model):
        """Test if InheritedModel is subclass of TimeStampedModel."""
        assert issubclass(inherited_model, core_model) is True

    def test_inherited_model_is_not_abstract(self, inherited_model):
        """Test if InheritedModel is not abstract."""
        assert inherited_model._meta.abstract is False

    def test_inherited_model_created_at(self, inherited_model):
        """Test if created_at is in InheritedModel."""
        assert hasattr(inherited_model, "created_at") is True

    def test_inherited_model_created_at_sets_on_creation(self, inherited_model_with_table):
        """Test if created_at sets on creation."""
        obj = inherited_model_with_table.objects.create()
        assert obj.created_at is not None

    def test_inherited_model_updated_at(self, inherited_model):
        """Test if updated_at is in InheritedModel."""
        assert hasattr(inherited_model, "updated_at") is True

    def test_inherited_model_updated_at_updates_on_save(self, inherited_model_with_table):
        """Test if updated_at updates on save."""
        instance = inherited_model_with_table.objects.create()
        updated_at = instance.updated_at

        with freeze_time(timezone.now() + timezone.timedelta(days=1)):
            instance.save()

        assert instance.updated_at > updated_at

    def test_inherited_model_ordering(self, inherited_model_with_table):
        """Test if the ordering is correct."""
        inherited_model_with_table.objects.create()

        with freeze_time(timezone.now() + timezone.timedelta(days=1)):
            inherited_model_with_table.objects.create()

        objects = inherited_model_with_table.objects.all()
        assert objects[0].updated_at > objects[1].updated_at


class TestOrderableModel:
    """Test OrderableModel."""

    @pytest.fixture(scope="class")
    def core_model(self):
        """Core model fixture."""
        return OrderableModel

    def test_model_name(self, inherited_model, core_model):
        """Test if InheritedModel name is correct."""
        assert inherited_model._meta.db_table == f"inherited_model_{core_model._meta.db_table}"

    def test_model_is_abstract(self, core_model):
        """Test if OrderableModel is abstract."""
        assert core_model._meta.abstract is True

    def test_inherited_model_is_subclass_of_model(self, inherited_model, core_model):
        """Test if InheritedModel is subclass of OrderableModel."""
        assert issubclass(inherited_model, core_model) is True

    def test_inherited_model_is_not_abstract(self, inherited_model):
        """Test if InheritedModel is not abstract."""
        assert inherited_model._meta.abstract is False

    def test_inherited_model_position(self, inherited_model):
        """Test if position is in InheritedModel."""
        assert hasattr(inherited_model, "position") is True

    def test_inherited_model_ordering(self, inherited_model_with_table):
        """Test if the ordering is correct."""
        o1 = inherited_model_with_table.objects.create(position=1)
        o2 = inherited_model_with_table.objects.create(position=2)
        o3 = inherited_model_with_table.objects.create()

        objects = inherited_model_with_table.objects.all()

        assert objects[0] == o1
        assert objects[1] == o2
        assert objects[2] == o3


class TestSlugModel:
    """Test SlugModel."""

    @pytest.fixture(scope="class")
    def core_model(self):
        """Core model fixture."""
        return SlugModel

    def test_model_name(self, inherited_model, core_model):
        """Test if InheritedModel name is correct."""
        assert inherited_model._meta.db_table == f"inherited_model_{core_model._meta.db_table}"

    def test_model_is_abstract(self, core_model):
        """Test if SlugModel is abstract."""
        assert core_model._meta.abstract is True

    def test_inherited_model_is_subclass_of_model(self, inherited_model, core_model):
        """Test if InheritedModel is subclass of SlugModel."""
        assert issubclass(inherited_model, core_model) is True

    def test_inherited_model_is_not_abstract(self, inherited_model):
        """Test if InheritedModel is not abstract."""
        assert inherited_model._meta.abstract is False

    def test_inherited_model_slug(self, inherited_model):
        """Test if slug is in InheritedModel."""
        assert hasattr(inherited_model, "slug") is True

    def test_inherited_model_slug_generation_exception(self, inherited_model):
        """Test if generate_slug raises an exception."""
        instance = inherited_model()

        with pytest.raises(NotImplementedError):
            instance.save()

    def test_inherited_model_slug_generation(self, inherited_model_with_table):
        """Test if generate_slug generates a slug."""

        class TestSlugModel(inherited_model_with_table):
            """Test slug model."""

            def generate_slug(self):
                """Generate slug."""
                return "slug"

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestSlugModel)

        instance = TestSlugModel()
        instance.save()

        assert instance.slug == "slug"
