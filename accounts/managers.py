from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, full_name, password):
        if not email:
            raise ValueError('User must have an email')

        if not phone_number:
            raise ValueError('User must have an phone number')

        if not full_name:
            raise ValueError('User must have a full name')

        user = self.model(email=self.normalize_email(email), phone_number=phone_number, full_name=full_name)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, phone_number, full_name, password):
        user = self.create_user(email, phone_number, full_name, password)
        user.is_admin = True
        user.save(using=self.db)
        return user