from django import forms
from .models import Profile, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# ------ 2 register variantui -------
from django.contrib.auth.models import User

# ------ 1 register variantui -------
# from .models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

# ------ 1 register veikia ------
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True, label="El. paštas")
#     password2 = None
#     password1 = forms.CharField(label="Slaptažodis", widget=forms.PasswordInput)

#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #   self.fields["password1"].label = "Slaptažodis"

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1"]
#         labels = {
#             "username": "Vartotojo vardas",
#             # 'password1': 'slaptažodis'
#         }
#         help_texts = {
#             "username": None,
#         }
#         error_messages = {
#             "username": {"unique": "Toks vartotojas jau egzistuoja."},
#         }

#     def clean_password1(self):
#         # self yra UserRegisterForm objektas (instance), o .instance yra modelio (User) instance
#         # print(self.instance)
#         password1 = self.cleaned_data.get("password1")
#         try:
#             password_validation.validate_password(password1, self.instance)
#         except forms.ValidationError as error:

#             # Method inherited from BaseForm
#             self.add_error("password1", error)
#         return password1

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("Toks el. paštas jau užregistruotas.")
#         return email


# ------ 2 register veikia ------
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, label="Vartotojo vardas", required=True)
    email = forms.EmailField(label="El. paštas", required=True)
    password1 = forms.CharField(
        label="Slaptažodis", widget=forms.PasswordInput, required=True
    )
    # password2 = forms.CharField(
    #     label="Pakartokite slaptažodį", widget=forms.PasswordInput
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {"required": "Šis laukas yra privalomas."}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            raise forms.ValidationError("Toks vartotojo vardas jau egzistuoja.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        queryset = User.objects.filter(email=email)
        if queryset.exists():
            raise forms.ValidationError("Toks el. paštas jau egzistuoja.")
        return email

    # du slaptažodžiai
    # def clean(self):
    #     data = self.cleaned_data
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password2 != password1:
    #         raise forms.ValidationError("Saptažodžiai turi sutapti")
    #     return data

    # vienas slaptažodis
    def clean_password1(self):
        # self yra RegisterForm objektas (instance)
        print(self)
        password1 = self.cleaned_data.get("password1")
        try:
            password_validation.validate_password(password1, self)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error("password1", error)
        return password1


# ------------ 1 login veikia -------------
# class MyLoginForm(forms.Form):
#     email = forms.EmailField(label="El. paštas")
#     password = forms.CharField(label="Slaptažodis", widget=forms.PasswordInput)


# ------------ 2 login veikia -------------
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label="El. paštas", required=True)
    password = forms.CharField(
        label="Slaptažodis", widget=forms.PasswordInput, required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {"required": "Šis laukas yra privalomas."}


# ------------ 3 login veikia -------------
# class MyLoginForm(forms.Form):
#     # veikia su tokiais pavadinimais:
#     # name = forms.CharField()
#     # psw = forms.CharField(widget=forms.PasswordInput)
#     email = forms.CharField(label="El. Paštas")
#     password = forms.CharField(label="Slaptažodis", widget=forms.PasswordInput)


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ["title", "video"]

#     # galima pakeisti formą čia (jeigu užkomentuota, tai forma rankiniu būdu padaryta template post_upload.html)
#     #     labels = {
#     #         "title": "Antraštė",
#     #         "video": "Įkelti video",
#     #     }

#     #     # error_messages = {
#     #     #     "title": {"required": "Šis laukas yra privalomas."},
#     #     #     "video": {"required": "Šis laukas yra privalomas."},
#     #     # }

#     # # tas pats kas ir error_messages variantas:
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     for field in self.fields.values():
#     #         field.error_messages = {"required": "Šis laukas yra privalomas."}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class UserUpdateForm(forms.Form):
    password = forms.CharField(
        label="Dabartinis slaptažodis",
        widget=forms.PasswordInput(
            attrs={"class": "textinput textInput form-control-update"}
        ),
        required=False,
    )

    password2 = forms.CharField(
        label="Naujas slaptažodis",
        widget=forms.PasswordInput(
            attrs={"class": "textinput textInput form-control-update"}
        ),
        validators=[validate_password],
        required=False,
    )

    password3 = forms.CharField(
        label="Pakartoti naują slaptažodį",
        widget=forms.PasswordInput(
            attrs={"class": "textinput textInput form-control-update"}
        ),
        validators=[validate_password],
        required=False,
    )

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.get("user") # __init__() got an unexpected keyword argument 'user'
        self.user = kwargs.pop("user")
        super().__init__(
            *args, **kwargs
        )  # jeigu ištrinti, mūsų klasė negaus Form klasės atributus ir metodus, bus klaidos
        # for field in self.fields.values():
        #     field.error_messages = {
        #         "required": "Šis laukas yra privalomas.",
        #     }

    error_messages = {
        "password_mismatch": "Nauji slaptažodžiai turi sutapti.",
        "password_incorrect": "Įveskite teisingą seną slaptažodį.",
        "password_fill_other": "Pakartokite naują slaptažodį.",
        "password_first": "Pirmiausia įveskite seną slaptažodį.",
    }

    def clean(self):
        password = self.cleaned_data.get("password")
        if password and not self.user.check_password(password):
            raise forms.ValidationError(
                self.error_messages["password_incorrect"], code="password_incorrect"
            )
        # print(password)
        # print(self.cleaned_data["password"])
        # password2 = self.cleaned_data["password2"] # Exception Type: KeyError Exception Value: 'password2'
        # password3 = self.cleaned_data["password3"]
        password2 = self.cleaned_data.get("password2")
        password3 = self.cleaned_data.get("password3")
        if self.cleaned_data["password"]:
            if password2 and password3:
                if password2 != password3:
                    raise forms.ValidationError(
                        self.error_messages["password_mismatch"],
                        code="password_mismatch",
                    )
            # return password2 # error - 'str' object has no attribute 'get'
            elif password2 or password3 == False:
                raise forms.ValidationError(
                    self.error_messages["password_fill_other"],
                    code="password_fill_other",
                )
            elif password2 == False or password3:
                raise forms.ValidationError(
                    self.error_messages["password_fill_other"],
                    code="password_fill_other",
                )
        # elif self.cleaned_data["password"] == False: # neveikia - kodel?
        elif self.cleaned_data["password"] == "":
            if password2 and password3:
                raise forms.ValidationError(
                    self.error_messages["password_first"], code="password_first",
                )
            elif password2 or password3 == False:
                raise forms.ValidationError(
                    self.error_messages["password_first"], code="password_first",
                )
            elif password2 == False or password3:
                raise forms.ValidationError(
                    self.error_messages["password_first"], code="password_first",
                )
        return self.cleaned_data

    def save(self, commit=True):
        newPassword = self.cleaned_data.get("password2")
        if newPassword:
            self.user.set_password(newPassword)
            if commit:
                self.user.save()
            return self.user
