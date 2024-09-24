package metadata.msg.client;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import javax.inject.Inject;
import javax.inject.Singleton;

import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttAsyncClient;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.context.annotation.Context;
import io.micronaut.http.HttpRequest;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.client.RxHttpClient;
import io.micronaut.http.client.exceptions.HttpClientResponseException;
import io.reactivex.Flowable;
import metadata.msg.config.MqttConfigurationProperties;
import metadata.msg.model.Experiment;
//import metadata.msg.model.MqttExperiment;
//import metadata.msg.model.MqttTrial;
import metadata.msg.model.MsgExperiment;
import metadata.msg.model.MsgTrial;
import metadata.msg.model.Trial;

@Singleton
public class MqttMessageClient implements MqttCallback {

	private static final Logger logger = LoggerFactory.getLogger(MqttMessageClient.class);

	int state = BEGIN;

	static final int BEGIN = 0;
	static final int CONNECTED = 1;
	static final int PUBLISHED = 2;
	static final int SUBSCRIBED = 3;
	static final int DISCONNECTED = 4;
	static final int FINISH = 5;
	static final int ERROR = 6;
	static final int DISCONNECT = 7;

	// Private instance variables
	private MqttAsyncClient client;
	private String brokerUrl;
	private String clientId;
	private List<String> topic;
	private List<Integer> qos;
	private boolean verbose;
	private MqttConnectOptions options;
	private boolean clean;
	private String metadataApiUrl;
	private Throwable ex = null;
	private Object waiter = new Object();
	private boolean donext = false;
	private String password;
	private String userName;
	private ObjectMapper objectMapper = new ObjectMapper();

	private final MqttConfigurationProperties mqtt;

	/**
	 * Constructs an instance of the sample client wrapper
	 * 
	 * @param brokerUrl    the url to connect to
	 * @param clientId     the client id to connect with
	 * @param cleanSession clear state at end of connection or not (durable or
	 *                     non-durable subscriptions)
	 * @param quietMode    whether debug should be printed to standard out
	 * @param userName     the username to connect with
	 * @param password     the password for the user
	 * @throws MqttException
	 */

	public MqttMessageClient(MqttConfigurationProperties mqttConfigurationProperties) throws MqttException {
		this.mqtt = mqttConfigurationProperties;

		logger.info("Mqtt message bus client initializing.");

		this.topic = this.mqtt.getTopic();
		this.qos = this.mqtt.getQos();

		this.brokerUrl = this.mqtt.getBrokerUrl();
		this.clientId = this.mqtt.getClientId();
		this.verbose = this.mqtt.isVerbose();
		this.clean = this.mqtt.isCleanSession();
		this.metadataApiUrl = this.mqtt.getMetadataApiUrl();
		this.password = null;
		this.userName = null;
		// This sample stores in a temporary directory... where messages temporarily
		// stored until the message has been delivered to the server.
		// ..a real application ought to store them somewhere
		// where they are not likely to get deleted or tampered with
		// String tmpDir = System.getProperty("java.io.tmpdir");
		// MqttDefaultFilePersistence persistence = new
		// MqttDefaultFilePersistence(tmpDir);
		MemoryPersistence persistence = new MemoryPersistence();

		try {
			// Construct the object that contains connection parameters
			// such as cleanSession and LWT
			options = new MqttConnectOptions();
			options.setCleanSession(clean);
			options.setAutomaticReconnect(true);
			if (password != null) {
				options.setPassword(this.password.toCharArray());
			}
			if (userName != null) {
				options.setUserName(this.userName);
			}

			// Construct the MqttClient instance
			client = new MqttAsyncClient(this.brokerUrl, clientId, persistence);

			// Set this wrapper as the callback handler
			client.setCallback(this);

			// listen();

		} catch (MqttException e) {
			e.printStackTrace();
			log("Unable to set up client: " + e.toString());
			System.exit(1);
		}
	}

	public void listen() {
		try {
			this.subscribe(topic, qos);
		} catch (Throwable th) {
			log("Throwable caught " + th);
			// th.printStackTrace();
		}
	}

	public boolean isConnected() {
		if (client != null) {
			return client.isConnected();
		} else {
			return false;
		}
	}

	public void disconnect() {
		state = DISCONNECT;
		donext = true;
		log("Initiating disconnect.");
	}

