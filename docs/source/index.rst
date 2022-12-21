qload : better assertion on files
=================================

qload is a library to load or extract content of a file to perform assertion in automatic tests without
boilerplate. qload can load a file locally or from remote storages like s3 or ftp.

Benefits
########

* oneliner to assert on the content of a file
* useful differential when the test fails
* support for the most common formats (yaml, csv, json, txt)
* support for multiple file systems and protocols (local, ftp, s3)
* rich expression engine to extract part of a file (`regexp <https://docs.python.org/3/library/re.html#regular-expression-syntax>`_ for `text` and `jmespath <https://jmespath.org/>`_ for `csv`, `json` and `yaml`)

Usage
#####

.. code-block:: python

    import qload

    assert 'database_url: postgresql://127.0.0.1:5432/postgres' in qload.text('file.txt')
    assert qload.text('file.txt', expression='Hello .*') == 'Hello Fabien'

    assert qload.json('file.json') == {}
    assert qload.json('s3://mybucket/file1.json') == {}
    assert qload.json('file.json', expression='$.id') == ''
    assert len(qload.json('file.json', expression='$.id')) == 4

    assert qload.yaml('file.yml')  == {}
    assert qload.yaml('file.yml', expression='$.id')  == ''

    assert qload.csv('file.csv', expression='$.id') == ''
    assert qload.csv('file.csv', expression='$.id') == ''

    assert qload.ftp(host='localhost', port=21, login='admin', password='admin').csv(path='dir/file.csv', expression='') == ''
    assert qload.s3(bucket='bucket1', access_key=access_key, access_secret=access_secret, endpoint='localhost').json(path='dir/file.csv', expression='') == ''

Installation
############

.. code-block::

    pip install qload

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
