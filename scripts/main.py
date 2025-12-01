# See: https://mkdocs-macros-plugin.readthedocs.io/en/latest

import os
from pathlib import Path
from scripts.generate_test_table import generate_test_table
from scripts.generate_report import generate_conformance_report
import re


def define_env(env):

    try:
        with open(Path(os.environ.get('PROTO_PATH'), 'rdf.proto'), 'r') as file:
            # Find the version of RDF-STaX
            _stax_version = re.search(r'https://w3id.org/stax/(\d+\.\d+\.\d+)', file.read()).group(1)
    except Exception as e:
        print('Warning: Failed to read RDF-STaX version, using dev as the default: ', e)
        _stax_version = 'dev'

    @env.macro
    def proto_version():
        tag = os.environ.get('TAG', 'dev')
        if tag == 'dev':
            print('Warning: TAG env var is not set, using dev as default')
            return tag
        elif tag == 'main':
            return 'dev'
        else:
            return tag.replace('v', '')
    
    
    @env.macro
    def git_tag():
        return os.environ.get('TAG', 'main')
        
    
    @env.macro
    def git_proto_link(file: str):
        tag = git_tag()
        return f'https://github.com/Jelly-RDF/jelly-protobuf/blob/{tag}/proto/{file}'
    

    @env.macro
    def git_test_link(file: str):
        tag = git_tag()
        return f'https://github.com/Jelly-RDF/jelly-protobuf/blob/{tag}/test/{file}'


    @env.macro
    def git_docs_link(file: str):
        tag = git_tag()
        return f'https://github.com/Jelly-RDF/jelly-rdf.github.io/blob/{tag}/{file}'
    

    @env.macro
    def git_tree_link(subdir: str = ''):
        return f'https://github.com/Jelly-RDF/jelly-rdf.github.io/{subdir}'
    

    @env.macro
    def specification_status():
        return 'Draft specification *(use the version selector on the top bar to find a stable specification)*' if (
            git_tag() == 'main'
        ) else f'Stable specification ({proto_version()})'

    @env.macro
    def stax_version():
        return _stax_version
    

    @env.macro
    def stax_link(page: str = ''):
        return f'https://w3id.org/stax/{stax_version()}/{page}'


    @env.macro
    def python_version():
        tag = os.environ.get('PYTHON_TAG', 'dev')
        if tag == 'dev':
            print('Warning: PYTHON_TAG env var is not set, using dev as default')
            return tag
        elif tag == 'main':
            return 'dev'
        else:
            return tag.replace('v', '')

    @env.macro
    def python_link(page: str = ''):
        version = python_version()
        return f'https://w3id.org/jelly/pyjelly/{version}/{page}'

    
    @env.macro
    def jvm_version():
        tag = os.environ.get('JVM_TAG', 'dev')
        if tag == 'dev':
            print('Warning: JVM_TAG env var is not set, using dev as default')
            return tag
        elif tag == 'main':
            return 'dev'
        else:
            return tag.replace('v', '')


    @env.macro
    def jvm_latest_release():
        tag = jvm_version()
        if tag == 'dev':
            tag = os.environ.get('JVM_LATEST_RELEASE', 'dev')
            if tag == 'dev' and len(os.environ.get('CI', '')) > 0:
                raise ValueError('JVM_LATEST_RELEASE env var is not set, but it is required in CI')
            tag = tag.replace('v', '')
        return tag


    @env.macro
    def jvm_link(page: str = ''):
        version = jvm_version()
        return f'https://w3id.org/jelly/jelly-jvm/{version}/{page}'


    def transform_nav_item(item):
        if list(item.values())[0] == 'https://w3id.org/jelly/jelly-jvm/':
            return {list(item.keys())[0]: jvm_link('')}
        if list(item.values())[0] == 'https://w3id.org/jelly/pyjelly/':
            return {list(item.keys())[0]: python_link('')}
        return item
    

    env.conf['nav'] = [
        transform_nav_item(item)
        for item in env.conf['nav']
    ]


    @env.macro
    def conformance_tests():
        return generate_test_table()


    @env.macro
    def conformance_report():
        return generate_conformance_report()
