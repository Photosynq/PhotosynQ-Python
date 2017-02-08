import sys
if sys.version_info < (3,0):
    sys.exit('Sorry, Python < 3.0 is not supported')

from setuptools import setup, find_packages
setup(
    name = "photosynq_py",
    version = "0.6",
    packages = ['photosynq_py'],
    test_suite = 'tests',

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['numpy','pandas'],

    #package_data = {
    #    # If any package contains *.txt or *.rst files, include them:
    #    '': ['*.txt', '*.rst'],
    #    # And include any *.msg files found in the 'hello' package, too:
    #    'hello': ['*.msg'],
    #},

    # could also include long_description, download_url, classifiers, etc.
)
