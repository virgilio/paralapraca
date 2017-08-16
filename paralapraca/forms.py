from accounts.forms import AcceptTermsForm
from django.contrib.auth.models import Group


class SignupForm(AcceptTermsForm):

    def signup(self, request, user):
        # Add the new user to the students group for Timtec compatibility
        user.groups.add(Group.objects.get(name='students'))
        user.accepted_terms = self.cleaned_data['accept_terms']
        user.save()
