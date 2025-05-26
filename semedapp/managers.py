from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, cpf=None, first_name=None, last_name=None, password=None, **extra_fields):
        if not username:
            raise ValueError("O campo username é obrigatório")
        if not cpf:
            raise ValueError("O campo CPF é obrigatório")
        if not first_name:
            raise ValueError("O campo nome é obrigatório")
        if not last_name:
            raise ValueError("O campo sobrenome é obrigatório")

        user = self.model(
            username=username,
            cpf=cpf,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, cpf=None, first_name=None, last_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser deve ter is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self.create_user(username, cpf, first_name, last_name, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)
