from django import forms

from rbac import models
from rbac.forms.base import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

    def clean_confirm_password(self):
        """
        检测两次密码是否一致
        :return:
        """
        passwrod = self.cleaned_data.get('password')
        confirm_paassword = self.cleaned_data.get('confirm_password')

        if passwrod and confirm_paassword:
            if passwrod != confirm_paassword:
                raise forms.ValidationError('两次密码输入不一致')
            else:
                return confirm_paassword


class UpdateUserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']


class ResetPwdUserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']

    def clean_confirm_password(self):
        """
        检测两次密码是否一致
        :return:
        """
        passwrod = self.cleaned_data.get('password')
        confirm_paassword = self.cleaned_data.get('confirm_password')

        if passwrod and confirm_paassword:
            if passwrod != confirm_paassword:
                raise forms.ValidationError('两次密码输入不一致')
            else:
                return confirm_paassword
