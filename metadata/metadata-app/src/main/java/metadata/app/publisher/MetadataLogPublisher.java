package metadata.app.publisher;

import io.micronaut.mqtt.annotation.Qos;
import io.micronaut.mqtt.annotation.Topic;
import io.micronaut.mqtt.v5.annotation.MqttPublisher;
import io.reactivex.Completable;

@MqttPublisher
public interface MetadataLogPublisher {

	@Topic(value = "metadata/log", qos = 1)
	//@MqttProperty(name = "contentType", value = "text/plain")
	Completable send(byte[] data);
	
	@Topic("metadata/log")
	//@MqttProperty(name = "contentType", value = "text/plain")
	Completable send(byte[] data, @Qos int qos);
	
}
