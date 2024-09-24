package metadata.app.service;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;
import java.io.PrintWriter;
import java.text.MessageFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.atomic.AtomicInteger;

import javax.inject.Inject;
import javax.inject.Named;
import javax.validation.constraints.NotNull;

import org.apache.lucene.search.TotalHits;
import org.elasticsearch.action.bulk.BulkItemResponse;
import org.elasticsearch.action.bulk.BulkRequest;
import org.elasticsearch.action.bulk.BulkResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.search.ClearScrollRequest;
import org.elasticsearch.action.search.ClearScrollResponse;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchScrollRequest;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.client.indices.CreateIndexRequest;
import org.elasticsearch.client.indices.CreateIndexResponse;
import org.elasticsearch.client.indices.GetIndexRequest;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.index.query.BoolQueryBuilder;
import org.elasticsearch.index.query.MatchQueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.Scroll;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.sort.SortOrder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.context.annotation.Context;
import io.micronaut.context.annotation.Property;
import io.micronaut.core.annotation.NonNull;
import io.micronaut.core.annotation.Nullable;
import io.micronaut.http.HttpStatus;
import io.micronaut.http.MediaType;
import io.micronaut.http.exceptions.HttpStatusException;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import io.reactivex.Observable;
import io.reactivex.Single;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import io.reactivex.subjects.PublishSubject;
import io.vertx.core.json.JsonArray;
import io.vertx.reactivex.pgclient.PgPool;
import io.vertx.reactivex.sqlclient.Row;
import io.vertx.reactivex.sqlclient.RowIterator;
import io.vertx.reactivex.sqlclient.RowSet;
import io.vertx.reactivex.sqlclient.Tuple;
import metadata.app.model.MessageReplay;
import metadata.app.model.MessageReplayExport;
import metadata.app.model.MessageTrialExport;
import metadata.app.model.MessageApiResult;
import metadata.app.model.Msg;
import metadata.app.model.Replay;
import metadata.app.model.ReplayCompletedMessage;
import metadata.app.model.ReplayCompletedReasonType;
import metadata.app.model.ReplayMessageCountMessage;
import metadata.app.model.ReplayObject;
import metadata.app.model.Trial;
import metadata.app.client.AgentClient;
import metadata.app.model.Experiment;
import metadata.app.model.Header;
import metadata.app.model.IgnoreMessageListItem;
import metadata.app.publisher.ReplayCompletedPublisher;
import metadata.app.publisher.ReplayCreatedPublisher;
import metadata.app.publisher.ReplayMessageCountPublisher;
import metadata.app.publisher.ReplayMessagePublisher;
import metadata.app.publisher.TrialCreatedPublisher;

@Context
public class DefaultReplayService implements ReplayService {
	private static final Logger logger = LoggerFactory.getLogger(DefaultReplayService.class);
	private ObjectMapper objectMapper = new ObjectMapper();
//	final BeanContext context = BeanContext.run();
	@Inject
	private PgPool postgresClient;
	@Inject
	private RestHighLevelClient elasticsearchClient;
	@Named("io")
	@Inject
	ExecutorService executorService;
	@Inject
	AgentClient agentClient;

	private final DefaultTrialService defaultTrialService;
	private final DefaultExperimentService defaultExperimentService;
	private final ReplayCreatedPublisher replayCreatedClient;
	private final ReplayMessagePublisher replayMessagePublisher;
	private final ReplayMessageCountPublisher replayMessageCountPublisher;
	private final ReplayCompletedPublisher replayCompletedPublisher;

	private PublishSubject<Boolean> interrupter;
	private Thread currentReplayThread;
	private boolean replayRunning = false;
	private long currentMessageCount = 0;
	private long totalMessageCount = 0;
	private String runningReplayId = "";
	private ReplayCompletedReasonType reason = ReplayCompletedReasonType.UNKNOWN;

	private final String HEADER_METADATA_FILE_SUFIX = ".metadata";

	@Property(name = "asist.testbedVersion")
	private String TESTBED_VERSION;

	@Inject
	public DefaultReplayService(DefaultTrialService defaultTrialService, DefaultExperimentService defaultExperimentService, ReplayCreatedPublisher replayCreatedClient,
			ReplayMessagePublisher replayMessagePublisher, ReplayMessageCountPublisher replayMessageCountPublisher,
			ReplayCompletedPublisher replayCompletedPublisher) {
		this.defaultTrialService = defaultTrialService;
		this.defaultExperimentService = defaultExperimentService;
		this.replayCreatedClient = replayCreatedClient;
		this.replayMessagePublisher = replayMessagePublisher;
		this.replayMessageCountPublisher = replayMessageCountPublisher;
		this.replayCompletedPublisher = replayCompletedPublisher;
//		client = context.getBean(PgPool.class);
//		PgPoolOptions options = new PgPoolOptions().setPort(5432).setHost("localhost").setDatabase("postgres").setUser("postgres").setPassword("example").setMaxSize(5);
//		client = PgClient.pool(options);
	}

