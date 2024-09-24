@echo on

for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H

echo "updating the AC CMU TA1 PyGL FoV container"
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%time% .

echo "List the Docker containers"
docker ps
