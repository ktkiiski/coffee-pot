"""
Django settings for production use.
"""
from .local import *

# No debugging in production
DEBUG = False

# The AWS access key used to access the storage buckets.
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]

# The AWS secret access key used to access the storage buckets.
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

# The S3 bucket used to store uploaded files.
AWS_S3_BUCKET_NAME = os.environ["AWS_S3_BUCKET_NAME"]

# The region to connect to when storing files.
AWS_REGION = os.environ["AWS_REGION"]

# A prefix to add to the start of all uploaded files.
AWS_S3_KEY_PREFIX = os.environ.get("AWS_S3_KEY_PREFIX") or "media"

# Whether to enable querystring authentication for uploaded files.
AWS_S3_BUCKET_AUTH = False

# The S3 bucket used to store static files.
AWS_S3_BUCKET_NAME_STATIC = AWS_S3_BUCKET_NAME

# Whether to enable querystring authentication for static files.
AWS_S3_BUCKET_AUTH_STATIC = False

# A prefix to add to the start of all static files.
AWS_S3_KEY_PREFIX_STATIC = os.environ.get("AWS_S3_KEY_PREFIX_STATIC") or "static"

# Whether to enable gzip compression for static files.
AWS_S3_GZIP_STATIC = True

DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
