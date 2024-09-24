package metadata.app.publisher;

import io.micronaut.mqtt.annotation.Qos;
import io.micronaut.mqtt.annotation.Topic;
import io.micronaut.mqtt.v5.annotation.MqttPublisher;
import io.reactivex.Completable;

@MqttPublisher
public interface ReplayCompletedPublisher {

	@Topic(value = "metadata/replay/completed", qos = 1)
	Completable send(byte[] data);
	
	@Topic("metadata/replay/completed")
	Completable send(byte[] data, @Qos int qos);
	
}
