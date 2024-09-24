FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./dist/metadata-web/. /usr/share/nginx/html
COPY ./dist/metadata-web/streamsaver/. /usr/share/StreamSaver.js
COPY ./certs/gitlab.asist.aptima.com.crt /etc/nginx/certs/asist/gitlab.asist.aptima.com.crt
COPY ./certs/gitlab.asist.aptima.com.key /etc/nginx/certs/asist/gitlab.asist.aptima.com.key