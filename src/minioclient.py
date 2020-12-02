from minio import Minio
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists, ResponseError, NoSuchBucket, NoSuchKey


class MinioClient:

    def __init__(self, host, login, password):
        self.minio = Minio(host, access_key=login, secret_key=password, secure=True)

    def ensure_bucket(self, bucketName):
        try:
            self.minio.make_bucket(bucketName)
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            raise

    def object_exists(self, bucket, object):
        try:
            ret = self.minio.stat_object(bucket, object)
        except NoSuchBucket as err:
            return False
        except NoSuchKey as err:
            return False
        return True

    def put_file(self, bucket, object, file_path, content_type):
        self.minio.fput_object(bucket, object, file_path, content_type)