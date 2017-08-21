from accounts.forms import AcceptTermsForm
from django.contrib.auth.models import Group
from django import forms


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
