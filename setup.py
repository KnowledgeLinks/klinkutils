__author__ = ",".join([ "KnowledgeLinks", "Jeremy Nelson", "Mike Stabile"])
__author_email__ = ','.join(['knowledgelinks.io@gmail.com',
                             'jermnelson@gmail.com',
                             'mstabile75@gmail.com'
                            ])
__license__ = "GPLv3"
__version__ = "1.0.1"

from setuptools import find_packages, setup

def readme():
    readme = ''
    try:
        with open('README.md') as rm_fo:
            readme = rm_fo.read()
    except FileNotFoundError:
        readme = "Not set"
    return readme


setup(
    name='klinkutils',
    version= __version__,
    author=__author__,
    author_email= __author_email__,
    description="Python utilities bundle",
    long_description=readme(),
    keywords='utilities colors',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'colorama'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Utilities",
        "Topic :: Cconsole :: formatting"
    ],
    url='https://github.com/KnowledgeLinks/klinkutils/tree/master',
    # test_suite='nose.collector',
    # tests_require=['nose', 'nose-cover3'],
    zip_safe=False
)
