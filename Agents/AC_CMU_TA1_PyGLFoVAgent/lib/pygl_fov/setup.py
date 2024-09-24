"""
"""

import setuptools

with open("README.md", "r") as readme_file:
	long_description = readme_file.read()

setuptools.setup(
	name="pygl_fov",
	version="0.3.6",
	author="Dana Hughes",
	author_email="danahugh@andrew.cmu.edu",
	description="Calculates blocks in a player's field of view in Minecraft",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/cmu_asist/pygl_fov",
	packages=setuptools.find_packages(include=["pygl_fov"]),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"operating System :: OS Independent",
	],
	python_requires=">=3.5",
#	package_dir={'': 'src'}
)
