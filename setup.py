from setuptools import setup, find_packages

setup(
    name='fitxatge',
    version='0.1.0',
    description='Sistema fitxatge per Microblau',
    url='https://github.com/spintog/fitxatge',
    author='Sergi Pinto',
    author_email='sergi@eslinux.org',
    license='GPL',
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['rq=src.main:display_quote']
    )
)