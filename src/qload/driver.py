import os.path
import tempfile
from typing import Optional

import boto3
import ftputil

from qload.base import QloadEngine
from qload.exception import InvalidRemoteFile


def file() -> QloadEngine:
    driver = QloadDriverFile()
    return QloadEngine(driver)


def ftp(host: str = 'localhost', user: Optional[str] = None, passwd: Optional[str] = None, **kwargs) -> QloadEngine:
    """

    :param host:
    :param user:
    :param passwd:
    :param kwargs: use session_factory arguments of ftputil (https://ftputil.sschwarzer.net/documentation#session-factories)

    >>> assert qload.ftp(user='admin', passwd='admin').text('file.txt', expression='Hello .*') == 'Hello fabien'
    >>> assert qload.ftp(user='admin', passwd='admin', port=210).text('file.txt', expression='Hello .*') == 'Hello fabien'

    :return:
    """
    driver = QloadDriverFtp(host=host, user=user, passwd=passwd, **kwargs)
    return QloadEngine(driver)


def s3(bucket: str, endpoint_url: Optional[str] = None, region_name: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] =  None, **kwargs) -> QloadEngine:
    """

    :param bucket: bucket name of s3
    :param kwargs:
    :return:
    """
    driver = QloadDriverS3(bucket, endpoint_url, region_name, aws_access_key_id, aws_secret_access_key, **kwargs)
    return QloadEngine(driver)


class QloadDriver:
    """
    the driver is an interface to download a remote file locally. A driver corresponds to a storage system.
    """


    def download(self, path: str) -> str:
        """
        primitive pour télécharger le fichier en local. Une fois téléchargée, le chemin est retourné.

        :param path: remote file path to download
        :return: path of the file that was downloaded locally
        """
        raise NotImplementedError


    def isfile(self, path: str) -> bool:
        """
        primitive to check if a file exists
        """
        raise NotImplementedError

class QloadDriverFile(QloadDriver):


    def download(self, path: str) -> str:
        """
        the driver which dialogues with the local filesystem does not need to download the file in order to be able to read its content.
        """
        return path

    def isfile(self, path: str) -> bool:
        return os.path.isfile(path)


class QloadDriverFtp(QloadDriver):


    def __init__(self, host: str = 'localhost', user: Optional[str] = None, passwd: Optional[str] = None, **kwargs):
        """
        Les arguments du driver correspond aux arguments de `ftplib.FTP`

        :param host:
        :param port:
        :param user:
        :param passwd:
        """
        self.host = host
        self.user = '' if user is None else user
        self.passwd = '' if passwd is None else passwd
        self.kwargs = kwargs

    def download(self, path: str) -> Optional[str]:
        """
        QloadDriverFtp loads an ftp file into the system temporary files and
        returns the path to the downloaded file.

        :param path: file path on ftp server
        :return:
        """
        my_session_factory = ftputil.session.session_factory(**self.kwargs)

        _, filepath = tempfile.mkstemp()
        with ftputil.FTPHost(self.host, self.user, self.passwd, session_factory=my_session_factory) as host:
            if host.path.isfile(path):
                host.download(path, filepath)
                return filepath

        raise InvalidRemoteFile(path)

    def isfile(self, path: str) -> bool:
        """
        Checks if a file exists on the ftp server

        """
        my_session_factory = ftputil.session.session_factory(**self.kwargs)

        with ftputil.FTPHost(self.host, self.user, self.passwd, session_factory=my_session_factory) as host:
            return host.path.isfile(path)

class QloadDriverS3(QloadDriver):


    def __init__(self, bucket: str, endpoint_url: Optional[str] = None, region_name: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] =  None, **kwargs):
        """

        :param bucket:
        :param endpoint_url: The complete URL to use for the constructed client. Normally, botocore will automatically construct the appropriate URL to use when communicating with a service.
        :param region_name: The name of the region associated with the client. A client is associated with a single region.
        :param aws_access_key_id: The access key to use when creating the client. This is entirely optional, and if not provided, the credentials configured for the session will automatically be used. You only need to provide this argument if you want to override the credentials used for this specific client.
        :param aws_secret_access_key: The secret key to use when creating the client. Same semantics as aws_access_key_id above.
        :param kwargs: other arguments allowed s3.client (see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html)
        """
        self.bucket = bucket
        if endpoint_url is not None:
            kwargs['endpoint_url'] = endpoint_url

        if region_name is not None:
            kwargs['region_name'] = region_name

        if aws_access_key_id is not None:
            kwargs['aws_access_key_id'] = aws_access_key_id

        if aws_secret_access_key is not None:
            kwargs['aws_secret_access_key'] = aws_secret_access_key

        self.kwargs = kwargs

    def download(self, path: str) -> Optional[str]:
        """
        QloadDriverS3 loads a file from a s3 bucket into the system temporary files and
        returns the path to the downloaded file.

        :param path: s3 key of the file on the s3 bucket
        :return:
        """
        from botocore.errorfactory import ClientError

        client = boto3.client('s3', **self.kwargs)
        _, filepath = tempfile.mkstemp()
        try:
            client.head_object(Bucket=self.bucket, Key=path)
        except ClientError:
            raise InvalidRemoteFile(path)

        client.download_file(Bucket=self.bucket, Key=path, Filename=filepath)
        return filepath


    def isfile(self, path: str) -> bool:
        """
        QloadDriverS3 checks if a file exists on the s3 bucket

        >>> driver = QloadDriverS3(bucket='mybucket')
        >>> driver.isfile(path='mykey')
        """
        from botocore.errorfactory import ClientError

        client = boto3.client('s3', **self.kwargs)
        _, filepath = tempfile.mkstemp()
        try:
            client.head_object(Bucket=self.bucket, Key=path)
            return True
        except ClientError:
            return False