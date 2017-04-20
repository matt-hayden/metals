from setuptools import find_packages, setup

setup(name='metals',
      use_vcs_version=True,
      description="List metadata on the command line, like ls",
      url='https://github.com/matt-hayden/metals',
	  maintainer="Matt Hayden",
	  maintainer_email="github.com/matt-hayden",
      license='Unlicense',
      packages=find_packages(),
	  entry_points = {
	    'console_scripts': [
		  'metals=metals.cli:main',
		],
	  },
      zip_safe=True,
	  setup_requires = [ "setuptools_git >= 1.2", ]
     )
