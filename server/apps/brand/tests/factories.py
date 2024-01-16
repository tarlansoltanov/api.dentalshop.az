import factory

from server.apps.brand.models import Brand


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker("company")
    photo = factory.django.ImageField()
    is_main = False
