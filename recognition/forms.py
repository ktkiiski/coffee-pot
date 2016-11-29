"""
Forms for picture labeling.
"""
from django import forms
from webcam.models import Picture


class PictureLeftLabelizerForm(forms.ModelForm):
    """
    Form for labelizing a left-side of a picture.
    """
    class Meta:
        model = Picture
        fields = [
            'left_label',
        ]
        widgets = {
            'left_label': forms.RadioSelect(),
        }


class PictureRightLabelizerForm(forms.ModelForm):
    """
    Form for labelizing a right-side of a picture.
    """
    class Meta:
        model = Picture
        fields = [
            'right_label',
        ]
        widgets = {
            'right_label': forms.RadioSelect(),
        }


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
