from django import forms


class NameForm(forms.Form):
    name1 = forms.CharField()