
from setuptools import setup, find_packages

#extras = {}

setup(
	name='crone', 
	version='0.0.1', 
	url='https://github.com/alice-tr/crone', 
	author='Alice Turk-Raleigh', 
	#author_email='name@domain', 
	description='Auspicious command scheduling', 
	packages=find_packages(), 
	install_requires=[
		'flatlib==0.2.3', 
		
		# TODO refactor these into "extras"
		'docopt-ng==0.7.2', 
		'inquirer==2.7.0', 
		'pendulum==2.1.2', 
	], 
	#extras_require=extras, 
)
