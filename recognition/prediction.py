"""
Integration for the picture labeling prediction.
"""
import requests

# The endpoint that will be queried for the labels
PREDICT_ENDPOINT = "https://coffeebrain.int.giosg.com/predict"

def predict_picture_labels(picture):
    """
    Tries to predict the best labels for both the left and the right
    side of the given Picture model instance, using its 'image'.

    Sets the 'recognized_left_label' and 'recognized_right_label' fields
    and then saves the image.
    """
    image_url = picture.image.url
    response = requests.post(PREDICT_ENDPOINT, json={
        'image_url': image_url,
    })
    data = response.json()
    # Get the best matching labels
    right_labels = data['right_probabilities']
    right_label_id, right_label_prob = max(right_labels.items(), key=lambda i: i[1])
    left_labels = data['left_probabilities']
    left_label_id, left_label_prob = max(left_labels.items(), key=lambda i: i[1])
    # Save the labels
    picture.recognized_left_label_id = left_label_id
    picture.recognized_left_probability = left_label_prob
    picture.recognized_right_label_id = right_label_id
    picture.recognized_right_probability = right_label_prob
    picture.save()
    return picture