	@Override
	public Replay createReplay(Replay replay) {
		String sqlQuery = "INSERT INTO replays (replay_id, replay_parent_id, replay_parent_type, date, ignore_message_list, ignore_source_list, ignore_topic_list) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING (id)";
		Tuple elements = Tuple.tuple();
		elements.addUUID(UUID.fromString(replay.getReplayId()));
		elements.addUUID(UUID.fromString(replay.getReplayParentId()));
		elements.addString(replay.getReplayParentType());
		elements.addLocalDateTime(LocalDateTime.ofInstant(Instant.parse(replay.getDate()), ZoneOffset.UTC));
		String ignoreMessageList = "[]";
		String ignoreSourceList = "[]";
		String ignoreTopicList = "[]";
		try {
			ignoreMessageList = objectMapper.writeValueAsString(replay.getIgnoreMessageList() != null ? replay.getIgnoreMessageList() : new ArrayList<IgnoreMessageListItem>());
			ignoreSourceList = objectMapper.writeValueAsString(replay.getIgnoreSourceList() != null ? replay.getIgnoreSourceList() : new ArrayList<String>());
			ignoreTopicList = objectMapper.writeValueAsString(replay.getIgnoreTopicList() != null ? replay.getIgnoreTopicList() : new ArrayList<String>());
		} catch (JsonProcessingException e) {
			logger.error(e.getMessage());
			return null;
		}
		elements.addValue(io.vertx.core.json.Json.decodeValue(ignoreMessageList));
		elements.addValue(io.vertx.core.json.Json.decodeValue(ignoreSourceList));
		elements.addValue(io.vertx.core.json.Json.decodeValue(ignoreTopicList));

		try {
			RowSet<Row> rowSet = postgresClient.preparedQuery(sqlQuery).rxExecute(elements).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			if (rowIterator.hasNext()) {
				logger.info("1 row(s) affected.");
				Row row = rowIterator.next();
				Long _id = row.getLong("id");
				logger.info(MessageFormat.format("id returned: {0}.", _id));
				replay.setId(_id);
			}
			if (replay.getId() > 0) {
				replayCreatedClient.send(objectMapper.writeValueAsBytes(replay)).subscribe(() -> {
					// handle completion
				}, throwable -> {
					// handle error
				});
				;
				return replay;
			} else {
				logger.error(MessageFormat.format("Replay id: {0} from database was invalid!", replay.getId()));
				return null;
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		} catch (JsonProcessingException e) {
			// TODO Auto-generated catch block
			logger.error(e.getMessage());
			return null;
		}
	}

	@Override
	public List<Replay> readReplays() {
		List<Replay> replays = new LinkedList<>();
		try {
			RowSet<Row> rowSet = postgresClient.preparedQuery("SELECT * from replays ORDER BY id ASC").rxExecute()
					.blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				JsonArray jsonMessageArray = (JsonArray) row.getValue("ignore_message_list");
				JsonArray jsonSourceArray = (JsonArray) row.getValue("ignore_source_list");
				JsonArray jsonTopicArray = (JsonArray) row.getValue("ignore_topic_list");
				replays.add(new Replay(row.getLong("id"), row.getUUID("replay_id").toString(),
						row.getUUID("replay_parent_id").toString(), row.getString("replay_parent_type"),
						row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						objectMapper.readValue(jsonMessageArray.encode(), new TypeReference<List<IgnoreMessageListItem>>() {}),
						objectMapper.readValue(jsonSourceArray.encode(), new TypeReference<List<String>>() {}),
						objectMapper.readValue(jsonTopicArray.encode(), new TypeReference<List<String>>() {})
						)
					);
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		} catch (JsonMappingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (JsonProcessingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return replays;
	}

	@Override
	public Replay readReplay(long id) {
		List<Replay> replays = new LinkedList<>();
		try {
			RowSet<Row> rowSet = postgresClient.preparedQuery("SELECT * FROM replays WHERE id = $1")
					.rxExecute(Tuple.of((int) id)).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				JsonArray jsonMessageArray = (JsonArray) row.getValue("ignore_message_list");
				JsonArray jsonSourceArray = (JsonArray) row.getValue("ignore_source_list");
				JsonArray jsonTopicArray = (JsonArray) row.getValue("ignore_topic_list");
				replays.add(new Replay(row.getLong("id"), row.getUUID("replay_id").toString(),
						row.getUUID("replay_parent_id").toString(), row.getString("replay_parent_type"),
						row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						objectMapper.readValue(jsonMessageArray.encode(), new TypeReference<List<IgnoreMessageListItem>>() {}),
						objectMapper.readValue(jsonSourceArray.encode(), new TypeReference<List<String>>() {}),
						objectMapper.readValue(jsonTopicArray.encode(), new TypeReference<List<String>>() {})
						)
					);
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		} catch (JsonMappingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (JsonProcessingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		if (replays.isEmpty()) {
			logger.info(MessageFormat.format("No replay id: {0} found!", id));
			return null;
		}
		return replays.iterator().next();
	}

	@Override
	public Replay readReplayUUID(String replayId) {
		List<Replay> replays = new LinkedList<>();
		try {
			RowSet<Row> rowSet = postgresClient.preparedQuery("SELECT * FROM replays WHERE replay_id = $1")
					.rxExecute(Tuple.of(UUID.fromString(replayId))).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				JsonArray jsonMessageArray = (JsonArray) row.getValue("ignore_message_list");
				JsonArray jsonSourceArray = (JsonArray) row.getValue("ignore_source_list");
				JsonArray jsonTopicArray = (JsonArray) row.getValue("ignore_topic_list");
				replays.add(new Replay(row.getLong("id"), row.getUUID("replay_id").toString(),
						row.getUUID("replay_parent_id").toString(), row.getString("replay_parent_type"),
						row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						objectMapper.readValue(jsonMessageArray.encode(), new TypeReference<List<IgnoreMessageListItem>>() {}),
						objectMapper.readValue(jsonSourceArray.encode(), new TypeReference<List<String>>() {}),
						objectMapper.readValue(jsonTopicArray.encode(), new TypeReference<List<String>>() {})
						)
					);
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		} catch (JsonMappingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (JsonProcessingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		if (replays.isEmpty()) {
			logger.info(MessageFormat.format("No replay uuid: {0} found!", replayId));
			return null;
		}
		return replays.iterator().next();
	}

	@Override
	public Replay updateReplay(Replay replay) {
		String sqlQuery = "UPDATE replays SET replay_id = $1, replay_parent_id = $2, replay_parent_type = $3, date = $4, ignore_message_list = $5, ignore_source_list = $6, ignore_topic_list = $7 WHERE id = $8 RETURNING (id)";
		Tuple elements = Tuple.tuple();
		elements.addUUID(UUID.fromString(replay.getReplayId()));
		elements.addUUID(UUID.fromString(replay.getReplayParentId()));
		elements.addString(replay.getReplayParentType());
		elements.addLocalDateTime(LocalDateTime.ofInstant(Instant.parse(replay.getDate()), ZoneOffset.UTC));
		String ignoreMessageList = "[]";
		String ignoreSourceList = "[]";
		String ignoreTopicList = "[]";
		try {
			ignoreMessageList = objectMapper.writeValueAsString(replay.getIgnoreMessageList() != null ? replay.getIgnoreMessageList() : new ArrayList<IgnoreMessageListItem>());
			ignoreSourceList = objectMapper.writeValueAsString(replay.getIgnoreSourceList() != null ? replay.getIgnoreSourceList() : new ArrayList<String>());
			ignoreTopicList = objectMapper.writeValueAsString(replay.getIgnoreTopicList() != null ? replay.getIgnoreTopicList() : new ArrayList<String>());
		} catch (JsonProcessingException e) {
			logger.error(e.getMessage());
			return null;
		}
		elements.addValue(io.vertx.core.json.Json.decodeValue(ignoreMessageList));
		elements.addValue(io.vertx.core.json.Json.decodeValue(ignoreSourceList));
		elements.addValue(io.vertx.core.json.Json.decodeValue(ignoreTopicList));
		elements.addLong(replay.getId());
		try {
			RowSet<Row> rowSet = postgresClient.preparedQuery(sqlQuery).rxExecute(elements).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			if (rowIterator.hasNext()) {
				logger.info("1 row(s) affected.");
				Row row = rowIterator.next();
				Long _id = row.getLong("id");
				logger.info(MessageFormat.format("id returned: {0}.", _id));
				if (replay.getId() == _id) {
					return replay;
				} else {
					logger.error(MessageFormat.format("id returned: {0} does not match replay id.", replay.getId()));
					return null;
				}
			} else {
				logger.info("No replays found!");
				return null;
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
	}

	@Override
	public boolean deleteReplay(long id) {
		try {
			RowSet<Row> rowSet = postgresClient.preparedQuery("DELETE FROM replays WHERE id = $1")
					.rxExecute(Tuple.of((int) id)).blockingGet();
			if (rowSet.rowCount() > 0) {
				logger.info(MessageFormat.format("{0} row(s) affected.", rowSet.rowCount()));
				return true;
			} else {
				logger.error(MessageFormat.format("Replay with id: {0} was not deleted!", id));
				return false;
			}

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return false;
		}
//		client.preparedQuery("DELETE FROM replays WHERE id = $1").execute(Tuple.of((int) id), ar -> {
//			if (ar.succeeded()) {
//				RowSet<Row> rows = ar.result();
//				logger.info(rows.rowCount() + " row(s) affected.");
//			} else {
//				logger.error(ar.cause().getMessage());
//			}
//		});
//		return true;
	}
	
	public Replay apiRunTrialBlocking(@NonNull @NotNull String trialId, @NonNull @NotNull List<IgnoreMessageListItem> ignoreMessageList, @NonNull @NotNull List<String> ignoreSourceList, @NonNull @NotNull List<String> ignoreTopicList, @NonNull @NotNull String index) {
		if (replayRunning) {
			logger.error("There is a reaply already running!");
			return null;
		}
		replayRunning = true;
		try {
			Replay replay = new Replay(-1, UUID.randomUUID().toString(),
					trialId, "TRIAL",
					Instant.now().toString(), ignoreMessageList, ignoreSourceList, ignoreTopicList);
			Replay newReplay = createReplay(replay);
			if (newReplay != null) {
				runningReplayId = newReplay.getReplayId();
				logger.info(MessageFormat.format("Run replay {0} created.", newReplay.getReplayId()));

				// Start replay here!
				performBlockingReplay(replay, index);
				
				// End replay
				logger.info("Run replay finished.");
				if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
					reason = ReplayCompletedReasonType.FINISHED;
				}
				reset();
			} else {
				logger.info(MessageFormat.format("Run replay {0} could not be created.", replay.getReplayId()));
				replayRunning = false;
				runningReplayId = "";
				return null;
			}
			return newReplay;
		} catch (Exception e) {
			logger.error(e.getMessage());
			reset();
			return null;
		}
	}
	
	public Replay apiRunReplayBlocking(@NonNull @NotNull String replayId, @NonNull @NotNull List<IgnoreMessageListItem> ignoreMessageList, @NonNull @NotNull List<String> ignoreSourceList, @NonNull @NotNull List<String> ignoreTopicList, @NonNull @NotNull String index) {
		if (replayRunning) {
			logger.error("There is a reaply already running!");
			return null;
		}
		replayRunning = true;
		try {
			Replay replay = new Replay(-1, UUID.randomUUID().toString(),
					replayId, "REPLAY",
					Instant.now().toString(), ignoreMessageList, ignoreSourceList, ignoreTopicList);
			Replay newReplay = createReplay(replay);
			if (newReplay != null) {
				runningReplayId = newReplay.getReplayId();
				logger.info(MessageFormat.format("Run replay {0} created.", newReplay.getReplayId()));

				// Start replay here!
				performBlockingReplay(replay, index);
				
				// End replay
				logger.info("Run replay finished.");
				if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
					reason = ReplayCompletedReasonType.FINISHED;
				}
				reset();
			} else {
				logger.info(MessageFormat.format("Run replay {0} could not be created.", replay.getReplayId()));
				replayRunning = false;
				runningReplayId = "";
				return null;
			}
			return newReplay;
		} catch (Exception e) {
			logger.error(e.getMessage());
			reset();
			return null;
		}
	}
	
	public Replay apiRunTrialQuick(@NonNull @NotNull String trialId, @NonNull @NotNull List<IgnoreMessageListItem> ignoreMessageList, @NonNull @NotNull List<String> ignoreSourceList, @NonNull @NotNull List<String> ignoreTopicList, @NonNull @NotNull String index) {
		if (replayRunning) {
			logger.error("There is a reaply already running!");
			return null;
		}
		replayRunning = true;
		try {
			Replay replay = new Replay(-1, UUID.randomUUID().toString(),
					trialId, "TRIAL",
					Instant.now().toString(), ignoreMessageList, ignoreSourceList, ignoreTopicList);
			Replay newReplay = createReplay(replay);
			if (newReplay != null) {
				runningReplayId = newReplay.getReplayId();
				logger.info(MessageFormat.format("Run replay {0} created.", newReplay.getReplayId()));

				// Start replay here!
				performReplay(replay, index);
				
				// End replay
				logger.info("Run replay finished.");
				if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
					reason = ReplayCompletedReasonType.FINISHED;
				}
				reset();
			} else {
				logger.info(MessageFormat.format("Run replay {0} could not be created.", replay.getReplayId()));
				replayRunning = false;
				runningReplayId = "";
				return null;
			}
			return newReplay;
		} catch (Exception e) {
			logger.error(e.getMessage());
			reset();
			return null;
		}
	}
	
	public Replay apiRunReplayQuick(@NonNull @NotNull String replayId, @NonNull @NotNull List<IgnoreMessageListItem> ignoreMessageList, @NonNull @NotNull List<String> ignoreSourceList, @NonNull @NotNull List<String> ignoreTopicList, @NonNull @NotNull String index) {
		if (replayRunning) {
			logger.error("There is a reaply already running!");
			return null;
		}
		replayRunning = true;
		try {
			Replay replay = new Replay(-1, UUID.randomUUID().toString(),
					replayId, "REPLAY",
					Instant.now().toString(), ignoreMessageList, ignoreSourceList, ignoreTopicList);
			Replay newReplay = createReplay(replay);
			if (newReplay != null) {
				runningReplayId = newReplay.getReplayId();
				logger.info(MessageFormat.format("Run replay {0} created.", newReplay.getReplayId()));

				// Start replay here!
				performReplay(replay, index);
				
				// End replay
				logger.info("Run replay finished.");
				if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
					reason = ReplayCompletedReasonType.FINISHED;
				}
				reset();
			} else {
				logger.info(MessageFormat.format("Run replay {0} could not be created.", replay.getReplayId()));
				replayRunning = false;
				runningReplayId = "";
				return null;
			}
			return newReplay;
		} catch (Exception e) {
			logger.error(e.getMessage());
			reset();
			return null;
		}
	}
	
	private void performReplay(Replay replay, String index) {
		try {
			final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(15L));
			SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

			BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
			if (replay.getReplayParentType().equals("TRIAL")) {
				boolQueryBuilder.must(QueryBuilders.matchQuery("msg.trial_id.keyword", replay.getReplayParentId()));
				boolQueryBuilder.mustNot(QueryBuilders.existsQuery("msg.replay_id"));
			} else {
				boolQueryBuilder.must(QueryBuilders.matchQuery("msg.replay_id.keyword", replay.getReplayParentId()));
			}

			List<String> ignoreMessageTypes = new ArrayList<String>();
			List<String> ignoreSubTypes = new ArrayList<String>();
			replay.getIgnoreMessageList().forEach(ingnoreListItem -> {
				ignoreMessageTypes.add(ingnoreListItem.getMessageType());
				ignoreSubTypes.add(ingnoreListItem.getSubType());
			});
			List<String> ignoreSources = new ArrayList<String>();
			replay.getIgnoreSourceList().forEach(source -> {
				ignoreSources.add(source);
			});
			List<String> ignoreTopics = new ArrayList<String>();
			replay.getIgnoreTopicList().forEach(topic -> {
				ignoreTopics.add(topic);
			});

			SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
			searchSourceBuilder.fetchSource(null, "message");
			searchSourceBuilder.sort("@timestamp", SortOrder.ASC);
			searchSourceBuilder.query(boolQueryBuilder);

			searchRequest.source(searchSourceBuilder);

			SearchResponse searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);

			String scrollId = searchResponse.getScrollId();

			TotalHits totalHits = searchResponse.getHits().getTotalHits();
			totalMessageCount = totalHits.value;
			SearchHit[] searchHits = searchResponse.getHits().getHits();
			currentMessageCount = 0;
			while (searchHits != null && searchHits.length > 0) {
				// messageSourceCount.set(0, messageSourceCount.get(0) + searchHits.length);
				// Arrays.stream(searchHits).forEach(searchHit -> {
				for (SearchHit searchHit : searchHits) {
					currentMessageCount = currentMessageCount + 1;
					Map<String, Object> sourceMap = searchHit.getSourceAsMap();
					String timestamp = sourceMap.get("@timestamp").toString();
					String topic = sourceMap.get("topic").toString();
					Map<String, Object> message = new HashMap<String, Object>();
					String strHeader = objectMapper.writeValueAsString(sourceMap.remove("header"));
					Header header = objectMapper.readValue(strHeader, Header.class);
					message.put("header", header);
					String strMsg = objectMapper.writeValueAsString(sourceMap.remove("msg"));
					Msg msg = objectMapper.readValue(strMsg, Msg.class);
					msg.setReplayId(replay.getReplayId());
					msg.setReplayParentId(replay.getReplayParentId());
					msg.setReplayParentType(replay.getReplayParentType());
					message.put("msg", msg);
					message.put("data", sourceMap.remove("data"));
					String message_type = header.getMessageType();
					String sub_type = msg.getSubType();
					String source = msg.getSource();
					try {
						boolean send = true;
						if (ignoreMessageTypes.contains(message_type)) {
							if (ignoreSubTypes.contains(sub_type)) {
								send = false;
							}
						}
						if (ignoreSources.contains(source)) {
							send = false;
						}
						if (ignoreTopics.contains(topic)) {
							send = false;
						}
						if (send) {
							replayMessagePublisher.send(objectMapper.writeValueAsBytes(message), topic, 0)
									.subscribe(() -> {
										// handle completion
										logger.trace(MessageFormat.format("{0} [{1}] : {2}", timestamp, topic, objectMapper.writeValueAsString(message)));
										// messageDestinationCount.set(0, messageDestinationCount.get(0) + 1);
									}, throwable -> {
										logger.error(throwable.getMessage());
									});
						} else {
							logger.trace("Skipping message.");
						}
					} catch (JsonProcessingException e) {
						logger.error(e.getMessage());
					}
				}

				SearchScrollRequest scrollRequest = new SearchScrollRequest(scrollId);
				scrollRequest.scroll(scroll);
				searchResponse = elasticsearchClient.scroll(scrollRequest, RequestOptions.DEFAULT);
				scrollId = searchResponse.getScrollId();
				searchHits = searchResponse.getHits().getHits();
			}

//        logger.info(MessageFormat.format("SOURCE: {0} DESTINATION: {1}", messageSourceCount.get(0), messageDestinationCount.get(0)));
			ClearScrollRequest clearScrollRequest = new ClearScrollRequest();
			clearScrollRequest.addScrollId(scrollId);
			ClearScrollResponse clearScrollResponse = elasticsearchClient.clearScroll(clearScrollRequest, RequestOptions.DEFAULT);

			boolean succeeded = clearScrollResponse.isSucceeded();
			return;

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
				reason = ReplayCompletedReasonType.ERROR;
			}
			reset();
			return;
		} catch (IOException e) {
			logger.error(e.getMessage());
			if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
				reason = ReplayCompletedReasonType.ERROR;
			}
			reset();
			return;
		}
	}
	
	private void performBlockingReplay(Replay replay, String index) {
		logger.info(MessageFormat.format("{0} [{1}] running blocking replay [{2}].", replay.getReplayParentType(), replay.getReplayParentId(), replay.getReplayId()));
		interrupter = PublishSubject.create();
		try {
			final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(15L));
			SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

			BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
			if (replay.getReplayParentType().equals("TRIAL")) {
				boolQueryBuilder.must(QueryBuilders.matchQuery("msg.trial_id.keyword", replay.getReplayParentId()));
				boolQueryBuilder.mustNot(QueryBuilders.existsQuery("msg.replay_id"));
			} else {
				boolQueryBuilder.must(QueryBuilders.matchQuery("msg.replay_id.keyword", replay.getReplayParentId()));
			}

			List<String> ignoreMessageTypes = new ArrayList<String>();
			List<String> ignoreSubTypes = new ArrayList<String>();
			replay.getIgnoreMessageList().forEach(ingnoreListItem -> {
				ignoreMessageTypes.add(ingnoreListItem.getMessageType());
				ignoreSubTypes.add(ingnoreListItem.getSubType());
			});
			List<String> ignoreSources = new ArrayList<String>();
			replay.getIgnoreSourceList().forEach(source -> {
				ignoreSources.add(source);
			});
			List<String> ignoreTopics = new ArrayList<String>();
			replay.getIgnoreTopicList().forEach(topic -> {
				ignoreTopics.add(topic);
			});

			SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
			searchSourceBuilder.fetchSource(null, "message");
			searchSourceBuilder.sort("@timestamp", SortOrder.ASC);
			searchSourceBuilder.query(boolQueryBuilder);

			searchRequest.source(searchSourceBuilder);

			SearchResponse searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);

			String scrollId = searchResponse.getScrollId();

			TotalHits totalHits = searchResponse.getHits().getTotalHits();
			totalMessageCount = totalHits.value;
			SearchHit[] searchHits = searchResponse.getHits().getHits();

			List<Instant> lastInstant = new ArrayList<Instant>();
			lastInstant.add(null);
			// List<Integer> messageSourceCount = new ArrayList<Integer>();
			// messageSourceCount.add(0);
			// List<Integer> messageDestinationCount = new ArrayList<Integer>();
			// messageDestinationCount.add(1);
			currentMessageCount = 0;
			while (searchHits != null && searchHits.length > 0) {
				// messageSourceCount.set(0, messageSourceCount.get(0) + searchHits.length);
				// Arrays.stream(searchHits).forEach(searchHit -> {
				for (SearchHit searchHit : searchHits) {
					currentMessageCount = currentMessageCount + 1;
					Map<String, Object> sourceMap = searchHit.getSourceAsMap();
					String timestamp = sourceMap.get("@timestamp").toString();
					String topic = sourceMap.get("topic").toString();
					Map<String, Object> message = new HashMap<String, Object>();
					String strHeader = objectMapper.writeValueAsString(sourceMap.remove("header"));
					Header header = objectMapper.readValue(strHeader, Header.class);
					message.put("header", header);
					String strMsg = objectMapper.writeValueAsString(sourceMap.remove("msg"));
					Msg msg = objectMapper.readValue(strMsg, Msg.class);
					msg.setReplayId(replay.getReplayId());
					msg.setReplayParentId(replay.getReplayParentId());
					msg.setReplayParentType(replay.getReplayParentType());
					message.put("msg", msg);
					message.put("data", sourceMap.remove("data"));
					String message_type = header.getMessageType();
					String sub_type = msg.getSubType();
					String source = msg.getSource();
					try {
						Instant instant = Instant.parse(timestamp);
						long delay = ChronoUnit.MILLIS.between(lastInstant.get(0) != null ? lastInstant.get(0) : instant, instant);
						if (delay > 15000)
							delay = 15000;
						lastInstant.set(0, instant);
						currentReplayThread = Thread.currentThread();
						Thread.sleep(delay);
//						Thread.sleep(0);
						boolean send = true;
						if (ignoreMessageTypes.contains(message_type)) {
							if (ignoreSubTypes.contains(sub_type)) {
								send = false;
							}
						}
						if (ignoreSources.contains(source)) {
							send = false;
						}
						if (ignoreTopics.contains(topic)) {
							send = false;
						}
						if (send) {
							replayMessagePublisher.send(objectMapper.writeValueAsBytes(message), topic)
									.subscribe(() -> {
										// handle completion
										logger.trace(MessageFormat.format("{0} [{1}] : {2}", timestamp, topic,
												objectMapper.writeValueAsString(message)));
										// messageDestinationCount.set(0, messageDestinationCount.get(0) + 1);
									}, throwable -> {
										logger.error(throwable.getMessage());
									});
						} else {
							logger.trace("Skipping message.");
						}
						ReplayMessageCountMessage replayMessageCountMessage = new ReplayMessageCountMessage(
								replay.getReplayId(), currentMessageCount, totalMessageCount);
						replayMessageCountPublisher.send(objectMapper.writeValueAsBytes(replayMessageCountMessage))
								.subscribe(() -> {
									// handle completion
								}, throwable -> {
									logger.error(throwable.getMessage());
								});

					} catch (JsonProcessingException e) {
						logger.error(e.getMessage());
					} catch (InterruptedException e) {
						// logger.error(e.getMessage());
						logger.error(MessageFormat.format("{0} [{1}] canceled replay [{2]}.", replay.getReplayParentType(), replay.getReplayParentId(), replay.getReplayId()));
					}
				}

				SearchScrollRequest scrollRequest = new SearchScrollRequest(scrollId);
				scrollRequest.scroll(scroll);
				searchResponse = elasticsearchClient.scroll(scrollRequest, RequestOptions.DEFAULT);
				scrollId = searchResponse.getScrollId();
				searchHits = searchResponse.getHits().getHits();
			}

//        logger.info(MessageFormat.format("SOURCE: {0} DESTINATION: {1}", messageSourceCount.get(0), messageDestinationCount.get(0)));
			ClearScrollRequest clearScrollRequest = new ClearScrollRequest();
			clearScrollRequest.addScrollId(scrollId);
			ClearScrollResponse clearScrollResponse = elasticsearchClient.clearScroll(clearScrollRequest,
					RequestOptions.DEFAULT);

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
				reason = ReplayCompletedReasonType.ERROR;
			}
			reset();
		} catch (IOException e) {
			logger.error(e.getMessage());
			if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
				reason = ReplayCompletedReasonType.ERROR;
			}
			reset();
		}
	}
	
	public List<Replay> apiRunTrial(@NonNull @NotNull List<ReplayObject> replayObjects, @NonNull @NotNull List<IgnoreMessageListItem> ignoreMessageList, @NotNull List<String> ignoreSourceList, @NotNull List<String> ignoreTopicList, @NonNull @NotNull boolean restart, @NonNull @NotNull String index) {
		if (replayRunning) {
			logger.error("There is a reaply already running!");
			return null;
		}
		replayRunning = true;
		try {
			Map<String, String> asiMap = new HashMap<String, String>();
			List<Replay> replays = new ArrayList<Replay>();
//			replayObjects.forEach(replayObject -> {
			for (int i = 0; i < replayObjects.size(); i++) {
				ReplayObject replayObject = replayObjects.get(i);				
				if (replayObject.getType().toUpperCase().equals("ASI")) {
					if (i + 1 < replayObjects.size()) {
						String asi = replayObject.getId();
						String nextReplayParentId = replayObjects.get(i + 1).getId();
						asiMap.put(nextReplayParentId, asi);
					}
				} else { // Should all be TRIAL types here.
					String replayParentId = replayObject.getId();
					Replay replay = new Replay(-1, UUID.randomUUID().toString(), replayParentId, "TRIAL",	Instant.now().toString(), ignoreMessageList, ignoreSourceList, ignoreTopicList);
					Replay newReplay = createReplay(replay);
					if (newReplay != null) {
						runningReplayId = newReplay.getReplayId();
						logger.info(MessageFormat.format("{0} [{1}] created replay [{2}].", newReplay.getReplayParentType(), newReplay.getReplayParentId(), newReplay.getReplayId()));
						replays.add(newReplay);
					} else {
						logger.info(MessageFormat.format("[{0}] could not be create replay!", replay.getReplayId()));
//					replayRunning = false;
//					runningReplayId = "";
					}
				}
			};
			
			if (replays.size() > 0) {
				// Start replay here!
				AtomicInteger counter = new AtomicInteger();
				Observable
					.fromIterable(replays)
					.map(r -> messageWorker(r, index, restart, asiMap.get(r.getReplayParentId()) == null ? null : asiMap.get(r.getReplayParentId())))
					.subscribeOn(Schedulers.computation())
					.doOnError(error -> logger.error(error.getMessage()))
					.subscribe(
							x -> {
								// On next
								logger.info("Replay completed.");
							},
							error -> {
								// logger.error(error.getMessage());
								if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
									reason = ReplayCompletedReasonType.ERROR;
								}
								reset();
							},
							() -> {
								logger.info("Replay finished.");
								if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
									reason = ReplayCompletedReasonType.FINISHED;
								}
								reset();
							});

			} else {
				logger.info("No replays could not be created.");
				replayRunning = false;
				runningReplayId = "";
				return null;
			}
			return replays;
		} catch (Exception e) {
			logger.error(e.getMessage());
			reset();
			return null;
		}
	}
	
	public List<Replay> apiRunReplay(@NonNull @NotNull List<ReplayObject> replayObjects, @NonNull @NotNull List<IgnoreMessageListItem> ignoreMessageList, @NotNull List<String> ignoreSourceList, @NotNull List<String> ignoreTopicList, @NonNull @NotNull boolean restart, @NonNull @NotNull String index) {
		if (replayRunning) {
			logger.error("There is a reaply already running!");
			return null;
		}
		replayRunning = true;
		try {
			Map<String, String> asiMap = new HashMap<String, String>();
			List<Replay> replays = new ArrayList<Replay>();
//			replayObjects.forEach(replayObject -> {
			for (int i = 0; i < replayObjects.size(); i++) {
				ReplayObject replayObject = replayObjects.get(i);				
				if (replayObject.getType().toUpperCase().equals("ASI")) {
					if (i + 1 < replayObjects.size()) {
						String asi = replayObject.getId();
						String nextReplayParentId = replayObjects.get(i + 1).getId();
						asiMap.put(nextReplayParentId, asi);
					}
				} else { // Should all be REPLAY types here.
					String replayParentId = replayObject.getId();
					Replay replay = new Replay(-1, UUID.randomUUID().toString(), replayParentId, "REPLAY",	Instant.now().toString(), ignoreMessageList, ignoreSourceList, ignoreTopicList);
					Replay newReplay = createReplay(replay);
					if (newReplay != null) {
						runningReplayId = newReplay.getReplayId();
						logger.info(MessageFormat.format("{0} [{1}] created replay [{2}].", newReplay.getReplayParentType(), newReplay.getReplayParentId(), newReplay.getReplayId()));
						replays.add(newReplay);
					} else {
						logger.info(MessageFormat.format("[{0}] could not be create replay!", replay.getReplayId()));
//					replayRunning = false;
//					runningReplayId = "";
					}
				}
			};
			
			if (replays.size() > 0) {
				// Start replay here!
				AtomicInteger counter = new AtomicInteger();
				Observable
					.fromIterable(replays)
					.map(r -> messageWorker(r, index, restart, asiMap.get(r.getReplayParentId()) == null ? null : asiMap.get(r.getReplayParentId())))
					.subscribeOn(Schedulers.computation())
					.doOnError(error -> logger.error(error.getMessage()))
					.subscribe(
							x -> {
								// On next
								logger.info("Replay completed.");
							},
							error -> {
								// logger.error(error.getMessage());
								if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
									reason = ReplayCompletedReasonType.ERROR;
								}
								reset();
							},
							() -> {
								logger.info("Replay finished.");
								if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
									reason = ReplayCompletedReasonType.FINISHED;
								}
								reset();
							});

			} else {
				logger.info("No replays could not be created.");
				replayRunning = false;
				runningReplayId = "";
				return null;
			}
			return replays;
		} catch (Exception e) {
			logger.error(e.getMessage());
			reset();
			return null;
		}
	}

	@Override
	public Replay runReplay(@NonNull @NotNull MessageReplay messageReplay, @NonNull @NotNull String index) {
		if (replayRunning) {
			logger.error("There is a reaply already running!");
			return null;
		}
		replayRunning = true;
		try {
			Replay replay = new Replay(-1, messageReplay.getMsg().getReplayId(),
					messageReplay.getMsg().getReplayParentId(), messageReplay.getMsg().getReplayParentType(),
					messageReplay.getMsg().getTimestamp(), messageReplay.getData().getIgnoreMessageList(), messageReplay.getData().getIgnoreSourceList(), messageReplay.getData().getIgnoreTopicList());
			Replay newReplay = createReplay(replay);
			if (newReplay != null) {
				runningReplayId = newReplay.getReplayId();
				logger.info(MessageFormat.format("Run replay {0} created.", newReplay.getReplayId()));

				// Start replay here!
				Observable
					.just(newReplay)
					.map(r -> messageWorker(r, index, false, null))
					.subscribeOn(Schedulers.computation())
					.doOnError(error -> logger.error(error.getMessage()))
					.subscribe(
							x -> {
								// On next
								// logger.info(MessageFormat.format("Run replay successful: {0}", x));
							},
							error -> {
								// logger.error(error.getMessage());
								if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
									reason = ReplayCompletedReasonType.ERROR;
								}
								reset();
							},
							() -> {
								logger.info("Run replay finished.");
								if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
									reason = ReplayCompletedReasonType.FINISHED;
								}
								reset();
							});

			} else {
				logger.info(MessageFormat.format("Run replay {0} could not be created.", replay.getReplayId()));
				replayRunning = false;
				runningReplayId = "";
				return null;
			}
			return newReplay;
		} catch (Exception e) {
			logger.error(e.getMessage());
			reset();
			return null;
		}
	}

	private Observable<Boolean> messageWorker(Replay replay, String index, boolean restart, String asi) {
		logger.info(MessageFormat.format("{0} [{1}] running replay [{2}].", replay.getReplayParentType(), replay.getReplayParentId(), replay.getReplayId()));
		interrupter = PublishSubject.create();
		try {
			// Start ASI if not null
			if (asi != null) {
				logger.info(MessageFormat.format("Starting up {0}.", asi));
				agentClient.agentsUp(asi);
				logger.info(MessageFormat.format("Starting up {0} complete.", asi));
			}
			
			final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(15L));
			SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

			BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
			if (replay.getReplayParentType().equals("TRIAL")) {
				boolQueryBuilder.must(QueryBuilders.matchQuery("msg.trial_id.keyword", replay.getReplayParentId()));
				boolQueryBuilder.mustNot(QueryBuilders.existsQuery("msg.replay_id"));
			} else {
				boolQueryBuilder.must(QueryBuilders.matchQuery("msg.replay_id.keyword", replay.getReplayParentId()));
			}

			List<String> ignoreMessageTypes = new ArrayList<String>();
			List<String> ignoreSubTypes = new ArrayList<String>();
			replay.getIgnoreMessageList().forEach(ingnoreListItem -> {
				ignoreMessageTypes.add(ingnoreListItem.getMessageType());
				ignoreSubTypes.add(ingnoreListItem.getSubType());
			});
			List<String> ignoreSources = new ArrayList<String>();
			replay.getIgnoreSourceList().forEach(source -> {
				ignoreSources.add(source);
			});
			List<String> ignoreTopics = new ArrayList<String>();
			replay.getIgnoreTopicList().forEach(topic -> {
				ignoreTopics.add(topic);
			});

			SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
			searchSourceBuilder.fetchSource(null, "message");
			searchSourceBuilder.sort("@timestamp", SortOrder.ASC);
			searchSourceBuilder.query(boolQueryBuilder);

			searchRequest.source(searchSourceBuilder);

			SearchResponse searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);

			String scrollId = searchResponse.getScrollId();

			TotalHits totalHits = searchResponse.getHits().getTotalHits();
			totalMessageCount = totalHits.value;
			SearchHit[] searchHits = searchResponse.getHits().getHits();

			List<Instant> lastInstant = new ArrayList<Instant>();
			lastInstant.add(null);
			// List<Integer> messageSourceCount = new ArrayList<Integer>();
			// messageSourceCount.add(0);
			// List<Integer> messageDestinationCount = new ArrayList<Integer>();
			// messageDestinationCount.add(1);
			currentMessageCount = 0;
			logger.info(MessageFormat.format("Running new replay on replay parent id {0} consisting of {1} messages", replay.getReplayParentId(), totalMessageCount));
			while (searchHits != null && searchHits.length > 0) {
				// messageSourceCount.set(0, messageSourceCount.get(0) + searchHits.length);
				// Arrays.stream(searchHits).forEach(searchHit -> {
				for (SearchHit searchHit : searchHits) {
					currentMessageCount = currentMessageCount + 1;
					Map<String, Object> sourceMap = searchHit.getSourceAsMap();
					String timestamp = sourceMap.get("@timestamp").toString();
					String topic = sourceMap.get("topic").toString();
					Map<String, Object> message = new HashMap<String, Object>();
					String strHeader = objectMapper.writeValueAsString(sourceMap.remove("header"));
					Header header = objectMapper.readValue(strHeader, Header.class);
					message.put("header", header);
					String strMsg = objectMapper.writeValueAsString(sourceMap.remove("msg"));
					Msg msg = objectMapper.readValue(strMsg, Msg.class);
					msg.setReplayId(replay.getReplayId());
					msg.setReplayParentId(replay.getReplayParentId());
					msg.setReplayParentType(replay.getReplayParentType());
					message.put("msg", msg);
					message.put("data", sourceMap.remove("data"));
					String message_type = header.getMessageType();
					String sub_type = msg.getSubType();
					String source = msg.getSource();
					try {
						Instant instant = Instant.parse(timestamp);
						long delay = ChronoUnit.MILLIS.between(lastInstant.get(0) != null ? lastInstant.get(0) : instant, instant);
						if (delay > 15000)
							delay = 15000;
						lastInstant.set(0, instant);
						currentReplayThread = Thread.currentThread();
						Thread.sleep(delay);
//						Thread.sleep(0);
						boolean send = true;
						if (ignoreMessageTypes.contains(message_type)) {
							if (ignoreSubTypes.contains(sub_type)) {
								send = false;
							}
						}
						if (ignoreSources.contains(source)) {
							send = false;
						}
						if (ignoreTopics.contains(topic)) {
							send = false;
						}
						if (send) {
							replayMessagePublisher.send(objectMapper.writeValueAsBytes(message), topic)
									.subscribe(() -> {
										// handle completion
										logger.trace(MessageFormat.format("{0} [{1}] : {2}", timestamp, topic,
												objectMapper.writeValueAsString(message)));
										// messageDestinationCount.set(0, messageDestinationCount.get(0) + 1);
									}, throwable -> {
										logger.error(throwable.getMessage());
									});
						} else {
							logger.trace("Skipping message.");
						}
						ReplayMessageCountMessage replayMessageCountMessage = new ReplayMessageCountMessage(
								replay.getReplayId(), currentMessageCount, totalMessageCount);
						replayMessageCountPublisher.send(objectMapper.writeValueAsBytes(replayMessageCountMessage))
								.subscribe(() -> {
									// handle completion
								}, throwable -> {
									logger.error(throwable.getMessage());
								});

					} catch (JsonProcessingException e) {
						logger.error(e.getMessage());
						logger.error(MessageFormat.format("{0} [{1}] canceled replay [{2]}.", replay.getReplayParentType(), replay.getReplayParentId(), replay.getReplayId()));
						return Observable.just(false).takeUntil(interrupter);
					} catch (InterruptedException e) {
						// logger.error(e.getMessage());
						logger.error(MessageFormat.format("{0} [{1}] canceled replay [{2]}.", replay.getReplayParentType(), replay.getReplayParentId(), replay.getReplayId()));
						return Observable.just(false).takeUntil(interrupter);
					}
				}

				SearchScrollRequest scrollRequest = new SearchScrollRequest(scrollId);
				scrollRequest.scroll(scroll);
				searchResponse = elasticsearchClient.scroll(scrollRequest, RequestOptions.DEFAULT);
				scrollId = searchResponse.getScrollId();
				searchHits = searchResponse.getHits().getHits();
			}

			// logger.info(MessageFormat.format("SOURCE: {0} DESTINATION: {1}", messageSourceCount.get(0), messageDestinationCount.get(0)));
			ClearScrollRequest clearScrollRequest = new ClearScrollRequest();
			clearScrollRequest.addScrollId(scrollId);
			ClearScrollResponse clearScrollResponse = elasticsearchClient.clearScroll(clearScrollRequest,
					RequestOptions.DEFAULT);
			
			// Stop ASI if not null
			if (asi != null) {
				logger.info(MessageFormat.format("Shutting down {0}.", asi));
				agentClient.agentsDown(asi);
				logger.info(MessageFormat.format("Shutting down {0} complete.", asi));
			}
			
			if (restart) {
				// Restart AC scripts
				logger.info("Restaring AC agents.");
				logger.info("Shutting down AC agents.");
				agentClient.agentsScriptDown();
				logger.info("Shutting down AC agents complete.");
				logger.info("Starting up AC agents.");				
				agentClient.agentsScriptUp();
				logger.info("Starting up AC agents complete.");
			}

			boolean succeeded = clearScrollResponse.isSucceeded();
			return Observable.just(succeeded).takeUntil(interrupter);

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
				reason = ReplayCompletedReasonType.ERROR;
			}
			reset();
			return null;
		} catch (IOException e) {
			logger.error(e.getMessage());
			if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
				reason = ReplayCompletedReasonType.ERROR;
			}
			reset();
			return null;
		} catch (Exception e) {
			logger.error(e.getMessage());
			if (reason.equals(ReplayCompletedReasonType.UNKNOWN)) {
				reason = ReplayCompletedReasonType.ERROR;
			}
			reset();
			return null;
		}
	}

	private void reset() {
		ReplayCompletedMessage replayCompletedMessage = new ReplayCompletedMessage(runningReplayId, reason,
				currentMessageCount, totalMessageCount);
		interrupter = null;
		currentReplayThread = null;
		replayRunning = false;
		currentMessageCount = 0;
		totalMessageCount = 0;
		reason = ReplayCompletedReasonType.UNKNOWN;
		runningReplayId = "";
		try {
			replayCompletedPublisher.send(objectMapper.writeValueAsBytes(replayCompletedMessage)).subscribe(() -> {
				// handle completion
			}, throwable -> {
				logger.error(throwable.getMessage());
			});
		} catch (JsonProcessingException e) {
			logger.error(e.getMessage());
		}
	}

	@Override
	public boolean abortReplay() {
		if (interrupter != null) {
			interrupter.onNext(true);
			currentReplayThread.interrupt();
			reason = ReplayCompletedReasonType.ABORTED;
			return true;
		}
		return false;
	}

	@Override
	public String findReplayRootId(String replayId) {
		try {
			String sql = "WITH recursive tree(child, root) AS\r\n"
					+ "(\r\n"
					+ "          SELECT    c.replay_id,\r\n"
					+ "                    c.replay_parent_id\r\n"
					+ "          FROM      replays c\r\n"
					+ "          LEFT JOIN replays p\r\n"
					+ "          ON        c.replay_parent_id = p.replay_id\r\n"
					+ "          WHERE     p.replay_parent_id IS NULL\r\n"
					+ "          UNION\r\n"
					+ "          SELECT     replay_id,\r\n"
					+ "                     root\r\n"
					+ "          FROM       tree\r\n"
					+ "          INNER JOIN replays\r\n"
					+ "          ON         tree.child = replays.replay_parent_id )\r\n"
					+ "SELECT root\r\n"
					+ "FROM   tree\r\n"
					+ "WHERE  child = $1";
			RowSet<Row> rowSet = postgresClient.preparedQuery(sql).rxExecute(Tuple.of(UUID.fromString(replayId)))
					.blockingGet();
			if (rowSet.size() > 1) {
				logger.error(MessageFormat.format("More than one root found for replay uuid: {0}!", replayId));
				return null;
			} else if (rowSet.size() <= 0) {
				logger.error(MessageFormat.format("Root not found for replay uuid: {0}!", replayId));
				return null;
			} else {
				String rootId = null;
				RowIterator<Row> rowIterator = rowSet.iterator();
				while (rowIterator.hasNext()) {
					Row row = rowIterator.next();
					rootId = row.getUUID("root").toString();
				}
				return rootId;
			}

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
	}

	@Override
	public Trial findReplayRootTrial(String replayId) {
		List<Trial> trials = new LinkedList<>();
		try {
			String sql = "WITH RECURSIVE tree(child, root) AS (\r\n" + "SELECT\r\n" + "   c.replay_id,\r\n"
					+ "   c.replay_parent_id\r\n" + "FROM\r\n" + "   replays c\r\n" + "LEFT JOIN\r\n"
					+ "   replays p ON c.replay_parent_id = p.replay_id\r\n" + "WHERE\r\n"
					+ "   p.replay_parent_id IS NULL\r\n" + "   UNION\r\n" + "   SELECT\r\n" + "      replay_id,\r\n"
					+ "      root\r\n" + "   FROM\r\n" + "      tree\r\n" + "   INNER JOIN\r\n"
					+ "      replays on tree.child = replays.replay_parent_id	\r\n" + ")\r\n"
					+ "SELECT root FROM tree where child = $1";
			RowSet<Row> rowSet = postgresClient.preparedQuery(sql).rxExecute(Tuple.of(UUID.fromString(replayId)))
					.blockingGet();
			if (rowSet.size() > 1) {
				logger.error(MessageFormat.format("More than one root found for replay uuid: {0}!", replayId));
				return null;
			} else if (rowSet.size() <= 0) {
				logger.error(MessageFormat.format("Root not found for replay uuid: {0}!", replayId));
				return null;
			} else {
				RowIterator<Row> rowIterator = rowSet.iterator();
				while (rowIterator.hasNext()) {
					Row row = rowIterator.next();
					Trial trial = defaultTrialService.readTrialUUID(row.getUUID("root").toString());
					trials.add(trial);
				}
			}

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
		if (trials.isEmpty()) {
			logger.info(MessageFormat.format("No trial root using uuid: {0} found!", replayId));
			return null;
		}
		return trials.iterator().next();
	}

	@Override
	public List<Object> findReplayParents(String replayId) {
		List<Object> replays = new LinkedList<>();
		try {
			String sql = "WITH RECURSIVE parent (replay_parent_id, replay_id, replay_parent_type, level) AS\r\n"
					+ "(\r\n"
					+ "       SELECT replay_parent_id,\r\n"
					+ "              replay_id,\r\n"
					+ "              replay_parent_type,\r\n"
					+ "              0 AS level\r\n"
					+ "       FROM   replays c\r\n"
					+ "       WHERE  replay_id = $1\r\n"
					+ "       UNION ALL\r\n"
					+ "       SELECT     c.replay_parent_id,\r\n"
					+ "                  c.replay_id,\r\n"
					+ "                  c.replay_parent_type,\r\n"
					+ "                  level + 1\r\n"
					+ "       FROM       replays c\r\n"
					+ "       INNER JOIN parent p\r\n"
					+ "       ON         p.replay_parent_id = c.replay_id )\r\n"
					+ "SELECT replay_id, replay_parent_id, replay_parent_type, level\r\n"
					+ "FROM   parent\r\n"
					+ "ORDER  BY level ASC;";
			RowSet<Row> rowSet = postgresClient.preparedQuery(sql).rxExecute(Tuple.of(UUID.fromString(replayId)))
					.blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				String replayParentId = row.getUUID("replay_parent_id").toString();
				String replayParentType = row.getString("replay_parent_type");
				switch (replayParentType) {
				case "TRIAL":
					Trial trial = this.defaultTrialService.readTrialUUID(replayParentId);
					if (trial != null) {
						replays.add(trial);
					} else {
						logger.error(MessageFormat.format("Error reading Trial using uuid: {0}", replayParentId));
						return new LinkedList<>();
					}
					break;
				case "REPLAY":
					Replay replay = this.readReplayUUID(replayParentId);
					if (replay != null) {
						replays.add(replay);
					} else {
						logger.error(MessageFormat.format("Error reading Replay using uuid: {0}", replayParentId));
						return new LinkedList<>();
					}
				}

			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
		return replays;
	}
	
	@NonNull
	public SystemFile exportFile(@NonNull @NotNull String replayId, @NonNull @NotNull String index) {
		logger.info(MessageFormat.format("Exporting temporary file using replay [{0}] from index {1}.", replayId, index));
		try {
			Replay replay = readReplayUUID(replayId);		
			if (replay == null) {
				logger.error(MessageFormat.format("Export aborted! No replay found with id: [{0}].", replayId));
				return null;
			}
			List<Object> parents = findReplayParents(replayId);
			Trial root = findReplayRootTrial(replayId);

			// Need to confirm if we want the same filename logic we use for exporting trials.  
			// String HEADER_METADATA_FILE_PREFIX = MessageFormat.format(
			//		"TrialMessages_CondBtwn-{0}_CondWin-{1}-StaticMap_Trial-{2}_Team-na_Member-{3}_Vers-{4}",
			//		trial.getCondition(), trial.getExperiment().getMission(), trial.getTrialNumber(),
			//		String.join("-", trial.getSubjects()), trial.getTestbedVersion());
			String HEADER_METADATA_FILE_PREFIX = replay.getReplayId();
			String HEADER_METADATA_FILENAME = HEADER_METADATA_FILE_PREFIX + HEADER_METADATA_FILE_SUFIX;
			File file = File.createTempFile(HEADER_METADATA_FILE_PREFIX, HEADER_METADATA_FILE_SUFIX);
			logger.info(MessageFormat.format("File name: {0}.", HEADER_METADATA_FILENAME));
			PrintWriter printWriter = new PrintWriter(new FileWriter(file));

			// Add metadata json file header.
			MessageReplayExport messageReplayExport = MessageReplayExport.generate(parents, root, replay, index);
			printWriter.println(objectMapper.writeValueAsString(messageReplayExport));

			final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(30L));
			SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

			MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("msg.replay_id.keyword", replayId);

			SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
			searchSourceBuilder.size(1000);
			searchSourceBuilder.fetchSource(null, "message");
			searchSourceBuilder.sort("@timestamp", SortOrder.ASC);
			searchSourceBuilder.query(matchQueryBuilder);

			searchRequest.source(searchSourceBuilder);

			SearchResponse searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);

			String scrollId = searchResponse.getScrollId();

			TotalHits totalHits = searchResponse.getHits().getTotalHits();
			totalMessageCount = totalHits.value;
			SearchHit[] searchHits = searchResponse.getHits().getHits();

			List<Instant> lastInstant = new ArrayList<Instant>();
			lastInstant.add(null);
			currentMessageCount = 0;
			while (searchHits != null && searchHits.length > 0) {
				for (SearchHit searchHit : searchHits) {
					currentMessageCount = currentMessageCount + 1;
					String source = searchHit.getSourceAsString();
					printWriter.println(source);
				}
				SearchScrollRequest scrollRequest = new SearchScrollRequest(scrollId);
				scrollRequest.scroll(scroll);
				searchResponse = elasticsearchClient.scroll(scrollRequest, RequestOptions.DEFAULT);
				scrollId = searchResponse.getScrollId();
				searchHits = searchResponse.getHits().getHits();
			}

			ClearScrollRequest clearScrollRequest = new ClearScrollRequest();
			clearScrollRequest.addScrollId(scrollId);
			ClearScrollResponse clearScrollResponse = elasticsearchClient.clearScroll(clearScrollRequest, RequestOptions.DEFAULT);

			printWriter.close();

			logger.info(MessageFormat.format("Exported {0} documents successfully.", currentMessageCount));
			return new SystemFile(file).attach(HEADER_METADATA_FILENAME);
		} catch (IOException e) {
			logger.error(e.getMessage());
		}		
		throw new HttpStatusException(HttpStatus.SERVICE_UNAVAILABLE, "error exporting trial");
	}

	@NonNull
	public StreamedFile exportStreamed(@NonNull @NotNull String replayId, @NonNull @NotNull String index) {
		logger.info(MessageFormat.format("Exporting streamed file using replay [{0}] from index {1}.", replayId, index));
		PipedInputStream pipedInputStream = new PipedInputStream();
		PipedOutputStream pipedOutputStream = new PipedOutputStream();
		Replay replay = readReplayUUID(replayId);
		if (replay == null) {
			logger.error(MessageFormat.format("Export aborted! No replay found with id: [{0}].", replayId));
			return null; 
		}
		List<Object> parents = findReplayParents(replayId);
		Trial root = findReplayRootTrial(replayId);

		// Need to confirm if we want the same filename logic we use for exporting trials.  	
		// String HEADER_METADATA_FILE_PREFIX = MessageFormat.format(
		//		"TrialMessages_CondBtwn-{0}_CondWin-{1}-StaticMap_Trial-{2}_Team-na_Member-{3}_Vers-{4}",
		//		trial.getCondition(), trial.getExperiment().getMission(), trial.getTrialNumber(),
		//		String.join("-", trial.getSubjects()), trial.getTestbedVersion());
		String HEADER_METADATA_FILE_PREFIX = replay.getReplayId();
		String HEADER_METADATA_FILENAME = HEADER_METADATA_FILE_PREFIX + HEADER_METADATA_FILE_SUFIX;
		logger.info(MessageFormat.format("File name: {0}.", HEADER_METADATA_FILENAME));
		executorService.execute(() -> {
			try {
				pipedOutputStream.connect(pipedInputStream);

				PrintWriter printWriter = new PrintWriter(pipedOutputStream);

				// Add metadata json file header.
				MessageReplayExport messageReplayExport = MessageReplayExport.generate(parents, root, replay, index);
				printWriter.println(objectMapper.writeValueAsString(messageReplayExport));

				final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(30L));
				SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);
		
				MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("msg.replay_id.keyword", replayId);

				SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
				searchSourceBuilder.size(1000);
				searchSourceBuilder.fetchSource(null, "message");
				searchSourceBuilder.sort("@timestamp", SortOrder.ASC);
				searchSourceBuilder.query(matchQueryBuilder);

				searchRequest.source(searchSourceBuilder);

				SearchResponse searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);

				String scrollId = searchResponse.getScrollId();

				TotalHits totalHits = searchResponse.getHits().getTotalHits();
				totalMessageCount = totalHits.value;
				SearchHit[] searchHits = searchResponse.getHits().getHits();

				List<Instant> lastInstant = new ArrayList<Instant>();
				lastInstant.add(null);
				currentMessageCount = 0;
				while (searchHits != null && searchHits.length > 0) {
					for (SearchHit searchHit : searchHits) {
						currentMessageCount = currentMessageCount + 1;
						String source = searchHit.getSourceAsString();
						printWriter.println(source);
					}
					SearchScrollRequest scrollRequest = new SearchScrollRequest(scrollId);
					scrollRequest.scroll(scroll);
					searchResponse = elasticsearchClient.scroll(scrollRequest, RequestOptions.DEFAULT);
					scrollId = searchResponse.getScrollId();
					searchHits = searchResponse.getHits().getHits();
				}

				ClearScrollRequest clearScrollRequest = new ClearScrollRequest();
				clearScrollRequest.addScrollId(scrollId);
				ClearScrollResponse clearScrollResponse = elasticsearchClient.clearScroll(clearScrollRequest, RequestOptions.DEFAULT);

				printWriter.close();
				pipedOutputStream.flush();
				pipedOutputStream.close();
				logger.info(MessageFormat.format("Exported {0} documents successfully.", currentMessageCount));
			} catch (IOException e) {
				logger.error(e.getMessage());
			}

		});
		return new StreamedFile(pipedInputStream, MediaType.TEXT_PLAIN_TYPE).attach(HEADER_METADATA_FILENAME);
	}

	public MessageApiResult importFile(@NonNull @NotNull byte[] bytes, @NonNull @NotNull String filename, @NonNull @NotNull String index, @NonNull @NotNull boolean createIndex) {
		logger.info(MessageFormat.format("Importing {0} into index {1} [creating: {2}].", filename, index, createIndex));
		InputStream inputStream = null;
		BufferedReader bufferedReader = null;
		try {
			// Read in the file
			inputStream = new ByteArrayInputStream(bytes);
			bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

			// Create the index
			if (createIndex) {
				logger.info(MessageFormat.format("Creating index {0}.", index));
			    GetIndexRequest getIndexRequest = new GetIndexRequest(index);
			    boolean exists = elasticsearchClient.indices().exists(getIndexRequest, RequestOptions.DEFAULT);
			    if(!exists) {
			    	CreateIndexRequest createIndexRequest = new CreateIndexRequest(index);
			    	createIndexRequest.settings(Settings.builder() 
			    		    .put("index.lifecycle.name", "logstash-policy")
			    		    .put("index.lifecycle.rollover_alias", "logstash")
			    		    .put("index.refresh_interval", "5s")
			    		);
			    	createIndexRequest.mapping("{\r\n"
			    			+ "  \"dynamic\": false,\r\n"
			    			+ "  \"properties\": {\r\n"
			    			+ "    \"header\": {\r\n"
			    			+ "      \"properties\": {\r\n"
			    			+ "        \"message_type\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        }\r\n"
			    			+ "      }\r\n"
			    			+ "    },\r\n"
			    			+ "    \"msg\": {\r\n"
			    			+ "      \"properties\": {\r\n"
			    			+ "        \"trial_id\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"experiment_id\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"replay_id\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"replay_parent_id\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"replay_parent_type\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"source\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"sub_type\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"timestamp\": {\r\n"
			    			+ "          \"type\": \"date\"\r\n"
			    			+ "        },\r\n"
			    			+ "        \"name\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"testbed_version\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        }\r\n"
			    			+ "      }\r\n"
			    			+ "    },\r\n"
			    			+ "    \"topic\": {\r\n"
			    			+ "      \"type\": \"text\",\r\n"
			    			+ "      \"norms\": false,\r\n"
			    			+ "      \"fields\": {\r\n"
			    			+ "        \"keyword\": {\r\n"
			    			+ "          \"type\": \"keyword\",\r\n"
			    			+ "          \"ignore_above\": 256\r\n"
			    			+ "        }\r\n"
			    			+ "      }\r\n"
			    			+ "    },\r\n"
			    			+ "    \"@timestamp\": {\r\n"
			    			+ "      \"type\": \"date\"\r\n"
			    			+ "    },\r\n"
			    			+ "    \"@version\": {\r\n"
			    			+ "      \"type\": \"keyword\"\r\n"
			    			+ "    },\r\n"
			    			+ "    \"error\": {\r\n"
			    			+ "      \"properties\": {\r\n"
			    			+ "        \"reason\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"plugin_id\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        },\r\n"
			    			+ "        \"plugin_type\": {\r\n"
			    			+ "          \"type\": \"text\",\r\n"
			    			+ "          \"norms\": false,\r\n"
			    			+ "          \"fields\": {\r\n"
			    			+ "            \"keyword\": {\r\n"
			    			+ "              \"type\": \"keyword\",\r\n"
			    			+ "              \"ignore_above\": 256\r\n"
			    			+ "            }\r\n"
			    			+ "          }\r\n"
			    			+ "        }\r\n"
			    			+ "      }\r\n"
			    			+ "    }\r\n"
			    			+ "  }\r\n"
			    			+ "}",
			    			XContentType.JSON);
			    	CreateIndexResponse createIndexResponse = elasticsearchClient.indices().create(createIndexRequest, RequestOptions.DEFAULT);
			    	boolean acknowledged = createIndexResponse.isAcknowledged();
			    	logger.info(MessageFormat.format("Create index response acknowledged: {0}.", acknowledged));
			    } else {
			    	logger.info(MessageFormat.format("Index [{0}] could not be created because it already exists!.", index));
			    }
			}
			// Prepare bulk insert by adding json documents from the file to the request.
			BulkRequest bulkRequest = new BulkRequest();
			int line = 0;
			while (bufferedReader.ready()) {
				String json = bufferedReader.readLine();
				// If there is a header then process it.
				if (line == 0) {
					MessageReplayExport messageReplayExport = objectMapper.readValue(json, MessageReplayExport.class);
					
					// Check to see if the trialId is already present in elasticsearch.
					String replayId = messageReplayExport.getMsg().getReplayId();
					// Check to see if index already has a document with this trial id.
					SearchRequest searchRequest = new SearchRequest(index);

					MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("msg.replay_id.keyword", replayId);

					SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
					searchSourceBuilder.size(0);
					searchSourceBuilder.fetchSource(null, "message");
					searchSourceBuilder.query(matchQueryBuilder);

					searchRequest.source(searchSourceBuilder);

					SearchResponse searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);

					TotalHits totalHits = searchResponse.getHits().getTotalHits();
					totalMessageCount = totalHits.value;
					
					if (totalMessageCount > 0) {
						return new MessageApiResult("failure", MessageFormat.format("Imported aborted! Replay: [{0}] already exists in index: [{1}]", replayId, index), new HashMap<String, String>());
					}
					
					// Trial should always be first in list (root).
					List<Object> parents = messageReplayExport.getData().getMetadata().getParents(); 
					Trial trial = (Trial) objectMapper.readValue(objectMapper.writeValueAsString(parents.get(0)), Trial.class);
					// Create experiment
					Experiment experiment = new Experiment(
						-1,
						trial.getExperiment().getExperimentId(),
						trial.getExperiment().getName(),
						trial.getExperiment().getDate(),
						trial.getExperiment().getAuthor(),
						trial.getExperiment().getMission()
						);
					logger.info(MessageFormat.format("Creating experiment [{0}] found in header.", experiment.getExperimentId()));
					defaultExperimentService.createExperiment(experiment);					
					// Create trial
					logger.info(MessageFormat.format("Creating trial [{0}] found in header.", trial.getTrialId()));
					defaultTrialService.createTrial(trial);
					// Create replays (if any)
					Replay replay = messageReplayExport.getData().getMetadata().getReplay();
					createReplay(replay);
					for (int i = 1; i < parents.size(); i++) {
						Replay pReplay = (Replay) parents.get(i);
						createReplay(pReplay);
					}
				} else {
					IndexRequest indexRequest = new IndexRequest(index).source(json, XContentType.JSON);
					bulkRequest.add(indexRequest);
				}
				line++;
			}
			logger.info(MessageFormat.format("Bulk indexing [{0}] documents found in file [total estimated size: {1} MB ].", bulkRequest.requests().size(), bulkRequest.estimatedSizeInBytes() / (1024 * 1024)));
			BulkResponse bulkResponse = elasticsearchClient.bulk(bulkRequest, RequestOptions.DEFAULT);
			int errorCount = 0;
			BulkItemResponse[] bulkItemResponse = bulkResponse.getItems();			
			if (bulkResponse.hasFailures()) {				
				for (int i = 0; i < bulkItemResponse.length; i++) {
					if (bulkItemResponse[i].isFailed()) {
						errorCount++;
						BulkItemResponse.Failure failure = bulkItemResponse[i].getFailure(); 
						logger.error(failure.getMessage());
					}
					
				}
			}
			logger.info(MessageFormat.format("Imported {0} out of {1} documents with {2} errors.", bulkItemResponse.length - errorCount, bulkItemResponse.length, errorCount));
			return new MessageApiResult("success", MessageFormat.format("Imported {0} out of {1} documents with {2} errors.", bulkItemResponse.length - errorCount, bulkItemResponse.length, errorCount), new HashMap<String, String>());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			logger.error(e.getMessage());
			return new MessageApiResult("failure", e.getMessage(), new HashMap<String, String>());
		}	
	}
	
	public boolean existElasticsearch(String id, String index) {
		// Check to see if the trialId is already present in elasticsearch.
		long totalMessageCount = 0;
		// Check to see if index already has a document with this trial id.
		SearchRequest searchRequest = new SearchRequest(index);

		MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("msg.replay_id.keyword", id);

		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		searchSourceBuilder.size(0);
		searchSourceBuilder.fetchSource(null, "message");
		searchSourceBuilder.query(matchQueryBuilder);

		searchRequest.source(searchSourceBuilder);
		
		try {
			SearchResponse searchResponse; searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);
		
			TotalHits totalHits = searchResponse.getHits().getTotalHits();
			totalMessageCount = totalHits.value;
			
		} catch (IOException e) {
			logger.error(e.getMessage());
		}

		
		if (totalMessageCount > 0) {
			return true;
		} else {
			return false;
		}
	}
}
