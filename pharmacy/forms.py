from .models import Medicine, Category, Payment, Items, Settings
from django import forms
from django.utils.datetime_safe import datetime

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')

class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')

class AddMedicineForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.now,
                                     widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="تاريخ بداية الصلاحية")

    end_date = forms.DateField(initial=datetime.now,
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="تاريخ نهاية الصلاحية")

    class Meta:
        model = Medicine
        fields = ('name', 'category', 'price', 'quantity', 'notes', 'start_date', 'end_date')

    def __init__(self, user, *args, **kwargs):
        super(AddMedicineForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(username=user)



class UpdateMedicineForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.now,
                                     widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="تاريخ بداية الصلاحية")

    end_date = forms.DateField(initial=datetime.now,
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="تاريخ نهاية الصلاحية")

    class Meta:
        model = Medicine
        fields = ('name', 'category', 'price', 'quantity', 'notes', 'start_date', 'end_date')

    def __init__(self, user, *args, **kwargs):
        super(UpdateMedicineForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(username=user)


class NewPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('date',)

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        exclude = ('data', 'username', 'total')

class AddPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('data','date','total')

class UpdatePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('date','total')

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('days','qty')