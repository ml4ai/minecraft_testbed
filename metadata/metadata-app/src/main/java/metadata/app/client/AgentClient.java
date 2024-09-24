package metadata.app.client;

import java.util.List;

import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.client.annotation.Client;
import io.micronaut.retry.annotation.Recoverable;
import io.micronaut.scheduling.TaskExecutors;
import io.micronaut.scheduling.annotation.ExecuteOn;

@Client("${agents.clientUrl}") 
@Recoverable
public interface AgentClient extends AgentOperations {

    @Get("/agents") 
    @Override
    List<String> agents();
    
    @Post("/agents/{name}/up")
    @ExecuteOn(TaskExecutors.IO)
    @Override
    String agentsUp(String name);
    
    @Post("/agents/{name}/down")
    @Override
    String agentsDown(String name);
    
    @Post("/agents/script/up")
    @Override
    String agentsScriptUp();
    
    @Post("/agents/script/down")
    @Override
    String agentsScriptDown();
}
