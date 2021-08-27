from io import BytesIO, SEEK_SET
import weasyprint

from django.contrib import admin
from django.http import FileResponse
from django.template.defaultfilters import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.template.loader import render_to_string

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser, StudentUser, Student


class StudentInline(admin.StackedInline):
    verbose_name_plural = "student info"
    model = Student


def get_student_id(modeladmin, request, queryset):
    print(queryset)
    html = render_to_string('student/student-ID.html', {
        'users': queryset,
    })

    out = BytesIO()

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        out
    )
    out.seek(SEEK_SET)
    response = FileResponse(out, content_type="application/pdf", filename="Student-ID.pdf")

    return response
get_student_id.short_description = "Get IDs of selected Students"


class StudentAdmin(UserAdmin):
    actions = [get_student_id]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_filter = ['student__std', ]

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
         ),
    )

    inlines = [StudentInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(student__isnull=False)

    def get_student(self, obj):
        return obj.student.enrollment_no

    def get_student_id(self, obj):
        return mark_safe(f"<a href={obj.student.get_id_pdf()}>ID</a>")

    list_display = ['get_student', 'first_name', 'last_name', 'email', 'get_student_id']
    get_student.short_description = 'enrollment no.'
    get_student_id.short_description = 'ID'


admin.site.register(StudentUser, StudentAdmin)


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_filter = ['is_superuser', 'is_manager']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_manager')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2')}
         ),
        (None, {
            'fields': ('is_superuser', 'is_manager')}
         ),
    )


class HideStudentAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


admin.site.register(Student, HideStudentAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
