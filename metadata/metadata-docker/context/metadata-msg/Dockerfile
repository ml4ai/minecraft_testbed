FROM adoptopenjdk/openjdk13-openj9:jdk-13.0.2_8_openj9-0.18.0-alpine-slim
COPY context/metadata-msg/metadata-msg-*.jar metadata-msg.jar
CMD java -Dcom.sun.management.jmxremote -noverify ${JAVA_OPTS} -jar metadata-msg.jar