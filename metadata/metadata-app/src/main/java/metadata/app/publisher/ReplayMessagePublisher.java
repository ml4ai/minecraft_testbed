package metadata.app.publisher;

import io.micronaut.mqtt.annotation.Qos;
import io.micronaut.mqtt.annotation.Topic;
import io.micronaut.mqtt.v5.annotation.MqttPublisher;
import io.reactivex.Completable;

@MqttPublisher
public interface ReplayMessagePublisher {

	Completable send(byte[] data, @Topic String topic);
	
	Completable send(byte[] data, @Topic String topic, @Qos int qos);
	
}
