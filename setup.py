#Create by Damien Gygi and Raphaël Schaffo
#INF2 DLM A
#HE ARC année 2015-2016

"""Sample Hammer Paper Scissors Slackbot"""

from setuptools import setup, find_packages

setup(
    name='HPSBot',
    version='0.0.1',
    description='A slack bot to play Hammer Scissors Paper.',
	url='https://github.com/DamienGygi/BotProject',
	author='Raphaël Schaffo and Damien Gygi',
    packages=find_packages(),
    install_requires=('aiohttp', 'asyncio','json'),
    extras_requires={
        'test': ('pytest', 'pytest-flake8', 'pytest-coverage'),
        'docs': ('Sphinx', 'sphinx_rtd_theme'),
    },
	license='MIT',
    packages=['hpsbot'],
    zip_safe=False
) 
