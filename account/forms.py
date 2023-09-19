from django import forms
from . models import Account, Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control p_input',
        'placeholder':'input password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control p_input',
        'placeholder':'confirm password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password or len(password) < 6:
            raise forms.ValidationError("please check your password, password must be greater than 5 and must match")

        

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control p_input'
            

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'passport', 'id_verification')

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            