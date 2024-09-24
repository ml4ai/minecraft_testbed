package metadata.app.appender;

import java.text.DateFormat;
import java.text.MessageFormat;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Base64.Encoder;
import java.util.Date;

import javax.inject.Inject;
import javax.inject.Singleton;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.UnsynchronizedAppenderBase;
import metadata.app.model.LogMessage;
import metadata.app.publisher.MetadataLogPublisher;

@Singleton
public class MqttAppender extends UnsynchronizedAppenderBase<ILoggingEvent> { //UnsynchronizedAppenderBase
	
	@Inject
	private MetadataLogPublisher metadataLogClient;
	
	private ObjectMapper objectMapper = new ObjectMapper();
    
	@Override
	protected void append(ILoggingEvent eventObject) {
        String event = format(eventObject);        

    	Encoder encoder = Base64.getEncoder();
    	String encodedString = encoder.encodeToString(event.getBytes());
    	
    	LogMessage logMessage = new LogMessage(encodedString);

        if (metadataLogClient != null) {
    		try {
				this.metadataLogClient.send(objectMapper.writeValueAsBytes(logMessage)).subscribe(() -> {
				    // handle completion
				}, throwable -> {
				    // handle error
				});
			} catch (JsonProcessingException e) {
				addError(e.getMessage());
				e.printStackTrace();
			}       	
        }
        else {
        	System.out.println("MetadataLogClient is null!");
        	addError("MetadataLogClient is null!");
        }        	
		
	}

	// private final int DEFAULT_BUFFER_SIZE = 512;
    private DateFormat df = new SimpleDateFormat("HH:mm:ss.SSS");

    private String format(ILoggingEvent event) {    	
        return MessageFormat.format("{0} [{1}] {2} {3} - {4}",
        		df.format(new Date(event.getTimeStamp())),
        		event.getThreadName(),
        		event.getLevel().toString(),
        		event.getLoggerName(),
        		event.getFormattedMessage()
        		);
    }
}
