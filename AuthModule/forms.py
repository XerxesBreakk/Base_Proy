from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    
    error_messages = {
        "password_mismatch": ("La clave no coincide"),
    }
    password1 = forms.CharField(
        label=("Clave"),
        strip=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'placeholder':"Password",'class':"form-control form-control-user",}),
        help_text=("Mínimo 8 caracteres, debe contener numeros y letras."),
    )
    password2 = forms.CharField(
        label=("Confirmacion de clave"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'placeholder':"Password",'class':"form-control form-control-user",}),
        strip=True,
        help_text=("Ingrese su clave nuevamente, para verificación"),
    )

    class Meta:
        model = User
        fields = ("username","email","first_name","last_name","is_superuser","is_staff",)

        widgets= {
            'email': forms.EmailInput(
                attrs={
                    'id':"email",
                    'placeholder':"capenafi@espol.edu.ec",
                    'class':"form-control form-control-user",
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'id':"username",
                    'placeholder':"Username",
                    'class':"form-control form-control-user",
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'id':"first_name",
                    'placeholder':"Nombres",
                    'class':"form-control form-control-user",
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'id':"last_name",
                    'placeholder':"Apellidos",
                    'class':"form-control form-control-user",
                }
            ),
            'is_superuser': forms.CheckboxInput(
                attrs={
                    'class':"form-check-input",
                }
            ),
            'is_staff': forms.CheckboxInput(
                attrs={
                    'value':'True',
                    'class':"form-check-input",
                }
            ),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user