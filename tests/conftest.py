import os
import yaml
import pytest


crawl_names = []
crawls = []

def pytest_addoption(parser):
    default_file = os.path.join(os.path.dirname(__file__), 'crawl_tests.yaml')
    parser.addoption('--crawl-file', action='store', default=default_file)
    parser.addoption('--run-only', action='store', default='')


def pytest_generate_tests(metafunc):
    if 'crawl' in metafunc.fixturenames:
        init_crawl_data(metafunc.config.getoption('--crawl-file'),
                        metafunc.config.getoption('--run-only'))

        metafunc.parametrize('crawl', crawls,
                             ids=crawl_names,
                             scope='class')

def init_crawl_data(filename, run_only):
    """ Load the crawl YAML
    """
    global crawl_names
    global crawls
    if crawl_names and crawls:
        return

    run_only_list = run_only.split(',') if run_only else None

    crawls_root = None
    with open(filename) as fh:
        crawls_root = yaml.safe_load(fh.read())

    for crawl in crawls_root['crawls']:
        if crawl.get('skip'):
            continue

        if run_only_list and crawl['name'] not in run_only_list:
            continue

        crawl_names.append(crawl['name'])
        crawls.append(crawl)

