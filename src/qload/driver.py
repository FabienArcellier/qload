import tempfile
from typing import Optional

import ftputil

from qload.base import QloadEngine
from qload.exception import InvalidRemoteFile


def file():
    driver = QloadDriverFile()
    return QloadEngine(driver)


def ftp(host: str = 'localhost', user: Optional[str] = None, passwd: Optional[str] = None, **kwargs):
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


class QloadDriverFile(QloadDriver):

    def download(self, path: str) -> str:
        """
        the driver which dialogues with the local filesystem does not need to download the file in order to be able to read its content.

        :param path:
        :return:
        """
        return path


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

