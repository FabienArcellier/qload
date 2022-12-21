from typing import Optional, List, Union

from qload.driver import file, ftp


def json(path: str, expression: Optional[str] = None) ->  Union[None, str, list, dict]:
    """
    loads part of a json file and can filter it from a jmespath expression
    to make the assertion error display more explicit

    >>> import qload
    >>> assert qload.json('/home/fabien/file.json') == [{'hello': 'world'}]
    >>> assert qload.json('ftp://localhost:21/home/fabien/file.json', expression='[0]') == { 'hello' : 'world' }

    :param path:
    :param expression: jmespath expression
    :return:
    """
    return file().json(path=path, expression=expression)


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


def yaml(path: str, expression: Optional[str] = None) ->  Union[None, str, list, dict]:
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
    return file().yaml(path=path, expression=expression)