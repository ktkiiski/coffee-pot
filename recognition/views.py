"""
Contains picture recognizion related view classes.
"""
from django.views.generic import TemplateView
from webcam.models import Picture


class LabelizerView(TemplateView):
    """
    Shows the HTML page for labelizing unlabeled pictures.
    """
    template_name = "labelizer.html"

    def get_context_data(self, **kwargs):
        context = super(LabelizerView, self).get_context_data(**kwargs)
        pics = Picture.objects.filter(label__isnull=True)
        context['pictures'] = pics.order_by('-created_at')[0:10]
        return context
