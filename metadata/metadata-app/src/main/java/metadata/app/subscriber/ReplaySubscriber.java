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
import metadata.app.model.MessageReplay;
import metadata.app.model.Replay;
import metadata.app.service.DefaultReplayService;


@MqttSubscriber
public class ReplaySubscriber {

	private static final Logger logger = LoggerFactory.getLogger(ReplaySubscriber.class);
	private ObjectMapper objectMapper = new ObjectMapper();
    
    private final DefaultReplayService defaultReplayService;

	@Inject
	public ReplaySubscriber(DefaultReplayService defaultReplayService) {
		this.defaultReplayService = defaultReplayService;
	}

	@Topic("replay")
    public void receive(byte[] data) {  
	   	
    	MessageReplay msgReplay;
		try {
			String message = new String(data, StandardCharsets.UTF_8);			
			msgReplay = objectMapper.readValue(message, MessageReplay.class);
			
			Replay replay = new Replay(
					-1,
					msgReplay.getMsg().getReplayId(),
					msgReplay.getMsg().getReplayParentId(),
					msgReplay.getMsg().getReplayParentType(),
					msgReplay.getMsg().getTimestamp(),
					msgReplay.getData().getIgnoreMessageList(),
					msgReplay.getData().getIgnoreSourceList(),
					msgReplay.getData().getIgnoreTopicList()
					);
			
			Replay newReplay = defaultReplayService.createReplay(replay);
			if (newReplay != null) {
				logger.info(MessageFormat.format("Replay {0} created over message bus.", newReplay.getReplayId()));
			} else {
				logger.info(MessageFormat.format("Replay {0} could not be created over message bus.", replay.getReplayId()));
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
