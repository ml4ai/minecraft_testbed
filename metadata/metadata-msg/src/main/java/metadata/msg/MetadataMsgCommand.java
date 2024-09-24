package metadata.msg;

import javax.inject.Inject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.micronaut.configuration.picocli.PicocliRunner;
import io.micronaut.context.ApplicationContext;
import io.micronaut.context.BeanContext;
import io.micronaut.runtime.server.EmbeddedServer;
import metadata.msg.client.MqttMessageClient;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;

@Command(name = "metadata-msg", description = "...",
        mixinStandardHelpOptions = true)
public class MetadataMsgCommand implements Runnable {

//    @Option(names = {"-l", "--listen"}, description = "Listen on the message bus for incoming messages.")
	@Inject
    ApplicationContext appContext;

	private static final Logger logger = LoggerFactory.getLogger(MqttMessageClient.class);
	
    public static void main(String[] args) throws Exception {
        PicocliRunner.run(MetadataMsgCommand.class, args);
    }

    public void run() {
    	// Since MqttMessageClient uses @Context it gets instantiated and there is a call to listen() in the constructor.

    	if (!appContext.isRunning()) { // future versions of PicocliRunner may start the context
            appContext.start();
        }

        // start the embedded server
        EmbeddedServer server = appContext.getBean(EmbeddedServer.class);
        if (!server.isRunning()) {
        	long start = System.currentTimeMillis();
            server.start();
        	long end = System.currentTimeMillis();
            long took = end - start;
            if (server.isRunning()) {
            	logger.info("Startup completed in {}ms. Server Running: {}", took, server.getURL().toString());
            }
        }
        
    	MqttMessageClient client = appContext.getBean(MqttMessageClient.class);
    	client.listen();
        
/*
 *      // business logic here
 *      if (listen) {
 *          final BeanContext context = BeanContext.run();
 *          MqttMessageClient client = context.createBean(MqttMessageClient.class);
 *          client.listen();                  
 *      }
*/
    	
    }
}
