from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from symbi.models import InterestTag, SymbiUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "w-full p-2 border border-gray-300 rounded"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "w-full p-2 border border-gray-300 rounded"}
        )
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": ("This account is inactive."),
    }

    class Meta:
        model = SymbiUser
        fields = ["username", "password"]


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-2 border border-gray-300 rounded",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full p-2 border border-gray-300 rounded",
            },
        ),
    )
    full_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-2 border border-gray-300 rounded",
            }
        ),
    )
    pronouns = forms.IntegerField(
        widget=forms.Select(
            choices=SymbiUser.Pronouns.choices,
            attrs={"class": "w-full p-2 border border-gray-300 rounded"},
        ),
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "w-full p-2 border border-gray-300 rounded",
                "type": "date",
            }
        ),
    )
    major = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "w-full p-2 border border-gray-300 rounded"}
        ),
    )
    interests = forms.ModelMultipleChoiceField(
        queryset=InterestTag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "w-1/2 p-2 border border-gray-300 rounded max-h-52 overflow-y-auto"
            }
        ),
        required=False,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "w-full p-2 border border-gray-300 rounded"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "w-full p-2 border border-gray-300 rounded"}
        )
    )

    class Meta:
        model = SymbiUser
        fields = [
            "username",
            "email",
            "full_name",
            "pronouns",
            "date_of_birth",
            "major",
            "interests",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if SymbiUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose a different one."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        email_domain = email.split("@")[1]

        if email_domain != "nyu.edu":
            raise forms.ValidationError(
                "Invalid email domain. Please use an NYU email address to sign up."
            )
        elif SymbiUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already associated with an account.")

        return email
