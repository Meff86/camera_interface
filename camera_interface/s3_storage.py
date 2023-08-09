from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'meff1986'
    location = 'media'


class StaticStorage(S3Boto3Storage):
    bucket_name = 'meff1986'
    location = 'static'