from django import forms
from host import models
from host.forms.base import BootStrapModelForm


class HostModelForm(BootStrapModelForm):
    class Meta:
        model = models.Host
        fields = '__all__'
