Local testbed docker build instructions
=======================================

Prerequisites
-------------

* Docker:
  * Docker (Linux) 19.03.11 or newer
  * docker-compose: 1.29.2  or newer
  * Python 3.7 or newer
  * An MQTT debugging tool for debugging ( MQTT Explorer is a good choice )


* The following files were compressed in the .7z format to save space in the repo and avoid the need for web mirrors - please extract these large files and folders before attempting to build the testbed:
  * Agents\AC_CMU_TA1_PyGLFoVAgent\ConfigFolder\maps.7z


## Build Options

### LINUX - PREFERRED AND MOST UP TO DATE
* Clone the repository if you have not done so - using the "main" branch
* login to the gitlab container registry using the following command:
     `docker login registry.gitlab.com/artificialsocialintelligence/study3/`
* Enter your GitLab username and password when prompted
* Navigate to the clone repo's Local directory.
* On Linux and MacOS, run the script `testbed_build.sh`.
* At this stage, certain docker images will build directly on your machine using docker commands, this may take some time for larger images
* Other images may be pulled at runtime from the gitlab image registry associated with this repository
* The testbed and associated containers is quite large, so set aside ~1hr for the build process
