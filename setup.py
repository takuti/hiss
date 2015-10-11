from setuptools import setup

setup(
    name='hiss',
    version='0.1',
    py_modules=['hiss'],
    install_requires=[
        'Click',
        'requests_oauthlib'
    ],
    entry_points='''
        [console_scripts]
        hiss=hiss:cli
    ''',
)
