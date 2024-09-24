package metadata.app.subscriber;

import java.nio.charset.StandardCharsets;
import java.text.MessageFormat;
import javax.inject.Inject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.mqtt.annotation.MqttSubscriber;
import io.micronaut.mqtt.annotation.Topic;
import metadata.app.model.Experiment;
import metadata.app.model.MessageExperiment;
import metadata.app.service.DefaultExperimentService;


@MqttSubscriber
public class ExperimentSubscriber {

	private static final Logger logger = LoggerFactory.getLogger(ExperimentSubscriber.class);
	private ObjectMapper objectMapper = new ObjectMapper();
	    
    private final DefaultExperimentService defaultExperimentService;

	@Inject
	public ExperimentSubscriber(DefaultExperimentService defaultExperimentService) {
		this.defaultExperimentService = defaultExperimentService;
	}

    @Topic("experiment")
    public void receive(byte[] data) {  
    	
    	MessageExperiment msgExperiment;
		try {
			String message = new String(data, StandardCharsets.UTF_8);			
			msgExperiment = objectMapper.readValue(message, MessageExperiment.class);
			
			Experiment experiment = new Experiment(
					-1,
					msgExperiment.getMsg().getExperimentId(),
					msgExperiment.getData().getName(),
					msgExperiment.getData().getDate(),
					msgExperiment.getData().getAuthor(),
					msgExperiment.getData().getMission()
					);
			
			Experiment newExperiment = defaultExperimentService.createExperiment(experiment);
			if (newExperiment != null) {
				logger.info(MessageFormat.format("Experiment {0} created over message bus.", newExperiment.getExperimentId()));
			} else {
				logger.info(MessageFormat.format("Experiment {0} could not be created over message bus.", experiment.getExperimentId()));
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
