from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser, StudentUser, Student


class StudentInline(admin.StackedInline):
    verbose_name_plural = "student info"
    model = Student


class StudentAdmin(UserAdmin):
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

    def get_student(self, obj):
        return obj.student.enrollment_no

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_manager=False, is_superuser=False)

    list_display = ['get_student', 'first_name', 'last_name', 'email']
    get_student.short_description = 'enrollment no.'


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
