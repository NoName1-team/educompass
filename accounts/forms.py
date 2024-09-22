from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'XX XXX XX XX'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ism'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiya'}),
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['phone']
        if commit:
            user.save()
        return user
