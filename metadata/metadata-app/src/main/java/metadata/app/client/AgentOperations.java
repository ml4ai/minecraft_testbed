package metadata.app.client;

import java.util.List;

public interface AgentOperations {
	
    List<String> agents();
    String agentsUp(String name);
    String agentsDown(String name);
    String agentsScriptUp();
    String agentsScriptDown();
}
