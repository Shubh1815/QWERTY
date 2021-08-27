from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.http import JsonResponse, FileResponse
from django.contrib.auth import get_user_model
from django.db.models import Sum, F, DecimalField
from django.urls import reverse_lazy
from django.utils import timezone

from users.models import Student
from users.forms import StudentChangeForm, UserProfileChangeForm
from core.models import Transaction
from users.permissions import is_student, is_manager
from qwerty.settings import LOGIN_URL

from io import BytesIO, SEEK_SET
import json
import datetime
import weasyprint

# Create your views here.

User = get_user_model()


@is_student(login_url=LOGIN_URL)
def dashboard(request):
    if request.method == "GET":
        student = request.user.student

        transactions = Transaction.objects.get_student_transactions(student, params=request.GET)
        context = {
            'student': Student.objects.get(pk=student),
            'transactions': transactions
        }

        return render(request, 'student/dashboard.html', context=context)


@is_student(login_url=LOGIN_URL)
def profile(request):
    user = request.user
    student = request.user.student

    if request.method == 'GET':
        student_form = StudentChangeForm(instance=student, prefix="student")
        user_form = UserProfileChangeForm(instance=user, prefix="user")

    if request.method == 'POST':
        student_form = StudentChangeForm(request.POST, instance=student, prefix='student')
        user_form = UserProfileChangeForm(request.POST, instance=user, prefix='user')

        if student_form.is_valid() and user_form.is_valid():
            student_form.save()
            user_form.save()

            return redirect(reverse_lazy("student:profile"))

    context = {
        'student_form': student_form,
        'user_form': user_form,
    }

    return render(request, 'student/profile.html', context=context)


@is_student(login_url=LOGIN_URL)
def calorie_tracker(request):
    return render(request, 'student/calorie_tracker.html')


@is_student(login_url=LOGIN_URL)
def expense_tracker(request):
    return render(request, 'student/expense-tracker.html')


@is_student(login_url=LOGIN_URL)
def tracker(request, option, days):
    student = request.user.student
    time_span = timezone.now() - datetime.timedelta(days=days)

    if option == 'calorie':
        transactions = Transaction.canteen.filter(
            date__gte=time_span,
            bought_by=student,
        ).select_related('product__calorie')

        transactions = list(transactions.values('date').annotate(value=Sum('product__calorie__calories')))
        return JsonResponse(transactions, safe=False)

    if option == 'expense':
        transactions = Transaction.objects.filter(
            date__gte=time_span,
        )

        transactions = list(
            transactions.values('date').annotate(
                value=Sum(F('amount') * F('quantity'), output_field=DecimalField(max_digits=10, decimal_places=2))
            )
        )

        return JsonResponse(transactions, safe=False)

    return HttpResponse(status=404)


@is_student(login_url=LOGIN_URL)
def wallet(request):
    student = request.user.student
    return HttpResponse('Wallet')


@is_manager(login_url=LOGIN_URL)
def get_student_data(request, enrollment_no):
    student = get_object_or_404(Student, enrollment_no=enrollment_no)

    return JsonResponse(json.dumps(model_to_dict(student)), safe=False)


@staff_member_required
def student_id_pdf(request, enrollment_no):
    student = get_object_or_404(Student, enrollment_no=enrollment_no)

    html = render_to_string('student/student-ID.html', {
        'users': [student.user],
    })

    out = BytesIO()

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        out
    )
    out.seek(SEEK_SET)
    response = FileResponse(out, content_type="application/pdf", filename=f"{student.enrollment_no}_id.pdf")

    return response
