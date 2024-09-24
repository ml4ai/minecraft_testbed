package metadata.app.health;

import io.micronaut.context.annotation.Requires;
import io.micronaut.health.HealthStatus;
import io.micronaut.management.endpoint.health.HealthEndpoint;
import io.micronaut.management.health.indicator.HealthIndicator;
import io.micronaut.management.health.indicator.HealthResult;
import io.reactivex.Flowable;

import org.eclipse.paho.mqttv5.client.MqttAsyncClient;
import org.reactivestreams.Publisher;

import javax.inject.Singleton;
import java.util.Collections;

/**
 * A {@link HealthIndicator} for Mqtt Client.
 *
 */
@Requires(property = HealthEndpoint.PREFIX + ".mqtt.client.enabled", value = "true")
@Requires(beans = HealthEndpoint.class)
@Singleton
public class MqttHealthIndicator implements HealthIndicator {
	public static final String NAME = "mqtt-client";
	private MqttAsyncClient client;

	/**
	 * Constructor.
	 *
	 * @param client MqttAsyncClient.
	 */
	public MqttHealthIndicator(MqttAsyncClient client) {
		this.client = client;
	}

	@Override
	public Publisher<HealthResult> getResult() {
//		HealthStatus status = HealthStatus.DOWN;		
//		if (client != null) {
//			status = client.isConnected() ? HealthStatus.UP : HealthStatus.DOWN;
//		}
		HealthStatus status = client.isConnected() ? HealthStatus.UP : HealthStatus.DOWN;
		HealthResult.Builder builder = HealthResult.builder(NAME, status).details(Collections.singletonMap("class", client.getClass().getName()));
		return Flowable.just(builder.build());
	}
}