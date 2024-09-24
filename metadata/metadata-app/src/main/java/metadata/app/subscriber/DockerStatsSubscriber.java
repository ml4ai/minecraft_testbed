package metadata.app.subscriber;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.MessageFormat;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import javax.inject.Inject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.dockerjava.api.async.ResultCallbackTemplate;
import com.github.dockerjava.api.model.Statistics;

import io.micronaut.context.annotation.Property;
import io.micronaut.mqtt.annotation.MqttSubscriber;
import io.micronaut.mqtt.annotation.Topic;
import metadata.app.model.Experiment;
import metadata.app.model.MessageTrial;
import metadata.app.model.Trial;
import metadata.app.service.DefaultTrialService;
import metadata.app.service.DockerService;


@MqttSubscriber
public class DockerStatsSubscriber {

	private static final Logger logger = LoggerFactory.getLogger(DockerStatsSubscriber.class);
	private ObjectMapper objectMapper = new ObjectMapper();
	
	@Property(name = "docker.statsCollection")
	private boolean DOCKER_STATS_COLLECTION;
    
    private final DockerService dockerService;

	@Inject
	public DockerStatsSubscriber(DockerService dockerService) {
		this.dockerService = dockerService;
	}

    @Topic("trial")
    public void receive(byte[] data) {
    	if (!DOCKER_STATS_COLLECTION)
    		return;
		   	
    	MessageTrial msgTrial;
		try {
			String message = new String(data, StandardCharsets.UTF_8);
			msgTrial = objectMapper.readValue(message, MessageTrial.class);

			String subType = msgTrial.getMsg().getSubType();
			
			if(subType.equals("start")) {			
		        
			}
			
			if(subType.equals("stop")) {			

			}
			
	
    	} catch (JsonMappingException e3) {
			// TODO Auto-generated catch block
			e3.printStackTrace();
		} catch (JsonProcessingException e3) {
			// TODO Auto-generated catch block
			e3.printStackTrace();
		}			
    }
}
