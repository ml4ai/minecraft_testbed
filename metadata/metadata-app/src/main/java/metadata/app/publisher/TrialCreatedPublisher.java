package metadata.app.publisher;

import io.micronaut.mqtt.annotation.Qos;
import io.micronaut.mqtt.annotation.Topic;
import io.micronaut.mqtt.v5.annotation.MqttPublisher;
import io.reactivex.Completable;

@MqttPublisher
public interface TrialCreatedPublisher {

	@Topic(value = "metadata/trial/created", qos = 1)
	Completable send(byte[] data);
	
	@Topic("metadata/trial/created")
	Completable send(byte[] data, @Qos int qos);
	
}
