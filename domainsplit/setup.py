
import os
from distutils.core import setup
import py2exe

data_files = ['data/%s' % fname for fname in os.listdir('data')]

setup(
    author='Guilherme Starvaggi Franca',
    author_email='guifranca@gmail.com',
    description='Split domain names into words',
    fullname='domainsplit',
    url='http://www.gmake.com.br/project/domainsplit',
    license='GNU GPL v3 - http://www.gnu.org/licenses/gpl.html',
    name='domainsplit',
    version='0.1',
    scripts=['domainsplit'],
    data_files=[('share/domainsplit/data', data_files)],
    windows=['domainsplit']
)
