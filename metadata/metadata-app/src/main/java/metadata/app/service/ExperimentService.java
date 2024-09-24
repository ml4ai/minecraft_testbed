package metadata.app.service;

import java.util.List;

import metadata.app.model.Experiment;

public interface ExperimentService {	
	Experiment createExperiment(Experiment experiment);
	List<Experiment> readExperiments();
	Experiment readExperiment(long id);
	Experiment readExperimentUUID(String experimentId);
	Experiment updateExperiment(Experiment experiment);
    boolean deleteExperiment(long id);
}
