package metadata.app;

import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.Appender;
import io.micronaut.context.ApplicationContext;
import io.micronaut.runtime.Micronaut;
import metadata.app.appender.MqttAppender;

public class Application {
	
    public static void main(String[] args) {
    	ApplicationContext context = Micronaut.run(Application.class);

    	LoggerContext loggerContext = (LoggerContext) LoggerFactory.getILoggerFactory();    	
    	MqttAppender mqttAppender = context.getBean(MqttAppender.class); //new MqttAppender();
    	mqttAppender.setContext(loggerContext);
    	
//    	MetadataLogClient metadataLogClient = context.getBean(MetadataLogClient.class);
//    	mqttAppender.setMetadataLogClient(metadataLogClient);

    	mqttAppender.start();
    	
    	Logger logbackLogger = (Logger) LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
    	logbackLogger.addAppender((Appender<ILoggingEvent>)mqttAppender);
    	logbackLogger.setAdditive(true);
    }
}