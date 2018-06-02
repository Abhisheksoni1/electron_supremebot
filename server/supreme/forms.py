from django import forms
from supreme.models import Profile, Proxy, Setting


# from .models import SignUp


class LoginForm(forms.Form):
    password = forms.CharField(max_length=32)


class SaveTaskForm(forms.Form):
    category = forms.CharField(max_length=32)
    profile = forms.CharField(max_length=32)
    keyword = forms.CharField(max_length=32)
    color = forms.CharField(max_length=16)
    timer = forms.CharField(max_length=10)
    proxy = forms.CharField(max_length=32)
    size = forms.CharField(max_length=16)


class EditTaskForm(forms.Form):
    id = forms.IntegerField(initial=0)
    category = forms.CharField(max_length=32)
    profile = forms.CharField(max_length=32)
    keyword = forms.CharField(max_length=32)
    color = forms.CharField(max_length=16)
    timer = forms.CharField(max_length=10)
    proxy = forms.CharField(max_length=32)
    size = forms.CharField(max_length=16)


class SaveProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'phone', 'email', 'card_number', 'cvv',
                  'expiry', 'year', 'address1', 'address2', 'city',
                  'zip_code', 'payment_option', 'country')


class EditProfileForm(forms.ModelForm):
    id = forms.IntegerField(initial=0)

    class Meta:
        model = Profile
        fields = ('name', 'phone', 'email', 'card_number', 'cvv',
                  'expiry', 'year', 'address1', 'address2', 'city',
                  'zip_code', 'payment_option', 'country')


class SaveProxyForm(forms.ModelForm):
    class Meta:
        model = Proxy
        fields = ('name',)


class SaveSettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ('key', 'moniter', 'checkout_delay', 'gmail', 'mode')