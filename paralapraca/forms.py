from accounts.forms import AcceptTermsForm, BaseProfileEditForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class SignupForm(AcceptTermsForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def signup(self, request, user):
        # Add the new user to the students group for Timtec compatibility
        user.groups.add(Group.objects.get(name='students'))

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        user.accepted_terms = self.cleaned_data['accept_terms']
        user.save()


class ProfileEditForm(BaseProfileEditForm):

    email = forms.RegexField(label=_("email"), max_length=75, regex=r"^[\w.@+-]+$")

    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'picture',
                  'occupation', 'city', 'site', 'biography')

    # FIXME: username should be actually cleaned
    def clean_username(self):
        return self.instance.username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        if self.cleaned_data['password1']:
            self.instance.set_password(self.cleaned_data['password1'])
        return super(ProfileEditForm, self).save(commit=commit)
