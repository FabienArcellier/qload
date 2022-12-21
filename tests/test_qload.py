import os

import qload
import fixtup


def test_csv_should_load_file_content():
    with fixtup.up('files'):
        assert len(qload.csv('file.csv')) == 3


def test_csv_should_load_file_content_and_filter_by_expression():
    with fixtup.up('files'):
        assert qload.csv('file.csv', expression='[*].Account') == ['ALK', 'BTL', 'CKL']


def test_ftp_should_load_file_content_and_perform_expression_filter():
    with fixtup.up('ftp'):
        assert qload.ftp(user='admin', passwd='admin').text('file.txt', expression='Hello .*') == 'Hello fabien'


def test_ftp_should_load_file_content_and_perform_expression_filter_on_specific_port():
    with fixtup.up('ftp_p210'):
        assert qload.ftp(user='admin', passwd='admin', port=210).text('file.txt', expression='Hello .*') == 'Hello fabien'


def test_json_should_load_json_and_match_content():
    with fixtup.up('files'):
        dir = os.getcwd()
        assert [{'hello': 'world'}] == qload.json(os.path.join(dir, 'file.json'))


def test_json_should_load_text_and_trigger_exception():
    with fixtup.up('files'):
        try:
            dir = os.getcwd()
            assert 'database_url: postgresql://127.0.0.1:543/postgres' not in qload.text(os.path.join(dir, 'file.yml'))
        except BaseException as exception:
            pass


def test_text_should_load_text_and_match_content():
    with fixtup.up('files'):
        dir = os.getcwd()
        assert 'database_url: postgresql://127.0.0.1:5432/postgres' in qload.text(os.path.join(dir, 'file.yml'))


def test_text_should_load_text_and_match_content_with_expression():
    with fixtup.up('files'):
        dir = os.getcwd()
        assert 'database_url: postgresql://127.0.0.1:5432/postgres' == qload.text(os.path.join(dir, 'file.yml'), expression='database_url: .*')


def test_text_should_return_none_when_expression_match_nothing():
    with fixtup.up('files'):
        dir = os.getcwd()
        assert qload.text(os.path.join(dir, 'file.yml'), expression='youp: .*') is None


def test_yaml_should_load_yaml():
    with fixtup.up('files'):
        dir = os.getcwd()
        assert 'postgresql://127.0.0.1:5432/postgres' == qload.yaml(os.path.join(dir, 'file.yml'))['database_url']


def test_yaml_should_load_yaml_and_apply_expression():
    with fixtup.up('files'):
        dir = os.getcwd()
        assert 'postgresql://127.0.0.1:5432/postgres' == qload.yaml(os.path.join(dir, 'file.yml'), expression='database_url')


def test_yaml_should_load_yaml_and_apply_expression_and_raise_assert():
    with fixtup.up('files'):
        try:
            dir = os.getcwd()
            assert 'postgresql://127.0.0.1:543/postgres' == qload.yaml(os.path.join(dir, 'file.yml'), expression='database_url')
            assert False, 'it should raise an error'
        except AssertionError as exception:
            pass