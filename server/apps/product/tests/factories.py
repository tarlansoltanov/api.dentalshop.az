import factory

from server.apps.product.models import Product, ProductImage, ProductNote


class ProductNoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductNote

    text = factory.Faker("sentence")


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    image = factory.django.ImageField()
    product = factory.SubFactory("server.apps.product.tests.factories.ProductFactory")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    code = factory.Faker("ean13")
    name = factory.Faker("sentence")
    brand = factory.SubFactory("server.apps.brand.tests.factories.BrandFactory")
    category = factory.SubFactory("server.apps.category.tests.factories.CategoryFactory", is_main=True)
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    discount = factory.Faker("pyint", min_value=0, max_value=100)
    in_stock = factory.Faker("pybool")
    is_distributer = factory.Faker("pybool")
    main_note = factory.Faker("sentence")
    description = factory.Faker("paragraph")
