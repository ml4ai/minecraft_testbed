"""
"""

import setuptools

# Load in the `README.md` file as the long description for the package.
# This makes updating easier, as it avoids needless copying of information
# between this and the top-level README file
with open("README.md", "r") as readme_file:
	long_description = readme_file.read()

setuptools.setup(
	name="MinecraftElements",
	version="0.4.6",
	author="Dana Hughes",
	author_email="danahugh@andrew.cmu.edu",
	description="Enumerations of Minecraft elements",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/cmu_asist/MinecraftElements",
	packages=setuptools.find_packages(include=["MinecraftElements"]),
	classifiers=[
		"Programming Language :: Python :: 3.5",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Indended Audience :: Science/Research",

	],
	python_requires=">=3.5",
#	package_dir={'': 'src'}
)
