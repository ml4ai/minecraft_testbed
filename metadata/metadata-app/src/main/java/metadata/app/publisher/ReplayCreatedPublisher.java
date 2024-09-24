package metadata.app.publisher;

import io.micronaut.mqtt.annotation.Qos;
import io.micronaut.mqtt.annotation.Topic;
import io.micronaut.mqtt.v5.annotation.MqttPublisher;
import io.reactivex.Completable;

@MqttPublisher
public interface ReplayCreatedPublisher {

	@Topic(value = "metadata/replay/created", qos = 1)
	Completable send(byte[] data);
	
	@Topic("metadata/replay/created")
	Completable send(byte[] data, @Qos int qos);
	
}
