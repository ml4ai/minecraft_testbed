package metadata.app.controller;

import java.io.IOException;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.inject.Inject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.micronaut.core.annotation.Nullable;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.MediaType;
import io.micronaut.http.MutableHttpResponse;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Consumes;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Delete;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.Produces;
import io.micronaut.http.annotation.Put;
import io.micronaut.http.annotation.QueryValue;
import io.micronaut.http.multipart.CompletedFileUpload;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import metadata.app.model.BatchReplayBody;
import metadata.app.model.IgnoreMessageListItem;
import metadata.app.model.MessageReplay;
import metadata.app.model.MessageApiResult;
import metadata.app.model.Replay;
import metadata.app.model.ReplayBody;
import metadata.app.model.ReplayObject;
import metadata.app.model.Trial;
import metadata.app.service.DefaultReplayService;

@Controller("/replays")
public class ReplayController {
	private static final Logger logger = LoggerFactory.getLogger(ReplayController.class);
	private final DefaultReplayService crudService;

	@Inject
	public ReplayController(DefaultReplayService crudService) {
		this.crudService = crudService;
	}

	@Post("/")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<Replay> create(@Body Replay replay) {
		logger.info(MessageFormat.format("Creating replay {0}.", replay.getReplayId()));
		Replay createdReplay = crudService.createReplay(replay);
		if (createdReplay == null) {
			return HttpResponse.serverError(replay);
		} else if (createdReplay.getId() > 0) {
			return HttpResponse.ok(createdReplay);
		} else {
			return HttpResponse.badRequest(replay);
		}
	}

	@Get("/{id}")
	@Produces(MediaType.APPLICATION_JSON)
	public Replay read(long id) {
		return crudService.readReplay(id);
	}

	@Get("/uuid/{uuid}")
	@Produces(MediaType.APPLICATION_JSON)
	public Replay readUUID(String uuid) {
		return crudService.readReplayUUID(uuid);
	}

	@Get("/")
	@Produces(MediaType.APPLICATION_JSON)
	public List<Replay> reads() {
		return crudService.readReplays();
	}

	@Put("/{id}")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<Replay> update(@Body Replay replay, long id) {
		Replay updatedReplay = crudService.updateReplay(replay);
		if (updatedReplay == null) {
			return HttpResponse.serverError(replay);
		} else if (updatedReplay.getId() == replay.getId()) {
			return HttpResponse.ok(updatedReplay);
		} else {
			return HttpResponse.badRequest(replay);
		}
	}

	@Delete("/{id}")
	public HttpResponse<Boolean> delete(long id) {
		// return crudService.deleteReplay(id) ? HttpStatus.OK : HttpStatus.BAD_REQUEST;
		boolean deletedReplay = crudService.deleteReplay(id);
		if (deletedReplay == false) {
			return HttpResponse.serverError(false);
		} else {
			return HttpResponse.ok(true);
		}
	}

	@Get("/root-id/{uuid}")
	@Produces(MediaType.TEXT_PLAIN)
	public String rootId(String uuid) {
		return crudService.findReplayRootId(uuid);
	}

	@Get("/root-trial/{uuid}")
	@Produces(MediaType.APPLICATION_JSON)
	public Trial rootTrial(String uuid) {
		return crudService.findReplayRootTrial(uuid);
	}

	@Get("/parents/{uuid}")
	@Produces(MediaType.APPLICATION_JSON)
	public List<Object> parents(String uuid) {
		return crudService.findReplayParents(uuid);
	}

