package metadata.app.service;

import java.util.List;

import com.github.dockerjava.api.command.InspectContainerResponse;
import com.github.dockerjava.api.model.Container;
import com.github.dockerjava.api.model.Statistics;

import io.micronaut.core.annotation.NonNull;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import metadata.app.model.Experiment;

public interface DockerService {	
	Boolean ping();
	List<Container> containerList();
	List<String> containerLog(String containerId);
	Container containerStart(String containerId);
	Container containerStop(String containerId);
	SystemFile containerLogDownload(String containerId);
	List<Statistics> containerStats(String containerId);
//	List<Container> containerRestart(List<String> containerIds);
	StreamedFile containerLogsDownload();
}
