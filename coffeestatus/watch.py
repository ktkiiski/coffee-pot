from random import choice
from datetime import timedelta
from django.conf import settings
from webcam.models import Picture
from requests import post

FRESHNESS_DURATION = timedelta(minutes=15)
FULL_LABEL_IDS = {'plenty', 'full'}
FULL_CERTAINTY = 0.5
EMPTY_LABEL_IDS = {'empty', 'little'}
EMPTY_CERTAINTY = 0.5


def notify_slack(picture, message):
    """
    Notifies the Slack about the picture with the given message.
    """
    webhook_url = settings.SLACK_WEBHOOK_URL
    if not webhook_url:
        raise Exception("SLACK_WEBHOOK_URL is not configured")
    return post(webhook_url, json={
        "text": message,
        "attachments": [{
            "fallback": "Web camera snapshot",
            "image_url": picture.image.url,
        }]
    })

def check_fresh_coffee(picture):
    """
    Returns a string describing a message whether or not there is
    fresh coffee in the given picture. The freshness is determined
    accordingly to any previous pictures and their certainty.

    Returns None if there is no fresh coffee currently.
    """
    range_end = picture.created_at
    range_start = range_end - FRESHNESS_DURATION
    # Left side
    left_full_queryset = Picture.objects.order_by('created_at').filter(
        created_at__gte=range_start,
        created_at__lte=range_end,
        recognized_left_label_id__in=FULL_LABEL_IDS,
        recognized_left_probability__gte=FULL_CERTAINTY,
    )
    left_became_full = left_full_queryset.first() == picture
    left_empty_queryset = Picture.objects.filter(
        created_at__gte=range_start,
        created_at__lt=range_end,
        recognized_left_label_id__in=EMPTY_LABEL_IDS,
        recognized_left_probability__gte=EMPTY_CERTAINTY,
    )
    left_was_empty = left_empty_queryset.exists()
    left_is_fresh = left_became_full and left_was_empty
    # Right side
    right_full_queryset = Picture.objects.order_by('created_at').filter(
        created_at__gte=range_start,
        created_at__lte=range_end,
        recognized_right_label_id__in=FULL_LABEL_IDS,
        recognized_right_probability__gte=FULL_CERTAINTY,
    )
    right_became_full = right_full_queryset.first() == picture
    right_empty_queryset = Picture.objects.filter(
        created_at__gte=range_start,
        created_at__lt=range_end,
        recognized_right_label_id__in=EMPTY_LABEL_IDS,
        recognized_right_probability__gte=EMPTY_CERTAINTY,
    )
    right_was_empty = right_empty_queryset.exists()
    right_is_fresh = right_became_full and right_was_empty
    # Determine message
    template = choice([
        "Guess what?! {} Go get some!",
        "Attention! {} Hurry up!",
        "Hot beverages available! {}",
        "How about a break? {}",
        "Hey! {} Get your ass to the kitchen!",
        "I have important information to share: {}",
        "Wohoo! {}",
        "Kewl! {}",
    ])
    if left_is_fresh and right_is_fresh:
        return template.format("There is fresh coffee in both pots!")
    if left_is_fresh:
        return template.format("There is fresh coffee in the left pot!")
    if right_is_fresh:
        return template.format("There is fresh coffee in the right pot!")
    return None
