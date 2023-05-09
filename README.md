# qload : better assertion on files

qload is a library to load or extract content of a file to perform assertion in automatic tests without
boilerplate. It support file from filesystem, ftp, s3, ...

## Benefits

* oneliner to assert on the content of a file
* useful differential when the test fails thanks to subpart extraction
* support for the most common formats (yaml, csv, json, txt)
* support for multiple file systems and protocols (local, ftp, s3)
* rich expression engine to extract part of a file ([regexp](https://docs.python.org/3/library/re.html#regular-expression-syntax) for `text` and [jmespath](https://jmespath.org) for `csv`, `json` and `yaml` to improve differential) 

## Gettings started

```bash
pip install qload
```

## Usage

```python
import qload

assert 'database_url: postgresql://127.0.0.1:5432/postgres' in qload.text('file.txt')
assert qload.text('file.txt', expression='Hello .*') == 'Hello Fabien'

assert qload.json('file.json') == {}
assert qload.json('s3://mybucket/file1.json') == {}
assert qload.json('file.json', expression='$.id') == ''
assert len(qload.json('file.json', expression='$.id')) == 4

assert qload.yaml('file.yml')  == {}
assert qload.yaml('file.yml', expression='$.id')  == ''

assert qload.csv('file.csv', expression='[*].Account') == ['ALK', 'BTL', 'CKL']
assert qload.csv('file.csv', expression='[*].Account')[0] == 'ALK'

assert qload.parquet('file.parquet', expression='[*].Account')[0] == 'ALK'

assert qload.ftp(host='localhost', port=21, login='admin', password='admin').csv(path='dir/file.csv', expression='') == []
assert qload.s3(bucket='bucket', aws_access_key_id='', aws_secret_access_key='', region_name='eu-west-1', endpoint_url='http://localhost:9090').json(path='dir/file.csv') == {}


assert qload.isfile('file.json') is True
assert qload.s3(bucket='bucket').isfile('file.json') is True
```