	@Post("/run/trial/{uuid}")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<?> apiRunTrial(String uuid, @Body ReplayBody replayBody,@QueryValue(value = "index") String index, @Nullable @QueryValue(value = "quick") Boolean quick) {
		if (!Boolean.TRUE.equals(quick)) {
			quick = false;
		}
		Replay createdReplay = null;
		if (quick) {
			createdReplay = crudService.apiRunTrialQuick(uuid, replayBody.getIgnoreMessageList(), replayBody.getIgnoreSourceList(), replayBody.getIgnoreTopicList(), index);
		} else {
			ReplayObject replayObject = new ReplayObject(uuid, "TRIAL");
			List<ReplayObject> replayObjects = new ArrayList<ReplayObject>();			
			replayObjects.add(replayObject);
			createdReplay = crudService.apiRunTrial(replayObjects, replayBody.getIgnoreMessageList(), replayBody.getIgnoreSourceList(), replayBody.getIgnoreTopicList(), false, index).get(0);
		}
		if (createdReplay == null) {
//    		return HttpResponse.serverError(messageReplay);
			return HttpResponse.ok(new MessageApiResult("failure",
					MessageFormat.format("Replay using trialId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		} else if (createdReplay.getId() > 0) {
			Map<String, String> data = new HashMap<String, String>();
			data.put("replay_id", createdReplay.getReplayId());
			return HttpResponse.ok(new MessageApiResult("success",
					MessageFormat.format("Replay using trialId: [{0}] has completed, new replayId created: [{1}].",
							uuid, createdReplay.getReplayId()),
					data));
		} else {
			return HttpResponse.badRequest(new MessageApiResult("failure",
					MessageFormat.format("Replay using trialId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		}
	}

	@Post("/run/trial/blocking/{uuid}")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<?> apiRunTrialBlocking(String uuid, @Body ReplayBody replayBody, @QueryValue(value = "index") String index) {
		Replay createdReplay = crudService.apiRunTrialBlocking(uuid, replayBody.getIgnoreMessageList(), replayBody.getIgnoreSourceList(), replayBody.getIgnoreTopicList(), index);

		if (createdReplay == null) {
//    		return HttpResponse.serverError(messageReplay);
			return HttpResponse.ok(new MessageApiResult("failure",
					MessageFormat.format("Replay using trialId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		} else if (createdReplay.getId() > 0) {
			Map<String, String> data = new HashMap<String, String>();
			data.put("replay_id", createdReplay.getReplayId());
			return HttpResponse.ok(new MessageApiResult("success",
					MessageFormat.format("Replay using trialId: [{0}] has completed, new replayId created: [{1}].",
							uuid, createdReplay.getReplayId()),
					data));
		} else {
			return HttpResponse.badRequest(new MessageApiResult("failure",
					MessageFormat.format("Replay using trialId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		}
	}
	
	@Post("/run/replay/blocking/{uuid}")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<?> apiRunReplayBlocking(String uuid, @Body ReplayBody replayBody, @QueryValue(value = "index") String index) {
		Replay createdReplay = crudService.apiRunReplayBlocking(uuid, replayBody.getIgnoreMessageList(), replayBody.getIgnoreSourceList(), replayBody.getIgnoreTopicList(), index);

		if (createdReplay == null) {
//    		return HttpResponse.serverError(messageReplay);
			return HttpResponse.ok(new MessageApiResult("failure",
					MessageFormat.format("Replay using replayId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		} else if (createdReplay.getId() > 0) {
			Map<String, String> data = new HashMap<String, String>();
			data.put("replay_id", createdReplay.getReplayId());
			return HttpResponse.ok(new MessageApiResult("success",
					MessageFormat.format("Replay using replayId: [{0}] has completed, new replayId created: [{1}].",
							uuid, createdReplay.getReplayId()),
					data));
		} else {
			return HttpResponse.badRequest(new MessageApiResult("failure",
					MessageFormat.format("Replay using replayId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		}
	}
	
	@Post("/run/replay/{uuid}")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<?> apiRunReplay(String uuid, @Body ReplayBody replayBody,
			@QueryValue(value = "index") String index, @Nullable @QueryValue(value = "quick") Boolean quick) {
		if (!Boolean.TRUE.equals(quick)) {
			quick = false;
		}
		Replay createdReplay = null;
		if (quick) {
			createdReplay = crudService.apiRunReplayQuick(uuid, replayBody.getIgnoreMessageList(), replayBody.getIgnoreSourceList(), replayBody.getIgnoreTopicList(), index);
		} else {
			ReplayObject replayObject = new ReplayObject(uuid, "REPLAY");
			List<ReplayObject> replayObjects = new ArrayList<ReplayObject>();			
			replayObjects.add(replayObject);
			createdReplay = crudService.apiRunReplay(replayObjects, replayBody.getIgnoreMessageList(), replayBody.getIgnoreSourceList(), replayBody.getIgnoreTopicList(), false, index).get(0);
		}
		if (createdReplay == null) {
//    		return HttpResponse.serverError(messageReplay);
			return HttpResponse.ok(new MessageApiResult("failure",
					MessageFormat.format("Replay using replayId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		} else if (createdReplay.getId() > 0) {
			Map<String, String> data = new HashMap<String, String>();
			data.put("replay_id", createdReplay.getReplayId());
			return HttpResponse.ok(new MessageApiResult("success",
					MessageFormat.format("Replay using replayId: [{0}] has completed, new replayId created: [{1}].",
							uuid, createdReplay.getReplayId()),
					data));
		} else {
			return HttpResponse.badRequest(new MessageApiResult("failure",
					MessageFormat.format("Replay using replayId: [{0}] could not be completed.", uuid),
					new HashMap<String, String>()));
		}
	}

	@Post("/run/batch/trial")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<?> apiRunBatchTrial(@Body BatchReplayBody batchReplayBody, @QueryValue(value = "index") String index) {
		// No quick for batch (if we need this we need to turn quick into a threaded
		// call.
		List<Replay> createdReplays = crudService.apiRunTrial(batchReplayBody.getReplayObjects(), batchReplayBody.getIgnoreMessageList(), batchReplayBody.getIgnoreSourceList(), batchReplayBody.getIgnoreTopicList(), batchReplayBody.getRestart(), index);
		if (createdReplays == null) {
			return HttpResponse.ok(new MessageApiResult("failure", "Batch replays could not be called.",
					new HashMap<String, String>()));
		}
		if (createdReplays.size() <= 0) {
//        		return HttpResponse.serverError(messageReplay);
			return HttpResponse.ok(new MessageApiResult("failure", "Batch replay for trials could not be called.",
					new HashMap<String, String>()));
		} else {
			Map<String, String> data = new HashMap<String, String>();
			createdReplays.forEach((createdReplay) -> {
				data.put("replay_id", createdReplay.getReplayId());
			});
			return HttpResponse.ok(new MessageApiResult("success", "Batch trial replays called.", data));
		}

	}

	@Post("/run/batch/replay")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<?> apiRunBatchReplay(@Body BatchReplayBody batchReplayBody, @QueryValue(value = "index") String index) {
		// No quick for batch (if we need this we need to turn quick into a threaded
		// call.
		List<Replay> createdReplays = crudService.apiRunReplay(batchReplayBody.getReplayObjects(), batchReplayBody.getIgnoreMessageList(), batchReplayBody.getIgnoreSourceList(), batchReplayBody.getIgnoreTopicList(), batchReplayBody.getRestart(), index);
		if (createdReplays == null) {
			return HttpResponse.ok(new MessageApiResult("failure", "Batch replays could not be called.",
					new HashMap<String, String>()));
		}
		if (createdReplays.size() <= 0) {
//    		return HttpResponse.serverError(messageReplay);
			return HttpResponse.ok(new MessageApiResult("failure", "Batch replay for replays could not be called.",
					new HashMap<String, String>()));
		} else {
			Map<String, String> data = new HashMap<String, String>();
			createdReplays.forEach((createdReplay) -> {
				data.put("replay_id", createdReplay.getReplayId());
			});
			return HttpResponse.ok(new MessageApiResult("success", "Batch replay replays called.", data));
		}
	}

	@Post("/run")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<?> run(@Body MessageReplay messageReplay, @QueryValue(value = "index") String index,
			@Nullable @QueryValue(value = "quick") Boolean quick) {
		if (!Boolean.TRUE.equals(quick)) {
			quick = false;
		}
		Replay createdReplay = crudService.runReplay(messageReplay, index);
		if (createdReplay == null) {
//    		return HttpResponse.serverError(messageReplay);
			return HttpResponse.ok(null);
		} else if (createdReplay.getId() > 0) {
			return HttpResponse.ok(createdReplay);
		} else {
			return HttpResponse.badRequest(messageReplay);
		}
	}

	@Get("/run/abort")
	public boolean abort() {
		return crudService.abortReplay();
	}

	@Get(value = "/export/{uuid}")
	@Consumes(MediaType.APPLICATION_JSON)
	public MutableHttpResponse<StreamedFile> exportStreamed(String uuid, @QueryValue(value = "index") String index)
			throws IOException {
		StreamedFile streamedFile = crudService.exportStreamed(uuid, index);
		if (streamedFile != null) {
			return HttpResponse.ok(streamedFile);
		} else {
			return HttpResponse.notFound();
		}
	}

	@Get(value = "/export/file/{uuid}")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_OCTET_STREAM)
	public MutableHttpResponse<SystemFile> exportFile(String uuid, @QueryValue(value = "index") String index)
			throws IOException {
		SystemFile systemFile = (crudService.exportFile(uuid, index));
		if (systemFile != null) {
			return HttpResponse.ok(systemFile);
		} else {
			return HttpResponse.notFound();
		}
	}

	@Post("/import")
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	@Produces(MediaType.APPLICATION_JSON)
	public HttpResponse<MessageApiResult> importFile(CompletedFileUpload file,
			@QueryValue(value = "index") String index, @QueryValue(value = "createIndex") boolean createIndex) {
		try {
			MessageApiResult messageTrialImportResult = crudService.importFile(file.getBytes(), file.getFilename(),
					index, createIndex);
			return HttpResponse.ok(messageTrialImportResult);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return HttpResponse
					.serverError(new MessageApiResult("failure", "Error reading file!", new HashMap<String, String>()));
		}
	}
	
	@Get("/{uuid}/exist")
	public Boolean rootId(String uuid, @QueryValue(value = "index") String index) {
		return crudService.existElasticsearch(uuid, index);
	}
}