	/**
	 * Publish / send a message to an MQTT server
	 * 
	 * @param topicName the name of the topic to publish to
	 * @param qos       the quality of service to delivery the message at (0,1,2)
	 * @param payload   the set of bytes to send to the MQTT server
	 * @throws MqttException
	 */
	public void publish(String topicName, int qos, byte[] payload) throws Throwable {
		// Use a state machine to decide which step to do next. State change occurs
		// when a notification is received that an MQTT action has completed
		while (state != FINISH) {
			switch (state) {
			case BEGIN:
				// Connect using a non-blocking connect
				MqttConnector con = new MqttConnector();
				con.doConnect();
				break;
			case CONNECTED:
				// Publish using a non-blocking publisher
				Publisher pub = new Publisher();
				pub.doPublish(topicName, qos, payload);
				break;
			case PUBLISHED:
				state = DISCONNECT;
				donext = true;
				break;
			case DISCONNECT:
				Disconnector disc = new Disconnector();
				disc.doDisconnect();
				break;
			case ERROR:
				throw ex;
			case DISCONNECTED:
				state = FINISH;
				donext = true;
				break;
			}

			// if (state != FINISH) {
			// Wait until notified about a state change and then perform next action
			waitForStateChange(10000);
			// }
		}
	}

	/**
	 * Wait for a maximum amount of time for a state change event to occur
	 * 
	 * @param maxTTW maximum time to wait in milliseconds
	 * @throws MqttException
	 */
	private void waitForStateChange(int maxTTW) throws MqttException {
		synchronized (waiter) {
			if (!donext) {
				try {
					waiter.wait(maxTTW);
				} catch (InterruptedException e) {
					log("timed out");
					e.printStackTrace();
				}

				if (ex != null) {
					throw (MqttException) ex;
				}
			}
			donext = false;
		}
	}

	/**
	 * Subscribe to a topic on an MQTT server Once subscribed this method waits for
	 * the messages to arrive from the server that match the subscription. It
	 * continues listening for messages until the enter key is pressed.
	 * 
	 * @param topicName to subscribe to (can be wild carded)
	 * @param qos       the maximum quality of service to receive messages at for
	 *                  this subscription
	 * @throws MqttException
	 */
	public void subscribe(List<String> topicName, List<Integer> qos) throws Throwable {
		// Use a state machine to decide which step to do next. State change occurs
		// when a notification is received that an MQTT action has completed
		while (state != FINISH) {
			switch (state) {
			case BEGIN:
				// Connect using a non-blocking connect
				MqttConnector con = new MqttConnector();
				con.doConnect();
				break;
			case CONNECTED:
				// Subscribe using a non-blocking subscribe
				Subscriber sub = new Subscriber();
				sub.doSubscribe(topicName, qos);
				break;
			case SUBSCRIBED:
				// Block until Enter is pressed allowing messages to arrive
				log("Waiting for messages...");
				// log("Press <Enter> to exit");
				// try {
				// System.in.read();
				// } catch (IOException e) {
				// // If we can't read we'll just exit
				// }
				// state = DISCONNECT;
				// donext = true;
				break;
			case DISCONNECT:
				Disconnector disc = new Disconnector();
				disc.doDisconnect();
				break;
			case ERROR:
				log("ERROR!");
				throw ex;
			case DISCONNECTED:
				state = FINISH;
				donext = true;
				break;
			}

			// if (state != FINISH && state != DISCONNECT) {
			waitForStateChange(10000);
			// }
		}
	}

	/**
	 * Utility method to handle logging. If 'quietMode' is set, this method does
	 * nothing
	 * 
	 * @param message the message to log
	 */
	void log(String message) {
		if (verbose) {
			// System.out.println(message);
			logger.info(message);
		}
	}

	/****************************************************************/
	/* Methods to implement the MqttCallback interface */
	/****************************************************************/

	/**
	 * @see MqttCallback#connectionLost(Throwable)
	 */
	@Override
	public void connectionLost(Throwable cause) {
		// Called when the connection to the server has been lost.
		// An application may choose to implement reconnection
		// logic at this point. This sample simply exits.
		log("Connection to " + brokerUrl + " lost!" + cause);
		System.exit(1);
	}

