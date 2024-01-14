import factory

from server.apps.product.models import ProductNote


class ProductNoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductNote

    text = factory.Faker("sentence")
