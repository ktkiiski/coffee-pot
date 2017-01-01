"""
Django settings for production use.
"""
from .local import *

# No debugging in production
DEBUG = False

# Whether to enable gzip compression for static files.
AWS_S3_GZIP_STATIC = True

# In production, store static files to S3
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
