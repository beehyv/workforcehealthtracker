import re

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from MyUser.models import MyUser, HCWorker, HCWType, ResultStatus
from facility.models.facility import Facility


class UserCreationForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    organization = forms.ModelChoiceField(
        queryset=Facility.objects.all(),
        required=True,
    )

    class Meta:
        model = MyUser
        fields = '__all__'

    def clean_password1(self):
        username = self.cleaned_data.get("username")
        password1 = self.cleaned_data.get("password1")

        if (username and password1 and password1 == username):
            raise forms.ValidationError("Password and username should be different")
        if (username and password1 and username in password1):
            raise forms.ValidationError("Password should not contain username")
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$', password1):
            raise forms.ValidationError(
                "Password should be 6 character long, at least one uppercase, one lowercase, one number and no special characters")
        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    organization = forms.ModelChoiceField(
        queryset=Facility.objects.all(),
        required=True,
    )

    class Meta:
        model = MyUser
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_per_page = 20
    list_filter = ('is_admin',)
    _list_filter = list_filter
    list_display = ('first_name', 'last_name', 'username', 'whatsapp_number', 'assigned_facility')
    search_fields = ('first_name', 'username', 'whatsapp_number')
    filter_horizontal = ()

    def get_queryset(self, request):
        if request.user.is_admin:
            return MyUser.objects.all()
        else:
            facility = request.user.organization
            return MyUser.objects.filter(organization=facility).all()

    #todo make organization preselected by default on when manager create other managers

    def save_model(self, request, obj, form, change):
        default_group = obj.organization.usergroup_set.filter(is_default=True).first()
        res = super(MyUserAdmin, self).save_model(request, obj, form, change)
        default_group.managers.add(obj)
        return res

    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            (None, {'fields': ('first_name', 'last_name', 'email', 'username', 'organization', 'whatsapp_number', 'password', 'language')}),
        )
        # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
        # overrides get_fieldsets to use this attribute when creating a user.
        self.add_fieldsets = (
            (None, {
                'classes': ('wide',),

                'fields': ('first_name', 'last_name', 'email', 'username', 'organization', 'whatsapp_number', 'password1', 'password2', 'language')}
             ),
        )
        if request.user.is_admin:
            self.fieldsets = (
            (None, {'fields': ('first_name', 'last_name', 'email', 'username', 'whatsapp_number', 'organization', 'password', 'language', 'is_admin')}),)
            self.add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
            'first_name', 'last_name', 'email', 'username', 'whatsapp_number', 'organization', 'password1', 'password2', 'language', 'is_admin')}),)
        return super(MyUserAdmin, self).get_form(request, obj, **kwargs)

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_admin:
            self.list_filter = None
        else:
            self.list_filter = self._list_filter
        return super(MyUserAdmin, self).changelist_view(request, extra_context)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password1(self):
        username = self.user.username
        password1 = self.cleaned_data.get("new_password1")

        if (username and password1 and password1 == username):
            raise forms.ValidationError("Password and username should be different")
        if (username and password1 and username in password1):
            raise forms.ValidationError("Password should not contain username")
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$', password1):
            raise forms.ValidationError(
                "Password should be 6 character long, at least one uppercase, one lowercase, one number and no special characters")
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class CustomPasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Your old password was entered incorrectly. "
                               "Please enter it again."),
    })
    old_password = forms.CharField(label=("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


@sensitive_post_parameters()
@csrf_protect
@login_required
def custom_password_change_view(request,
                                template_name='registration/password_change_form.html',
                                post_change_redirect=None,
                                password_change_form=CustomPasswordChangeForm,
                                current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def custom_password_reset_confirm(request, uidb64=None, token=None,
                                  template_name='registration/password_reset_confirm.html',
                                  token_generator=default_token_generator,
                                  set_password_form=SetPasswordForm,
                                  post_reset_redirect=None,
                                  current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)



class HCWAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    list_per_page = 20
    list_display = ('first_name', 'last_name', 'hcw_type_id', 'phone_number', 'whatsapp_number')
    search_fields = ('first_name', 'phone_number', 'whatsapp_number')
    list_filter = ('hcw_type_id',)
    ordering = ('first_name',)
    filter_horizontal = ()
    readonly_fields = ('is_consented',)
    exclude = ('result_status_id', 'is_active')
    change_form_template = 'admin/MyUser/change_form.html'

    def save_model(self, request, obj, form, change):
        default_group = obj.facility.usergroup_set.filter(is_default=True).first()
        res = super(HCWAdmin, self).save_model(request, obj, form, change)
        default_group.workers.add(obj)
        return res

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_admin:
            if db_field.name == "facility":
                kwargs["queryset"] = Facility.objects.filter(id=request.user.organization.id)

        return super(HCWAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        if request.user.is_admin == True:
            self.list_filter = ('facility', 'hcw_type_id',)
            return HCWorker.objects
        hcw_set_id = set()
        for group in request.user.usergroup_set.all():
            for hcw in group.workers.all():
                hcw_set_id.add(hcw.id)

        return HCWorker.objects.filter(pk__in=hcw_set_id)

class HCWTypeAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('hcw_type_name',)


class ResultStatusAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('result_status', 'result_message')
    exclude = ('id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions and not request.user.is_admin:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(HCWorker, HCWAdmin)
admin.site.register(HCWType, HCWTypeAdmin)
admin.site.register(ResultStatus, ResultStatusAdmin)
