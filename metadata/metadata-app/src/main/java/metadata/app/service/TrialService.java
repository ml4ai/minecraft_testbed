package metadata.app.service;

import java.util.List;

import javax.validation.constraints.NotNull;

import io.micronaut.core.annotation.NonNull;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import metadata.app.model.MessageApiResult;
import metadata.app.model.Trial;

public interface TrialService {
	Trial createTrial(Trial metadata);
	List<Trial> readTrials();
	Trial readTrial(long id);
	Trial readTrialUUID(String trialId);
	Trial updateTrial(Trial metadata);
    boolean deleteTrial(long id);
    SystemFile exportFile(@NonNull @NotNull String trialId, @NonNull @NotNull String index);
    StreamedFile exportStreamed(@NonNull @NotNull String trialId, @NonNull @NotNull String index);
    MessageApiResult importFile(@NonNull @NotNull byte[] bytes, @NonNull @NotNull String filename, @NonNull @NotNull String index, @NonNull @NotNull boolean createIndex);
}
