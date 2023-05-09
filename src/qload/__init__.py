from typing import Optional, List, Union, Callable

from qload.driver import file, ftp, s3


def isfile(path: str, **kwargs) -> bool:
    return file().isfile(path=path, **kwargs)


def csv(path: str, expression: Optional[str] = None, **kwargs) ->  Union[None, str, list, dict]:
    """
    loads the content of a csv file and can filter it using jmespath expression to
    to make error display more explicit on the assertion.

    csv uses the csv.DictReader reader to parse and read the contents of the csv file
    into a dictionary list.

    >>> import qload
    >>>
    >>> assert qload.csv('/home/fabien/file.csv') == [{'account': 'BLD'}, {'account': 'ALK'}]
    >>> assert qload.csv('/home/fabien/file.csv', fieldnames = []) == [{'hello': 'world'}]
    >>> assert qload.csv('/home/fabien/file.csv', delimiter=';') == [{'account': 'BLD'}, {'account': 'ALK'}]

    :param path:
    :param expression: jmespath expression
    :return:
    """
    return file().csv(path=path, expression=expression, **kwargs)


def json(path: str, expression: Optional[str] = None) ->  Union[None, str, list, dict]:
    """
    loads the content of a json file and can filter it using jmespath expression
    to make error display more explicit on the assertion

    >>> import qload
    >>> assert qload.json('/home/fabien/file.json') == [{'hello': 'world'}]
    >>> assert qload.json('ftp://localhost:21/home/fabien/file.json', expression='[0]') == { 'hello' : 'world' }

    :param path:
    :param expression: jmespath expression
    :return:
    """
    return file().json(path=path, expression=expression)


def parquet(path:str, expression: Optional[str] = None) -> Union[None, str, list, dict]:
    """
    loads the content of a parquet file and can filter it using jmespath expression to
    to make error display more explicit on the assertion.

    pandas uses the pandas reader & pyarrow to parse and read the contents of the parquet file
    into a dictionary list.
    """
    return file().parquet(path=path, expression=expression)


def text(path: str, expression: Optional[str] = None, flags: int = 0) -> Union[str, List[str]]:
    """
    loads text from a file and can filter it through a regular expression
    to make the error displayed by an assertion more explicit.

    >>> import qload
    >>> assert qload.text('/home/fabien/file.txt') == "content"
    >>> assert qload.text('/home/fabien/file.txt', expression='Hello .*$') == "Hello fabien"
    >>> assert qload.text('ftp://localhost:21/home/fabien/file.txt') == "content"

    :param path:
    :param expression: regular expression in re.findall format
    :param flags: the regular expression’s behaviour can be modified by specifying a flags value (view https://docs.python.org/3/library/re.html#flags)
    :return:
    """
    return file().text(path=path, expression=expression, flags=flags)


def yaml(path: str, expression: Optional[str] = None, Loader: Optional[Callable] = None) ->  Union[None, str, list, dict]:
    """
    loads part of a yaml file and can filter it from a jmespath expression
    to make the assertion error display more explicit

    >>> import qload
    >>> assert qload.yaml('/home/fabien/file.yml') == [{'hello': 'world'}]
    >>> assert qload.yaml('ftp://localhost:21/home/fabien/file.yaml', expression='[0]') == { 'hello' : 'world' }

    :param path:
    :param expression: jmespath expression
    :return:
    """
    return file().yaml(path=path, expression=expression, Loader=Loader)