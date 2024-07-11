import logging
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

logger = logging.getLogger(__name__)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
        logger.info(f"Пароль установлен для пользователя {self.email}")

    def check_password(self, raw_password):
        is_correct = check_password(raw_password, self.password)
        if not is_correct:
            logger.warning(f"Неудачная попытка входа для пользователя {self.email}")
        return is_correct
