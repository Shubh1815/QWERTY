from django.urls import path
from .views import dashboard, products, profile

app_name = 'manager'

urlpatterns = [
    path('<int:category>/', dashboard, name="dashboard"),
    path('profile/', profile, name="profile"),
    path('products/<int:category>/', products, name="products")
]
