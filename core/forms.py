from django import forms
from core.models import Student
from .models import Transaction, Product


class TransactionCreationForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('product', 'quantity', 'bought_by')

    def clean(self):
        enrollment_no = self.cleaned_data.get('bought_by')
        product = Product.objects.get(name=self.cleaned_data.get('product'))
        quantity = self.cleaned_data.get('quantity')
        student = Student.objects.get(enrollment_no=enrollment_no)

        total_amount = product.amount * quantity

        if student.tokens < total_amount:
            raise forms.ValidationError("Student doesn't has enough money to buy")

        self.cleaned_data['amount'] = product.amount
        self.cleaned_data['total_amount'] = total_amount

        return self.cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.amount = self.cleaned_data['amount']

        student = obj.bought_by
        student.tokens -= self.cleaned_data['total_amount']

        if commit:
            obj.save()
            student.save()

        return obj


class TransactionChangeForm(forms.ModelForm):
    total_amount = forms.DecimalField(max_digits=7, decimal_places=2, disabled=True)

    class Meta:
        model = Transaction
        fields = ('product', 'quantity', 'bought_by', 'total_amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.initial['total_amount'] = self.instance.get_total_amount()
