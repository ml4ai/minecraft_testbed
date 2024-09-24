# Copyright (c) 2017 Microsoft Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================================================================

# NB if building this on Windows/OSX, make sure Docker has been allowed enough memory - the default 2048Mb is not
# enough for the gradle Minecraft deobfuscation step.

FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# 16.04 image doesn't contain sudo - install that first:
RUN apt-get update && apt-get install -y sudo

# Create a user called "malmo", give it sudo access and remove the requirement for a password:
RUN useradd --create-home --shell /bin/bash --no-log-init --groups sudo malmo
RUN sudo bash -c 'echo "malmo ALL=(ALL:ALL) NOPASSWD: ALL" | (EDITOR="tee -a" visudo)'

# While we are still root, install the necessary dependencies for Malmo:
RUN sudo apt-get update && apt-get install -y build-essential 
RUN sudo apt-get update && apt-get install -y git 
RUN sudo apt-get update && apt-get install -y libpython3.6-dev 
#RUN sudo apt-get update && apt-get install -y openjdk-8-jdk 
# to fix a problem with a newer version of java being used on Ubuntu
RUN sudo apt-get update && apt-get install -y openjdk-8-jre-headless=8u162-b12-1
RUN sudo apt-get update && apt-get install -y openjdk-8-jre=8u162-b12-1
RUN sudo apt-get update && apt-get install -y openjdk-8-jdk-headless=8u162-b12-1
RUN sudo apt-get update && apt-get install -y openjdk-8-jdk=8u162-b12-1

RUN sudo apt-get update && apt-get install -y swig 
RUN sudo apt-get update && apt-get install -y doxygen 
RUN sudo apt-get update && apt-get install -y xsltproc 
RUN sudo apt-get update && apt-get install -y ffmpeg --fix-missing 
RUN sudo apt-get update && apt-get install -y python3-tk 
RUN sudo apt-get update && apt-get install -y python3-pil.imagetk 
RUN sudo apt-get update && apt-get install -y wget 
RUN sudo apt-get update && apt-get install -y libbz2-dev 
RUN sudo apt-get update && apt-get install -y python3-pip 
RUN sudo apt-get update && apt-get install -y software-properties-common 
RUN sudo apt-get update && apt-get install -y xpra 
RUN sudo apt-get update && apt-get install -y libgl1-mesa-dri 
RUN sudo apt-get update && apt-get install -y zlib1g-dev 
    

RUN sudo update-ca-certificates -f

# Note the trailing slash - essential!
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/" >> /home/malmo/.bashrc

# Switch to the malmo user:
USER malmo
WORKDIR /home/malmo

# BOOST:
RUN mkdir /home/malmo/boost
WORKDIR /home/malmo/boost
RUN wget http://sourceforge.net/projects/boost/files/boost/1.66.0/boost_1_66_0.tar.gz
RUN tar xvf boost_1_66_0.tar.gz
WORKDIR /home/malmo/boost/boost_1_66_0
RUN echo "using python : 3.6 : /usr/bin/python3 : /usr/include/python3.6 : /usr/lib ;" > /home/malmo/user-config.jam
RUN ./bootstrap.sh --prefix=.
RUN ./b2 link=static cxxflags=-fPIC install


# CMAKE:
RUN mkdir /home/malmo/cmake
WORKDIR /home/malmo/cmake
RUN wget https://cmake.org/files/v3.11/cmake-3.11.0.tar.gz
RUN tar xvf cmake-3.11.0.tar.gz
WORKDIR /home/malmo/cmake/cmake-3.11.0
RUN ./bootstrap
RUN make -j4 
RUN sudo make install 

# Python3 is currently is missing distutils
RUN sudo apt install -y python3-distutils 
RUN sudo -H pip3 install setuptools
RUN sudo -H pip3 install future pillow matplotlib

RUN sudo  apt-get update && sudo apt-get install -y dos2unix

COPY ./build.sh /home/malmo/build.sh
RUN sudo dos2unix /home/malmo/build.sh
ENV MALMO_XSD_PATH=/home/malmo/MalmoPlatform/Schemas

RUN cp /home/malmo/boost/boost_1_66_0/lib/libboost_python3.a /home/malmo/boost/boost_1_66_0/lib/libboost_python36.a 

RUN sudo chmod +x /home/malmo/build.sh
RUN sudo /home/malmo/build.sh -boost 1_66_0 -python 3.6 -no_testing 

RUN sudo apt-get update && sudo apt-get install -y xvfb x11vnc lsof

RUN sudo -H pip3 install malmoenv

RUN sudo apt-get install -y curl

RUN sudo apt-get install -y vim

RUN sudo -H pip3 install paho-mqtt

RUN sudo -H pip3 install asyncio

RUN sudo -H pip3 install requests

ARG CACHE_BREAKER


# ADD MQTT Client

RUN sudo mkdir -p /home/malmo/MalmoPlatform/build/install/Python_Examples/MQTTClient
COPY ./MQTTClient/RawConnection.py /home/malmo/MalmoPlatform/build/install/Python_Examples/MQTTClient/RawConnection.py
COPY ./MQTTClient/Connection.py /home/malmo/MalmoPlatform/build/install/Python_Examples/MQTTClient/Connection.py



# Add port listening shell script and curl
COPY ./getLanPortBash /home/malmo/getLanPortBash
RUN sudo chmod +x /home/malmo/getLanPortBash
RUN sudo dos2unix /home/malmo/getLanPortBash
COPY ./Heartbeat.py /home/malmo/Heartbeat.py
RUN sudo chmod 777 /home/malmo/Heartbeat.py
COPY ./services.txt /etc/services

# Add missions

COPY ./mdf_load_falcon.py /home/malmo/MalmoPlatform/build/install/Python_Examples/mdf_load_falcon.py
COPY ./Falcon  /home/malmo/MalmoPlatform/build/install/Python_Examples/Falcon

COPY ./mdf_load_sparky.py /home/malmo/MalmoPlatform/build/install/Python_Examples/mdf_load_sparky.py
COPY ./Sparky  /home/malmo/MalmoPlatform/build/install/Python_Examples/Sparky

COPY ./TestScript.py /home/malmo/MalmoPlatform/build/install/Python_Examples/TestScript.py

WORKDIR /home/malmo/MalmoPlatform/Minecraft
RUN sudo chmod +x ./launchClient.sh

CMD (../../getLanPortBash &) && (python3 ../../Heartbeat.py &) && (Xvfb :1 -screen 0 1400x900x24 &) && sleep 2 && (/usr/bin/x11vnc -display :1.0 &) && sleep 2 && export DISPLAY=:1.0 &&  sudo ./launchClient.sh -port 10000 



