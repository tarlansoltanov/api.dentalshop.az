import factory

from server.apps.category.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    is_main = factory.Faker("boolean")
    parent = factory.Maybe(
        factory.LazyAttribute(lambda n: not n.is_main),
        factory.SubFactory(
            "server.apps.category.tests.factories.CategoryFactory",
            is_main=True,
        ),
    )
