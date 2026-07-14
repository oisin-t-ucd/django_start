from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Message


class ComposeMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["recipient", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        # Add a custom bootstrap primary button via python
        self.helper.add_input(
            Submit("submit", "Send Message", css_class="btn btn-primary mt-3")
        )
