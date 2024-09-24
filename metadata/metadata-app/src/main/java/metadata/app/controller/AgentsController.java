package metadata.app.controller;

import java.util.List;
import javax.inject.Inject;

import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Post;
import io.micronaut.scheduling.annotation.ExecuteOn;
import io.micronaut.scheduling.TaskExecutors;
import metadata.app.client.AgentClient;

@Controller("/agents")
public class AgentsController {
	
    private final AgentClient agentHttpClient;
    private ObjectMapper objectMapper = new ObjectMapper();
     
    @Inject
    public AgentsController(AgentClient agentHttpClient) {
        this.agentHttpClient = agentHttpClient;
    }
    
	
	@Get("/")
	public List<String> agents() {
		return agentHttpClient.agents();
	}
	
	@Post("/{name}/up")
	@ExecuteOn(TaskExecutors.IO)
	public String agentsUp(String name) {
		return agentHttpClient.agentsUp(name);
	}
	
	@Post("/{name}/down")
	@ExecuteOn(TaskExecutors.IO)
	public String agentsDown(String name) {
		return agentHttpClient.agentsDown(name);
	}
	
	@Post("/{name}/restart")
	@ExecuteOn(TaskExecutors.IO)
	public String agentsRestart(String name) {
		String down = agentHttpClient.agentsDown(name);
		String up = agentHttpClient.agentsUp(name);
		return down + System.lineSeparator() + System.lineSeparator() + up;
	}
	
	@Post("/script/restart")
	@ExecuteOn(TaskExecutors.IO)
	public String agentsScriptRestart(String name) {
		String down = agentHttpClient.agentsScriptDown();
		String up = agentHttpClient.agentsScriptUp();
		return down + System.lineSeparator() + System.lineSeparator() + up;
	}
}