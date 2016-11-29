import csv
from django.http import StreamingHttpResponse
from webcam.models import Picture


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def dump_labeled_pics(request):
    """A view that streams a labeled pictures as a CSV file."""
    pics = Picture.objects.filter(left_label__isnull=False, right_label__isnull=False)\
        .order_by('created_at')
    rows = ([pic.image.url, pic.left_label_id, pic.right_label_id] for pic in pics.iterator())
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="labeled_pics.csv"'
    return response
