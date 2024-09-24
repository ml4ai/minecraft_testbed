package metadata.msg.config;

import java.util.List;

import io.micronaut.context.annotation.ConfigurationProperties;

@ConfigurationProperties("mqtt")
public class MqttConfigurationProperties {
	String brokerUrl;
	String clientId;
	List<String> topic;
	List<Integer> qos;
	boolean verbose;
	boolean cleanSession;
	String metadataApiUrl;
	
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
	public boolean isVerbose() {
		return verbose;
	}
	public void setVerbose(boolean verbose) {
		this.verbose = verbose;
	}
	public boolean isCleanSession() {
		return cleanSession;
	}
	public void setCleanSession(boolean cleanSession) {
		this.cleanSession = cleanSession;
	}
	public String getMetadataApiUrl() {
		return metadataApiUrl;
	}
	public void setMetadataApiUrl(String metadataApiUrl) {
		this.metadataApiUrl = metadataApiUrl;
	}

}
