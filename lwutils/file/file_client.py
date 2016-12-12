from lwutils.boto3.resource import Resource


class FileClient(object):

    def factory(config):
        if config.get('FILE_PROVIDER') == "AWS":
            return AWSFileClient(config)
        # assert 0, "Unknown File provider: " + config.get('FILE_PROVIDER', "not configured")
    factory = staticmethod(factory)


class AWSFileClient(FileClient):

    def __init__(self, config):
        self.config = config
        self.s3 = Resource(self.config).s3()

    def get_folder(self, bucket_name):
        folder = AWSFolder(self.s3.Bucket(bucket_name))
        return folder


class AWSFolder(object):
    def __init__(self, s3_resource, bucket_name):
        self.s3_resource = s3_resource
        self.s3_bucket = self.s3_resource.Bucket(bucket_name)

    def files(self, filter):
        files = []
        s3_files = self.s3_bucket.objects.filter(Prefix=filter)
        for s3_file in s3_files:
            files.append(AWSFile(s3_file))
        return files

    def file(self, file_name):
        s3_file = self.s3_resource.Object(self.s3_bucket, file_name)
        return AWSFile(s3_file)


class AWSFile(object):
    def __init__(self, s3_file):
        self.s3_file = s3_file

    def get_body(self):
        return self.s3_file.get()["Body"].read()

    def set_body(self, file, public=False):
        acl = 'private' if not public else 'public-read'
        self.s3_file.put(ACL=acl, Body=file)

    def delete(self):
        self.s3_file.delete()

    def name(self):
        return self.s3_file.key

    def size(self):
        return self.s3_file.size
