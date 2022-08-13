from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.utils.datetime_safe import datetime


class Category(models.Model):
    username = models.ForeignKey('accounts.Accounts', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, verbose_name='اسم الفئة')
    description = models.CharField(max_length=128, verbose_name='وصف الفئة')

    def __str__(self):
        return self.name
    class Meta:
        ordering = ("name",)

class Medicine(models.Model):
    name = models.CharField(max_length=32, verbose_name='اسم الدواء')
    username = models.ForeignKey('accounts.Accounts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name='فئة الدواء')
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name='سعر الدواء')
    quantity = models.PositiveIntegerField(default=0, verbose_name='كمية الدواء')
    notes = models.TextField(max_length=1024, blank=True, verbose_name='ملاحظات عن الدواء')
    start_date = models.DateField(default=datetime.now, verbose_name='تاريخ بداية الصلاحية')
    end_date = models.DateField(default=datetime.now, verbose_name='تاريخ نهاية الصلاحية')

    class Meta:
        ordering = ("name",)


class Payment(models.Model):
    username = models.ForeignKey('accounts.Accounts', on_delete=models.CASCADE)
    data = models.TextField(max_length=1024, verbose_name='بيانات الفاتورة')
    date = models.DateTimeField(default=timezone.now, verbose_name='تاريخ الفاتورة')
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name='اجمالي الفاتورة')

    class Meta:
        ordering = ("-id",)


class Items(models.Model):
    username = models.ForeignKey('accounts.Accounts', on_delete=models.CASCADE)
    data = models.TextField(max_length=1024)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)


class Settings(models.Model):
    username = models.OneToOneField('accounts.Accounts', on_delete=models.CASCADE)
    days = models.IntegerField(default=30, verbose_name='عدد الأيام لأضافة الدواء لقائمة الأدوية الي اقتربت صلاحيتها من الانتهاء')
    qty = models.IntegerField(default=10, verbose_name='أقل قيمة لاضافة الدواء لقائمة النواقص')





















