"""
Contains picture recognizion related view classes.
"""
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from webcam.models import Picture
from .forms import PictureLabelizerForm


def labelize_pictures(request):
    """
    Shows the HTML page for labelizing unlabeled pictures.
    """
    form_set = modelformset_factory(Picture, form=PictureLabelizerForm, extra=0)
    pics = Picture.objects.filter(label__isnull=True).order_by('-created_at')[0:50]
    if request.method == 'POST':
        formset = form_set(request.POST, request.FILES, queryset=pics)
        if formset.is_valid():
            formset.save()
            return redirect('labelizer')
    else:
        formset = form_set(queryset=pics)
    return render(request, 'labelizer.html', {
        'formset': formset,
        'unlabeled_count': Picture.objects.filter(label__isnull=True).count(),
    })
