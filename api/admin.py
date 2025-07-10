from django.contrib import admin


from api.models import SignUp
# Register your models here.
class SignupAdmin(admin.ModelAdmin):
     list_display=('name', 'email')

# Register your models here.
admin.site.register(SignUp,SignupAdmin)

