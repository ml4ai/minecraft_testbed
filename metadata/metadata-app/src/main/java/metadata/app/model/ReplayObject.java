package metadata.app.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ReplayObject {
	
	@JsonProperty("id")
	private String id;
	@JsonProperty("type")
	private String type;
	
	public ReplayObject() {
		// TODO Auto-generated constructor stub
	}
	
	@JsonIgnore()
	public ReplayObject(String id, String type) {
		this.id = id;
		this.type = type;
	}
	
	@JsonProperty("id")
	public String getId() {
		return id;
	}
	@JsonProperty("id")
	public void setId(String id) {
		this.id = id;
	}
	
	@JsonProperty("type")
	public String getType() {
		return type;
	}
	@JsonProperty("type")
	public void setType(String type) {
		this.type = type;
	}
	
	@JsonIgnore()
	public static void main(String[] args) {
		try {
			ReplayObject replayObject1 = new ReplayObject("hello_world", "ASI");
			ObjectMapper objectMapper = new ObjectMapper();
			String json = "{\"id\": \"hello_world\",\"type\": \"ASI\"}";
			System.out.println(objectMapper.writeValueAsString(replayObject1));
			ReplayObject replayObject2 = objectMapper.readValue(json, ReplayObject.class);
			System.out.println(objectMapper.writeValueAsString(replayObject2));
		} catch (JsonProcessingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
