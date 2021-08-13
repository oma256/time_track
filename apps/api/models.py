from django.db import models
from django.core.cache import cache


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class VersionControl(SingletonModel):
    version = models.CharField(
        max_length=255, verbose_name="Версия приложения"
    )
    force_update = models.BooleanField(
        default=False, verbose_name="Принудительное обновление"
    )

    class Meta:
        verbose_name = "Управление версией приложения"
        verbose_name_plural = "Управление версиями приложения"

    def __str__(self):
        return self.version
