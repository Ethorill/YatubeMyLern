from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    email = forms.EmailField(max_length="200",
                             help_text="Мы отправим вам письмо"
                             )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ("first_name", "last_name", "username", "email")
