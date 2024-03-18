from setuptools import setup, find_packages

setup(
    name='seminar_registration_system',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django==4.2.11',
    ],
    python_requires='>=3.8',
    author='Mfundo Monchwe',
    description='A seminar registration system',
    author_email='diditmfundo@gmail.com'
)