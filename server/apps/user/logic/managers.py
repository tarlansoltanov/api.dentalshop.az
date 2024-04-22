from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone is the unique identifiers for authentication.
    """

    def create_user(self, phone, password=None, **extra_fields):
        """
        Create and save a User with the given phone and password.

        :param:
            phone (str): User phone number.
            password (str): User password.
            **extra_fields: Extra fields.

        :return:
            User: User model instance.
        """

        if not phone:
            raise ValueError("The Phone field must be set")

        phone = self.normalize_email(phone)

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given phone and password.

        :param:
            phone (str): User phone number.
            password (str): User password.
            **extra_fields: Extra fields.

        :return:
            User: User model instance.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)
