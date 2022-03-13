from django.db import models


class ReferenceBook(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    short_name = models.CharField(max_length=25, verbose_name='Короткое наименование', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    version = models.CharField(max_length=5, verbose_name='Версия')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала действия справочника этой версии')

    def __str__(self):
        return f'{self.name} | {self.version}'

    class Meta:
        unique_together = ('name', 'version')
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'


class ReferenceBookElement(models.Model):
    reference_book = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='elements')
    code = models.CharField(max_length=100, verbose_name='Код элемента')
    value = models.CharField(max_length=10, verbose_name='Значение')

    def __str__(self):
        return f'code: {self.code} | value: {self.value}'

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
