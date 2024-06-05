import jmespath
import re
from typing import Union, List


def re_find_all(content: str, expression: str, flags: int = 0) -> Union[None, str, List[str]]:
    """
    finds all occurrences of a regular expression in the content

    >>> expression.re_find_all('hello world    ! world !', r'world[\s]*!')
    >>> ['world    !', 'world !']

    :param content:
    :param expression:
    :return:
    """
    match = re.findall(expression, content, flags=flags)
    if len(match) == 0:
        return None
    elif len(match) == 1:
        return match[0]
    else:
        return match


def jmespath_find_all(content: Union[dict, list], expression: str) -> Union[None, str, list, dict]:
    """

    >>> jmespath_find_all([{'hello', 'world'}], expression='[0]')

    :param content:
    :param expression:
    :return:
    """

    result = jmespath.search(expression, content)
    return result