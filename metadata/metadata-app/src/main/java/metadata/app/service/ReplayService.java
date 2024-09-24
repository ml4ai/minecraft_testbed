package metadata.app.service;

import java.util.List;

import metadata.app.model.MessageReplay;
import metadata.app.model.Replay;
import metadata.app.model.Trial;

public interface ReplayService {	
	Replay createReplay(Replay replay);
	List<Replay> readReplays();
	Replay readReplay(long id);
	Replay readReplayUUID(String replayId);
	Replay updateReplay(Replay replay);
    boolean deleteReplay(long id);
    String findReplayRootId(String replayId);
	Trial findReplayRootTrial(String replayId);
	List<Object> findReplayParents(String replayId);
	Replay runReplay(MessageReplay messageReplay, String index);
	boolean abortReplay();
}
