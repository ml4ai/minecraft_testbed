package metadata.msg.client;

import io.micronaut.context.annotation.Requires;
import io.micronaut.health.HealthStatus;
import io.micronaut.http.HttpRequest;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.client.RxHttpClient;
import io.micronaut.http.client.annotation.Client;
import io.micronaut.management.endpoint.health.HealthEndpoint;
import io.micronaut.management.health.indicator.HealthIndicator;
import io.micronaut.management.health.indicator.HealthResult;
import io.reactivex.Flowable;
import org.reactivestreams.Publisher;

import javax.inject.Inject;
import javax.inject.Singleton;
import java.util.Collections;
 
@Singleton
@Requires(property = HealthEndpoint.PREFIX + ".mqtt.client.enabled", value = "true")
@Requires(beans = HealthEndpoint.class)
public class MqttHealthIndicator implements HealthIndicator {
	/**
     * Name for health indicator.
     */
    private static final String NAME = "mqtt-client-health";
 
    /**
     * MqttClient to check.
     */
    @Inject
	private MqttMessageClient mqttMessageClient;
 
    /**
     * Implementation of {@link HealthIndicator#getResult()} where we
     * check if the url is reachable and return result based
     * on the HTTP status code.
     *
     * @return Contains {@link HealthResult} with status UP or DOWN.
     */
    @Override
    public Publisher<HealthResult> getResult() {
        final boolean statusOk = mqttMessageClient.isConnected();
        final HealthStatus healthStatus = statusOk ? HealthStatus.UP : HealthStatus.DOWN;

        HealthResult healthResult = HealthResult.builder(NAME, healthStatus)
        										.details(Collections.singletonMap("class", mqttMessageClient.getClass().toString()))
        										.build();
    	return Flowable.just(healthResult);
    }
}