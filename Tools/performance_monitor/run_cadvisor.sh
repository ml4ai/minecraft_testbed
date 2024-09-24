VERSION=v0.39.3 # use the latest release version from https://github.com/google/cadvisor/releases
sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --volume=/cgroup:/cgroup:ro \
  --publish=8086:8080 \
  --detach=true \
  --name=cadvisor \
  --privileged=true \
  gcr.io/cadvisor/cadvisor:$VERSION