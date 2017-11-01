from lwutils.boto3.resource import Resource


class AWSFileClient(object):

    def __init__(self, config):
        self.config = config
        self.s3 = Resource(self.config).s3()

    def get_folder(self, bucket_name):
        folder = AWSFolder(self.s3, bucket_name)
        return folder

class AWSFolder(object):
    def __init__(self, s3_resource, bucket_name):
        self.s3_resource = s3_resource
        self.s3_bucket = self.s3_resource.Bucket(bucket_name)
        self.s3_bucket_name = bucket_name

    def files(self, filter):
        files = []
        s3_files = self.s3_bucket.objects.filter(Prefix=filter)
        for s3_file in s3_files:
            files.append(AWSFile(s3_file))
        return files

    def file(self, file_name):
        s3_file = self.s3_resource.Object(self.s3_bucket_name, file_name)
        return AWSFile(s3_file)

    def generate_url(self, file_name, expiry=600):
        url = self.s3_resource.meta.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.s3_bucket_name,
                'Key': file_name, },
            ExpiresIn=expiry, )
        return url


class AWSFile(object):
    def __init__(self, s3_file):
        self.s3_file = s3_file

    def get_body(self):
        return self.s3_file.get()["Body"].read()

    def set_body(self, file, public=False, content_encoding=None):
        acl = 'private' if not public else 'public-read'

        if content_encoding:
            self.s3_file.put(ACL=acl, Body=file,
                             ContentEncoding=content_encoding)
        else:
            self.s3_file.put(ACL=acl, Body=file)

    def delete(self):
        self.s3_file.delete()

    def name(self):
        return self.s3_file.key

    def size(self):
        return self.s3_file.size
