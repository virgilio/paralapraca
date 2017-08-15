from accounts.forms import AcceptTermsForm


class SignupForm(AcceptTermsForm):

    def signup(self, request, user):
        user.accepted_terms = self.cleaned_data['accept_terms']
        user.save()
