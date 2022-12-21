# qload : better assertion on files

qload is a library to load or extract content of a file to perform assertion in automatic tests wihtout
boilerplate. It support file from filesystem, ftp, s3, ...

## Benefits

* oneliner to assert on the content of a file
* useful differential when the test fails
* support for the most common formats (yaml, csv, json, txt, ...)
* support for multiple file systems and protocols (local, ftp, s3, ...)

## Gettings started

```bash
pip install qload
```

## Usage

```python
import qload

assert 'database_url: postgresql://127.0.0.1:5432/postgres' in qload.text('path')
assert qload.text('path', expression='database_url:.*') == 'database_url: postgresql://127.0.0.1:5432/postgres'

assert qload.json('file1.json') == {}
assert qload.json('s3://xxxxxx/file1.json') == {}
assert qload.json('path', expression='$.id') == ''
assert len(qload.json('path', expression='$.id')) == 4

assert qload.yaml('path')  == {}
assert qload.yaml('path', expression='$.id')  == ''

assert qload.csv('path', expression='$.id') == ''
assert qload.csv('path', expression='$.id') == ''

assert qload.ftp(login, password).csv(path='', expression='') == ''
assert qload.s3(access_key, access_secret).csv(path='', expression='') == ''
```