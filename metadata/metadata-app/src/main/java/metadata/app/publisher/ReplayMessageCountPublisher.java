package metadata.app.publisher;

import io.micronaut.mqtt.annotation.Qos;
import io.micronaut.mqtt.annotation.Topic;
import io.micronaut.mqtt.v5.annotation.MqttPublisher;
import io.reactivex.Completable;

@MqttPublisher
public interface ReplayMessageCountPublisher {

	@Topic(value = "metadata/replay/message/count", qos = 1)
	Completable send(byte[] data);
	
	@Topic("metadata/replay/message/count")
	Completable send(byte[] data, @Qos int qos);
	
}
