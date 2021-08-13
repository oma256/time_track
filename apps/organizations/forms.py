from django import forms

from apps.organizations.models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('phone',)
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'placeholder': '(000) 00-00-00',
                    'autocomplete': 'off',
                    'id': 'feedback-input-id',
                }
            )
        }
