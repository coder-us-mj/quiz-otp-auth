from django.contrib import admin
from quiz_app.common.models.user.user_signup import SignUp

class SignupAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SignUp model.
    Controls how user records are displayed in the Django admin panel.
    """
    list_display = ('name', 'email')

# Register the customized admin with the model
admin.site.register(SignUp, SignupAdmin)