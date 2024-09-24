FROM mcr.microsoft.com/dotnet/core/aspnet:2.1 

COPY ./docker-20.10.9.tgz /docker-20.10.9.tgz

WORKDIR /

RUN tar -xvzf docker-20.10.9.tgz
RUN cp ./docker/docker ./usr/bin

RUN mkdir -p /usr/local/lib/docker/cli-plugins
RUN curl -SL https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
RUN chmod -R 777 /usr/local/lib/docker/cli-plugins

ARG CACHE_BREAKER

COPY MalmoControl/MalmoControl/bin/Debug/netcoreapp2.1/publish home/MalmoControl

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /home/MalmoControl

RUN chmod -R 777 .

RUN umask 000 .

ENTRYPOINT [ "dotnet", "MalmoControl.dll" ]