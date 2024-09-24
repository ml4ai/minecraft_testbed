package metadata.app.model;

import java.util.List;

public class Mqtt {

	private String brokerUrl;
	private String clientId;
	private List<String> topic;
	private List<Integer> qos;
	private boolean verbose;
	private boolean cleanSession;
	
	public String getBrokerUrl() {
		return brokerUrl;
	}
	public void setBrokerUrl(String brokerUrl) {
		this.brokerUrl = brokerUrl;
	}
	public String getClientId() {
		return clientId;
	}
	public void setClientId(String clientId) {
		this.clientId = clientId;
	}
	public List<String> getTopic() {
		return topic;
	}
	public void setTopic(List<String> topic) {
		this.topic = topic;
	}
	public List<Integer> getQos() {
		return qos;
	}
	public void setQos(List<Integer> qos) {
		this.qos = qos;
	}
	public boolean getVerbose() {
		return verbose;
	}
	public void setVerbose(boolean verbose) {
		this.verbose = verbose;
	}
	public boolean getCleanSession() {
		return cleanSession;
	}
	public void setCleanSession(boolean cleanSession) {
		this.cleanSession = cleanSession;
	}
	
}