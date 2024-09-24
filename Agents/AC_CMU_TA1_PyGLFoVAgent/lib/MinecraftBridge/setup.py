import setuptools
from setup_utils import filter_deps

with open("README.md", "r") as readme_file:
	long_description = readme_file.read()

extras = {
    'MinecraftElements': filter_deps([
        'MinecraftElements @ git+https://gitlab.com/cmu_asist/MinecraftElements@v0.4.5'
    ])
}

setuptools.setup(
	name="MinecraftBridge",
	version="1.3.6",
	author="Dana Hughes",
	author_email="danahugh@andrew.cmu.edu",
	description="Bridge to multiple interfaces to Minecraft",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/cmu_asist/MinecraftBridge",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"operating System :: OS Independent",
	],
	python_requires=">=3.6",
	install_requires=[
		'ciso8601',
		'paho-mqtt',
	],
	extras_require={
        **extras,
        'all': list(set(sum(extras.values(), [])))
    }
)
