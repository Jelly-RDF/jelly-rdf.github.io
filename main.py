# See: https://mkdocs-macros-plugin.readthedocs.io/en/latest

import os
from pathlib import Path
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
        return f'https://github.com/Jelly-RDF/jelly-protobuf/blob/{tag}/{file}'
    

    @env.macro
    def git_docs_link(file: str):
        tag = git_tag()
        return f'https://github.com/Jelly-RDF/jelly-rdf.github.io/blob/{tag}/{file}'
    

    @env.macro
    def specification_status():
        return 'Draft' if git_tag() == 'main' else 'Stable'
    

    @env.macro
    def stax_version():
        return _stax_version
    

    @env.macro
    def stax_link(page: str = ''):
        return f'https://w3id.org/stax/{stax_version()}/{page}'

    
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
    def jvm_link(page: str = ''):
        version = jvm_version()
        return f'https://w3id.org/jelly/jelly-jvm/{version}/{page}'


    def transform_nav_item(item):
        if list(item.values())[0] == 'https://w3id.org/jelly/jelly-jvm/':
            return {list(item.keys())[0]: jvm_link('')}
        return item
    

    env.conf['nav'] = [
        transform_nav_item(item)
        for item in env.conf['nav']
    ]