	/**
	 * @see MqttCallback#deliveryComplete(IMqttDeliveryToken)
	 */
	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// Called when a message has been delivered to the
		// server. The token passed in here is the same one
		// that was returned from the original call to publish.
		// This allows applications to perform asynchronous
		// delivery without blocking until delivery completes.
		//
		// This sample demonstrates asynchronous deliver, registering
		// a callback to be notified on each call to publish.
		//
		// The deliveryComplete method will also be called if
		// the callback is set on the client
		//
		// note that token.getTopics() returns an array so we convert to a string
		// before printing it on the console
		log("Delivery complete callback: Publish Completed " + Arrays.toString(token.getTopics()));
	}

	/**
	 * @throws JsonProcessingException
	 * @see MqttCallback#messageArrived(String, MqttMessage)
	 */
	@Override
	public void messageArrived(String topic, MqttMessage message) {
		// Called when a message arrives from the server that matches any
		// subscription made by the client
		String time = new Timestamp(System.currentTimeMillis()).toString();
		log("Time: " + time + "  Topic: " + topic + "  Message: " + new String(message.getPayload()) + "  QoS: "
				+ message.getQos());

		switch (topic) {
		case "trial":
			MsgTrial msgTrial;
			try {
				msgTrial = objectMapper.readValue(new String(message.getPayload()), MsgTrial.class);
				
				String sub_type = msgTrial.getMsg().getSubType();
				switch (sub_type) {
				case "start":
				case "create":
					// Just need to pass in the id. This came from the control so id is expected to be correct.
					// No need to query to make sure id exists.
					Experiment tempExperiment = new Experiment(-1l, msgTrial.getMsg().getExperimentId(), "", "", "", "");
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
					try {
						URL url = new URL(metadataApiUrl);
						URI uri = URI.create("/trials");
						log("POST - " + url.toString() + uri.toString());
						RxHttpClient httpClient = RxHttpClient.create(url);
						Flowable<HttpResponse<Trial>> call = httpClient.exchange(
								HttpRequest.POST(uri.toString(), objectMapper.writeValueAsString(trial)), Trial.class);
						HttpResponse<Trial> response = call.blockingFirst();
						log(response.getStatus().getCode() + " : " + response.getStatus().getReason());
						httpClient.close();
					} catch (MalformedURLException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (HttpClientResponseException e2) {
						e2.printStackTrace();
					}	
					break;
				}
			} catch (JsonMappingException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			} catch (JsonProcessingException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			}
			break;
		case "experiment":
			MsgExperiment msgExperiment;
			try {
				msgExperiment = objectMapper.readValue(new String(message.getPayload()), MsgExperiment.class);

				String sub_type = msgExperiment.getMsg().getSubType();
				switch (sub_type) {
				case "create":
					// Create the experiment_id (UUID) here.
					// UUID experiment_id = UUID.randomUUID();
					Experiment experiment = new Experiment(
							-1,
							msgExperiment.getMsg().getExperimentId(),
							msgExperiment.getData().getName(),
							msgExperiment.getData().getDate(),
							msgExperiment.getData().getAuthor(),
							msgExperiment.getData().getMission()
							);
					try {
						URL url = new URL(metadataApiUrl);
						URI uri = URI.create("/experiments");
						log("POST - " + url.toString() + uri.toString());
						RxHttpClient httpClient = RxHttpClient.create(url);
						Flowable<HttpResponse<Experiment>> call = httpClient.exchange(
								HttpRequest.POST(uri.toString(), objectMapper.writeValueAsString(experiment)),
								Experiment.class);
						HttpResponse<Experiment> response = call.blockingFirst();
						log(response.getStatus().getCode() + " : " + response.getStatus().getReason());
						httpClient.close();
					} catch (MalformedURLException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (HttpClientResponseException e2) {
						e2.printStackTrace();
					}	
					break;
				}
			} catch (JsonMappingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (JsonProcessingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		default:
			log("Unrecognized topic: " + topic);
			break;
		}
	}

	/****************************************************************/
	/* End of MqttCallback methods */
	/****************************************************************/
	static void printHelp() {
		System.out.println(
				"Syntax:\n\n" + "    SampleAsyncCallBack [-h] [-a publish|subscribe] [-t <topic>] [-m <message text>]\n"
						+ "            [-s 0|1|2] -b <hostname|IP address>] [-p <brokerport>] [-i <clientID>]\n\n"
						+ "    -h  Print this help text and quit\n" + "    -q  Quiet mode (default is false)\n"
						+ "    -a  Perform the relevant action (default is publish)\n"
						+ "    -t  Publish/subscribe to <topic> instead of the default\n"
						+ "            (publish: \"Sample/Java/v3\", subscribe: \"Sample/#\")\n"
						+ "    -m  Use <message text> instead of the default\n"
						+ "            (\"Message from MQTTv3 Java client\")\n"
						+ "    -s  Use this QoS instead of the default (2)\n"
						+ "    -b  Use this name/IP address instead of the default (m2m.eclipse.org)\n"
						+ "    -p  Use this port instead of the default (1883)\n\n"
						+ "    -i  Use this client ID instead of SampleJavaV3_<action>\n"
						+ "    -c  Connect to the server with a clean session (default is false)\n"
						+ "     \n\n Security Options \n" + "     -u Username \n" + "     -z Password \n"
						+ "     \n\n SSL Options \n" + "    -v  SSL enabled; true - (default is false) "
						+ "    -k  Use this JKS format key store to verify the client\n"
						+ "    -w  Passpharse to verify certificates in the keys store\n"
						+ "    -r  Use this JKS format keystore to verify the server\n"
						+ " If javax.net.ssl properties have been set only the -v flag needs to be set\n"
						+ "Delimit strings containing spaces with \"\"\n\n"
						+ "Publishers transmit a single message then disconnect from the server.\n"
						+ "Subscribers remain connected to the server and receive appropriate\n"
						+ "messages until <enter> is pressed.\n\n");
	}

	/**
	 * Connect in a non-blocking way and then sit back and wait to be notified that
	 * the action has completed.
	 */
	public class MqttConnector {

		public MqttConnector() {
		}

		public void doConnect() {
			// Connect to the server
			// Get a token and setup an asynchronous listener on the token which
			// will be notified once the connect completes
			log("Connecting to " + brokerUrl + " with client ID " + client.getClientId());

			IMqttActionListener conListener = new IMqttActionListener() {
				public void onSuccess(IMqttToken asyncActionToken) {
					log("Connected");
					state = CONNECTED;
					carryOn();
				}

				public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
					ex = null; // Prevent the throw in the waitForStateChange method
					state = BEGIN; // Changed from ERROR to BEGIN to attempt a reconnect.
					log("connect failed: " + exception);
					log("Reconnecting...");
					try {
						waiter.wait(5000);
					} catch (InterruptedException e) {
						log("Reconnect timed out!");
						ex = e;
					}
					carryOn();
				}

				public void carryOn() {
					synchronized (waiter) {
						donext = true;
						waiter.notifyAll();
					}
				}
			};

			try {
				// Connect using a non-blocking connect
				client.connect(options, "Connect Asist Context", conListener);
			} catch (MqttException e) {
				// If though it is a non-blocking connect an exception can be
				// thrown if validation of parms fails or other checks such
				// as already connected fail.
				log("MqttException: " + e);
				state = ERROR;
				donext = true;
				ex = e;
			}
		}
	}

	/**
	 * Publish in a non-blocking way and then sit back and wait to be notified that
	 * the action has completed.
	 */
	public class Publisher {
		public void doPublish(String topicName, int qos, byte[] payload) {
			// Send / publish a message to the server
			// Get a token and setup an asynchronous listener on the token which
			// will be notified once the message has been delivered
			MqttMessage message = new MqttMessage(payload);
			message.setQos(qos);

			String time = new Timestamp(System.currentTimeMillis()).toString();
			log("Publishing at: " + time + " to topic \"" + topicName + "\" qos " + qos);

			// Setup a listener object to be notified when the publish completes.
			//
			IMqttActionListener pubListener = new IMqttActionListener() {
				public void onSuccess(IMqttToken asyncActionToken) {
					log("Publish Completed");
					state = PUBLISHED;
					carryOn();
				}

				public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
					ex = exception;
					state = ERROR;
					log("Publish failed" + exception);
					carryOn();
				}

				public void carryOn() {
					synchronized (waiter) {
						donext = true;
						waiter.notifyAll();
					}
				}
			};

			try {
				// Publish the message
				client.publish(topicName, message, "Pub sample context", pubListener);
			} catch (MqttException e) {
				state = ERROR;
				donext = true;
				ex = e;
			}
		}
	}

	/**
	 * Subscribe in a non-blocking way and then sit back and wait to be notified
	 * that the action has completed.
	 */
	public class Subscriber {
		public void doSubscribe(List<String> topicName, List<Integer> qos) {
			// Make a subscription
			// Get a token and setup an asynchronous listener on the token which
			// will be notified once the subscription is in place.
			log("Subscribing to topic \"" + topicName + "\" qos " + qos);

			IMqttActionListener subListener = new IMqttActionListener() {
				public void onSuccess(IMqttToken asyncActionToken) {
					log("Subscribe Completed");
					state = SUBSCRIBED;
					carryOn();
				}

				public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
					ex = exception;
					state = ERROR;
					log("Subscribe failed" + exception);
					carryOn();
				}

				public void carryOn() {
					synchronized (waiter) {
						donext = true;
						waiter.notifyAll();
					}
				}
			};

			try {
				client.subscribe(topicName.toArray(new String[topicName.size()]),
						qos.stream().mapToInt(i -> i).toArray(), "Subscribe sample context", subListener);
			} catch (MqttException e) {
				state = ERROR;
				donext = true;
				ex = e;
			}
		}
	}

	/**
	 * Disconnect in a non-blocking way and then sit back and wait to be notified
	 * that the action has completed.
	 */
	public class Disconnector {
		public void doDisconnect() {
			// Disconnect the client
			log("Disconnecting");

			IMqttActionListener discListener = new IMqttActionListener() {
				public void onSuccess(IMqttToken asyncActionToken) {
					log("Disconnect Completed");
					state = DISCONNECTED;
					carryOn();
				}

				public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
					ex = exception;
					state = ERROR;
					log("Disconnect failed: " + exception);
					carryOn();
				}

				public void carryOn() {
					synchronized (waiter) {
						donext = true;
						waiter.notifyAll();
					}
				}
			};

			try {
				client.disconnect("Disconnect Asist Context", discListener);
			} catch (MqttException e) {
				state = ERROR;
				donext = true;
				ex = e;
			}
		}
	}
}