import setuptools
from setup_utils import filter_deps

with open("README.md", "r") as readme_file:
	long_description = readme_file.read()

extras = {
	'MinecraftBridge': filter_deps([
		'MinecraftBridge @ git+https://gitlab.com/cmu_asist/MinecraftBridge@v1.3.1',
		'MinecraftElements @ git+https://gitlab.com/cmu_asist/MinecraftElements@v0.4.5'
	]),
	'RedisBridge': filter_deps([
		'RedisBridge @ git+https://gitlab.com/cmu_asist/RedisBridge@v1.1.3',
	]),
}

setuptools.setup(
	name="BaseAgent",
	version="0.1.3",
	author="Dana Hughes",
	author_email="danahugh@andrew.cmu.edu",
	description="Bridge to multiple interfaces to Minecraft",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/cmu_asist/BaseAgent",
	packages=setuptools.find_packages(),
	package_data={'BaseAgent': ['resources/*']},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"operating System :: OS Independent",
	],
	python_requires=">=3.6",
	install_requires=[
		'numpy',
	],
	extras_require={
		**extras,
		'all': list(set(sum(extras.values(), [])))
	}
)
