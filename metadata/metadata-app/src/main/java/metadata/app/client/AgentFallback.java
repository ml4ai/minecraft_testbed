package metadata.app.client;

import java.util.ArrayList;
import java.util.List;

import io.micronaut.retry.annotation.Fallback;

@Fallback
public class AgentFallback implements AgentOperations {

	@Override
	public List<String> agents() {
		return new ArrayList<String>();
	}

	@Override
	public String agentsUp(String name) {
		return "";
	}

	@Override
	public String agentsDown(String name) {
		return "";
	}

	@Override
	public String agentsScriptUp() {
		return "";
	}

	@Override
	public String agentsScriptDown() {
		return "";
	}

}
