"""
Forms for picture labeling.
"""
from django import forms
from webcam.models import Picture


class PictureLabelizerForm(forms.ModelForm):
    """
    Form for labelizing a picture.
    """
    class Meta:
        model = Picture
        fields = [
            'label',
        ]
        widgets = {
            'label': forms.RadioSelect(),
        }
