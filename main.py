# See: https://mkdocs-macros-plugin.readthedocs.io/en/latest

import os


def define_env(env):

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
        return f'https://jelly-rdf.github.io/jelly-jvm/{version}/{page}'


    def transform_nav_item(item):
        if list(item.values())[0] == 'https://jelly-rdf.github.io/jelly-jvm/':
            return {list(item.keys())[0]: jvm_link('')}
        return item
    

    env.conf['nav'] = [
        transform_nav_item(item)
        for item in env.conf['nav']
    ]
