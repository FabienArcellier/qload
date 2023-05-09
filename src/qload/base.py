import csv
import io
import json
import typing
from typing import Optional, Union, Callable

import yaml
from yaml import BaseLoader

from qload import expression as _expression

if typing.TYPE_CHECKING:
    from qload.driver import QloadDriver


class QloadEngine:
    """
    This engine takes the file on disk or which has been moved to disk, reads its content and
    applies an expression according to the format requested by the user.
    """

    def __init__(self, driver: 'QloadDriver' = None):
        self.driver = driver

    def isfile(self, path: str, **kwargs) -> bool:
        isfile = self.driver.isfile(path=path)
        return isfile

    def csv(self, path: str, expression: Optional[str] = None, **kwargs) ->  Union[None, str, list, dict]:
        local_path = self.driver.download(path=path)
        content = []
        with io.open(local_path) as fp:
            reader = csv.DictReader(fp, **kwargs)
            for item in reader:
                content.append(item)

        if expression is None:
            return content

        result = _expression.jmespath_find_all(content, expression)
        return result

    def json(self, path: str, expression: Optional[str] = None) -> Union[dict, list]:
        local_path = self.driver.download(path=path)
        with io.open(local_path) as fp:
            content = json.load(fp)

            if expression is None:
                return content

            result = _expression.jmespath_find_all(content, expression)
            return result

    def parquet(self, path: str, expression: Optional[str] = None, **kwargs) ->  Union[None, str, list, dict]:
        local_path = self.driver.download(path=path)
        from pandas import read_parquet

        df = read_parquet(local_path)
        content = df.to_dict('records')
        if expression is None:
            return content

        result = _expression.jmespath_find_all(content, expression)
        return result

    def text(self, path: str, expression: Optional[str] = None, flags: int = 0) -> str:
        """

        :param path:
        :param expression: regular expression in re.findall format
        :param flags: the regular expression’s behaviour can be modified by specifying a flags value (view https://docs.python.org/3/library/re.html#flags)
        :return:
        """
        local_path = self.driver.download(path=path)
        with io.open(local_path) as fp:
            content = fp.read()
            if expression is None:
                return content

            return _expression.re_find_all(content, expression, flags=flags)

    def yaml(self, path: str, expression: Optional[str] = None, Loader: Optional[Callable] = None) -> Union[dict, list]:
        """
        load a yaml file from disk and apply a jmespath expression to its contents.

        :param expression: jmespath expression
        :param Loader: pyyaml loader to use
        :return:
        """
        local_path = self.driver.download(path=path)
        with io.open(local_path) as fp:
            Loader = Loader if Loader is not None else  BaseLoader
            content = yaml.load(fp, Loader)

            if expression is None:
                return content

            result = _expression.jmespath_find_all(content, expression)
            return result
