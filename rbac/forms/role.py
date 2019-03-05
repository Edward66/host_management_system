from rbac import models
from rbac.forms.base import BootStrapModelForm


class RoleModelForm(BootStrapModelForm):
    class Meta:
        model = models.Role
        fields = ['title', ]
