from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    password = forms.CharField(required = True, widget = forms.PasswordInput)
    sexe_choices = (
        ("Homme","Homme"),
        ("Femme","Femme")
    )
    sexe = forms.CharField(widget = forms.Select(choices = sexe_choices))
    