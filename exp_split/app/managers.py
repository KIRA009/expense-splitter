from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_details):
        """
        Creates and saves a User with the given contact, password, name, gender, location_id
        """

        extra_details['is_superuser'] = False

        user = self.model(email=email, **extra_details)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_details):
        """
        Creates and saves a user with the given email, password
        """

        extra_details['is_superuser'] = True

        user = self.model(email=email, **extra_details)
        user.set_password(password)
        user.save(using=self._db)
        return user
