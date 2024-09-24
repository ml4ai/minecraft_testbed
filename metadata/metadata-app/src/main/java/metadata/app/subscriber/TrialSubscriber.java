package metadata.app.subscriber;

import java.nio.charset.StandardCharsets;
import java.text.MessageFormat;
import java.util.UUID;

import javax.inject.Inject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.mqtt.annotation.MqttSubscriber;
import io.micronaut.mqtt.annotation.Topic;
import metadata.app.model.Experiment;
import metadata.app.model.MessageTrial;
import metadata.app.model.Trial;
import metadata.app.service.DefaultTrialService;


@MqttSubscriber
public class TrialSubscriber {

	private static final Logger logger = LoggerFactory.getLogger(TrialSubscriber.class);
	private ObjectMapper objectMapper = new ObjectMapper();
    
    private final DefaultTrialService defaultTrialService;

	@Inject
	public TrialSubscriber(DefaultTrialService defaultTrialService) {
		this.defaultTrialService = defaultTrialService;
	}

    @Topic("trial")
    public void receive(byte[] data) {  
		   	
    	MessageTrial msgTrial;
		try {
			String message = new String(data, StandardCharsets.UTF_8);
			msgTrial = objectMapper.readValue(message, MessageTrial.class);

			String subType = msgTrial.getMsg().getSubType();
			String source = msgTrial.getMsg().getSource();
			
			if(subType.equals("create") || subType.equals("start")) {			
				// Only create trials if they are not replays.
				if (!isUUID(msgTrial.getMsg().getReplayId())) {	
					logger.info(MessageFormat.format("Message bus request from {0} to {1} trial [{2}].", source, subType, msgTrial.getMsg().getTrialId()));
					// Just need to pass in the id. This came from the control so id is expected to be correct.
					// No need to query to make sure id exists.
					Experiment tempExperiment = new Experiment(-1l, msgTrial.getMsg().getExperimentId(), msgTrial.getData().getExperimentName(), msgTrial.getData().getExperimentDate(), msgTrial.getData().getExperimentAuthor(), msgTrial.getData().getExperimentMission());
					Trial trial = new Trial(
						-1,
						msgTrial.getMsg().getTrialId(),
						msgTrial.getData().getName(),
						msgTrial.getData().getDate(),
						msgTrial.getData().getExperimenter(),
						msgTrial.getData().getSubjects(),
						msgTrial.getData().getTrialNumber(),
						msgTrial.getData().getGroupNumber(),
						msgTrial.getData().getStudyNumber(),
						msgTrial.getData().getCondition(),
						msgTrial.getData().getNotes(),
						msgTrial.getData().getTestbedVersion(),
						tempExperiment
						);
					
					Trial newTrial = defaultTrialService.createTrial(trial);
					if (newTrial != null) {
						logger.info(MessageFormat.format("Trial {0} created over message bus.", newTrial.getTrialId()));
					} else {
						logger.info(MessageFormat.format("Trial {0} could not be created over message bus.", trial.getTrialId()));
					}
				}
			}
	
    	} catch (JsonMappingException e3) {
			// TODO Auto-generated catch block
			e3.printStackTrace();
		} catch (JsonProcessingException e3) {
			// TODO Auto-generated catch block
			e3.printStackTrace();
		}			
    }
    
    private boolean isUUID(String value) {
		if (value != null) {
			try {
				UUID.fromString(value.toString());
				return true;
			} catch (Exception e) {
				return false;
			}
		}
		return false;
	}
}
