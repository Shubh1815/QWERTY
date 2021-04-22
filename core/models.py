from django.db import models
from django.shortcuts import get_object_or_404
from users.models import Student
from datetime import date


class TransactionManager(models.Manager):
    def get_student_transactions(self, student, params):

        qs = self.filter(bought_by=student)

        qs = qs.filter(product__category=params.get('category', 0))
        qs = qs.filter(date=params.get('date', date.today()))

        return qs


class Product(models.Model):
    CANTEEN = 0
    STATIONARY = 1
    TRANSPORTATION = 2

    CATEGORY_CHOICES = [
        (CANTEEN, 'Canteen'),
        (STATIONARY, 'Stationary'),
        (TRANSPORTATION, 'Transportation')
    ]

    name = models.CharField(max_length=50, primary_key=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.IntegerField(choices=CATEGORY_CHOICES)

    def amount_display(self):
        return f"Rs. {self.amount}"

    def __str__(self):
        return self.name


class Calorie(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="calorie")
    calories = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.product.name


class CanteenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product__category=Product.CANTEEN)


class StationaryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product__category=Product.STATIONARY)


class TransportationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product__category=Product.TRANSPORTATION)


class Transaction(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='transaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    bought_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    objects = TransactionManager()

    canteen = CanteenManager()
    stationary = StationaryManager()
    transportation = TransportationManager()

    @classmethod
    def process_transactions(cls, data):
        enrollment_no = data['enrollment_no']
        total_amount = data['total_amount']
        selected_products = data['selected']

        student = get_object_or_404(Student, enrollment_no=enrollment_no)

        if student.tokens < total_amount:
            return False

        for product in selected_products:
            p = Product.objects.get(name__iexact=product['name'])

            cls.objects.create(
                product=p,
                amount=p.amount,
                quantity=product['quantity'],
                bought_by=student,
            ).save()

        student.tokens -= total_amount
        student.save()

        return True

    def get_total_amount(self):
        return self.amount * self.quantity

    def __str__(self):
        return str(self.id)
