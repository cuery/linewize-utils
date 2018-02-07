import boto3


class Resource(object):

    def __init__(self, config):
        self.aws_access_key_id = config.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = config.get("AWS_SECRET_ACCESS_KEY")
        self.region_name = config.get("AWS_REGION")

    def _resource(self, service_name, region_name=None, **kwargs):
        session = boto3.session.Session()
        if region_name is None:
            region_name = self.region_name
        return session.resource(
            service_name, aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=region_name, **kwargs)

    def s3(self, region_name=None, **kwargs):
        return self._resource("s3", region_name=region_name, **kwargs)

    def sqs(self, region_name=None, **kwargs):
        return self._resource("sqs", region_name=region_name, **kwargs)

    def cloudwatch(self, region_name=None, **kwargs):
        return self._resource("cloudwatch", region_name=region_name, **kwargs)

    def ec2(self, region_name=None, **kwargs):
        return self._resource("ec2", region_name=region_name, **kwargs)

    def kinesis(self, region_name=None, **kwargs):
        return self._resource("kinesis", region_name=region_name, **kwargs)