from setuptools import setup

setup(
    name='bookkeeping',
    version='0.0.0',
    description='Console bookkeeping.',
    license='Apache License 2.0',
    author='FrozRt',
    author_email='chigrin_m@mail.ru',
    packages=['bookkeeping'],
    entry_points={'console_scripts': ['bookkeeping = bookkeeping: main']},
    install_requires=['appdirs', 'prettytable', ],
    package_data={'bookkeeping': ['resources/*'], }
)
