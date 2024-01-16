import factory

from server.apps.category.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    parent = None
