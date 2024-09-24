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
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ExecutorService;

import javax.inject.Inject;
import javax.inject.Named;
import javax.inject.Singleton;
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
import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.context.annotation.Property;
import io.micronaut.core.annotation.NonNull;
import io.micronaut.http.HttpStatus;
import io.micronaut.http.MediaType;
import io.micronaut.http.exceptions.HttpStatusException;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import io.vertx.reactivex.pgclient.PgPool;
import io.vertx.reactivex.sqlclient.Row;
import io.vertx.reactivex.sqlclient.RowIterator;
import io.vertx.reactivex.sqlclient.RowSet;
import io.vertx.reactivex.sqlclient.Tuple;
import metadata.app.model.Experiment;
import metadata.app.model.MessageTrialExport;
import metadata.app.model.MessageApiResult;
import metadata.app.model.Trial;
import metadata.app.publisher.TrialCreatedPublisher;

@Singleton
public class DefaultTrialService implements TrialService {
	private static final Logger logger = LoggerFactory.getLogger(DefaultTrialService.class);
	private ObjectMapper objectMapper = new ObjectMapper();
	// final BeanContext context = BeanContext.run();
	@Inject
	private PgPool client;
	@Inject
	private RestHighLevelClient elasticsearchClient;

	@Named("io")
	@Inject
	ExecutorService executorService;

	private long currentMessageCount = 0;
	private long totalMessageCount = 0;

	private final DefaultExperimentService defaultExperimentService;
	private final TrialCreatedPublisher trialCreatedClient;

	private final String HEADER_METADATA_FILE_SUFIX = ".metadata";

	@Property(name = "asist.testbedVersion")
	private String TESTBED_VERSION;

	@Inject
	public DefaultTrialService(DefaultExperimentService defaultExperimentService,
			TrialCreatedPublisher trialCreatedClient) {
		this.defaultExperimentService = defaultExperimentService;
		this.trialCreatedClient = trialCreatedClient;

//		client = context.getBean(PgPool.class);
//		PgPoolOptions options = new PgPoolOptions().setPort(5432).setHost("localhost").setDatabase("postgres").setUser("postgres").setPassword("example").setMaxSize(5);
//		client = PgClient.pool(options);
	}

	@Override
	public Trial createTrial(Trial trial) {
		String sqlQuery = "INSERT INTO trials (trial_id, name, date, experimenter, subjects, trial_number, group_number, study_number, condition, notes, testbed_version, experiment_id_experiments) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) RETURNING (id)";
		Tuple elements = Tuple.tuple();
		elements.addUUID(UUID.fromString(trial.getTrialId()));
		elements.addString(trial.getName());
		elements.addLocalDateTime(LocalDateTime.ofInstant(Instant.parse(trial.getDate()), ZoneOffset.UTC));
		elements.addString(trial.getExperimenter());
		elements.addStringArray(trial.getSubjects().toArray(new String[0]));
		elements.addString(trial.getTrialNumber());
		elements.addString(trial.getGroupNumber());
		elements.addString(trial.getStudyNumber());
		elements.addString(trial.getCondition());
		elements.addStringArray(trial.getNotes().toArray(new String[0]));
		elements.addString(trial.getTestbedVersion());
		elements.addUUID(UUID.fromString(trial.getExperiment().getExperimentId()));
		try {
			RowSet<Row> rowSet = client.preparedQuery(sqlQuery).rxExecute(elements).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			if (rowIterator.hasNext()) {
				logger.info("1 row(s) affected.");
				Row row = rowIterator.next();
				Long _id = row.getLong("id");
				logger.info(MessageFormat.format("id returned: {0}.", _id));
				trial.setId(_id);
			}
			if (trial.getId() > 0) {
				trialCreatedClient.send(objectMapper.writeValueAsBytes(trial)).subscribe(() -> {
					// handle completion
				}, throwable -> {
					// handle error
				});
				return trial;
			} else {
				logger.error(MessageFormat.format("Trial id: {0} from database was invalid!", trial.getId()));
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
	public List<Trial> readTrials() {
		List<Trial> trials = new LinkedList<>();
		try {
			RowSet<Row> rowSet = client.preparedQuery("SELECT * from trials ORDER BY id ASC").rxExecute().blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				if (row.getUUID("experiment_id_experiments") == null) {
					logger.error(MessageFormat.format("Trial [{0}] has no experiment assigned to it!",
							row.getUUID("trial_id").toString()));
				}
				Experiment experiment = defaultExperimentService.readExperimentUUID(row.getUUID("experiment_id_experiments") == null ? null	: row.getUUID("experiment_id_experiments").toString());
				trials.add(new Trial(row.getInteger("id"), row.getUUID("trial_id").toString(), row.getString("name"),
						row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						row.getString("experimenter"), Arrays.asList(row.getStringArray("subjects")),
						row.getString("trial_number"), row.getString("group_number"), row.getString("study_number"),
						row.getString("condition"), Arrays.asList(row.getStringArray("notes")),
						row.getString("testbed_version"), experiment));
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
		return trials;
	}

	@Override
	public Trial readTrial(long id) {
		List<Trial> trials = new LinkedList<>();
		try {
			RowSet<Row> rowSet = client.preparedQuery("SELECT * FROM trials WHERE id = $1").rxExecute(Tuple.of((int) id)).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				if (row.getUUID("experiment_id_experiments") == null) {
					logger.error(MessageFormat.format("Trial [{0}] has no experiment assigned to it!", row.getUUID("trial_id").toString()));
				}
				Experiment experiment = defaultExperimentService.readExperimentUUID(row.getUUID("experiment_id_experiments") == null ? null	: row.getUUID("experiment_id_experiments").toString());
				trials.add(new Trial(row.getInteger("id"), row.getUUID("trial_id").toString(), row.getString("name"),
						row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						row.getString("experimenter"), Arrays.asList(row.getStringArray("subjects")),
						row.getString("trial_number"), row.getString("group_number"), row.getString("study_number"),
						row.getString("condition"), Arrays.asList(row.getStringArray("notes")),
						row.getString("testbed_version"), experiment));
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
		if (trials.isEmpty()) {
			logger.info(MessageFormat.format("No trial id: {0} found!", id));
			return null;
		}
		return trials.iterator().next();
	}

	@Override
	public Trial readTrialUUID(String trialId) {
		List<Trial> trials = new LinkedList<>();
		try {
			RowSet<Row> rowSet = client.preparedQuery("SELECT * FROM trials WHERE trial_id = $1").rxExecute(Tuple.of(UUID.fromString(trialId))).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				if (row.getUUID("experiment_id_experiments") == null) {
					logger.error(MessageFormat.format("Trial [{0}] has no experiment assigned to it!",
							row.getUUID("trial_id").toString()));
				}
				Experiment experiment = defaultExperimentService
						.readExperimentUUID(row.getUUID("experiment_id_experiments") == null ? null
								: row.getUUID("experiment_id_experiments").toString());
				trials.add(new Trial(row.getInteger("id"), row.getUUID("trial_id").toString(), row.getString("name"),
						row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						row.getString("experimenter"), Arrays.asList(row.getStringArray("subjects")),
						row.getString("trial_number"), row.getString("group_number"), row.getString("study_number"),
						row.getString("condition"), Arrays.asList(row.getStringArray("notes")),
						row.getString("testbed_version"), experiment));
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
		if (trials.isEmpty()) {
			logger.info(MessageFormat.format("No trial uuid: {0} found!", trialId));
			return null;
		}
		return trials.iterator().next();
	}

	@Override
	public Trial updateTrial(Trial trial) {
		String sqlQuery = "UPDATE trials SET trial_id = $1, name = $2, date = $3, experimenter = $4, subjects = $5, trial_number = $6, group_number = $7, study_number = $8, condition = $9, notes = $10, testbed_version = $11, experiment_id_experiments = $12 WHERE id = $13 RETURNING (id)";
		Tuple elements = Tuple.tuple();
		elements.addUUID(UUID.fromString(trial.getTrialId()));
		elements.addString(trial.getName());
		elements.addLocalDateTime(LocalDateTime.ofInstant(Instant.parse(trial.getDate()), ZoneOffset.UTC));
		elements.addString(trial.getExperimenter());
		elements.addStringArray(trial.getSubjects().toArray(new String[0]));
		elements.addString(trial.getTrialNumber());
		elements.addString(trial.getGroupNumber());
		elements.addString(trial.getStudyNumber());
		elements.addString(trial.getCondition());
		elements.addStringArray(trial.getNotes().toArray(new String[0]));
		elements.addString(trial.getTestbedVersion());
		elements.addUUID(UUID.fromString(trial.getExperiment().getExperimentId()));
		elements.addInteger((int) trial.getId());
		try {
			RowSet<Row> rowSet = client.preparedQuery(sqlQuery).rxExecute(elements).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			if (rowIterator.hasNext()) {
				logger.info("1 row(s) affected.");
				Row row = rowIterator.next();
				Long _id = row.getLong("id");
				logger.info(MessageFormat.format("id returned: {0}.", _id));
				if (trial.getId() == _id) {
					return trial;
				} else {
					logger.error(MessageFormat.format("id returned: {0} does not match trial id.", trial.getId()));
					return null;
				}
			} else {
				logger.info("No trials found!");
				return null;
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
	}

	@Override
	public boolean deleteTrial(long id) {
		try {
			RowSet<Row> rowSet = client.preparedQuery("DELETE FROM trials WHERE id = $1").rxExecute(Tuple.of((int) id))
					.blockingGet();
			if (rowSet.rowCount() > 0) {
				logger.info(MessageFormat.format("{0} row(s) affected.", rowSet.rowCount()));
				return true;
			} else {
				logger.error(MessageFormat.format("Trial with id: {0} was not deleted!", id));
				return false;
			}

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return false;
		}
	}

	@Override
	@NonNull
	public SystemFile exportFile(@NonNull @NotNull String trialId, @NonNull @NotNull String index) {
		logger.info(MessageFormat.format("Exporting temporary file using trial [{0}] from index {1}.", trialId, index));
		try {
			Trial trial = this.readTrialUUID(trialId);
			if (trial == null) {
				logger.error(MessageFormat.format("Export aborted! No trial found with id: [{0}].", trialId));
				return null;
			}
			String HEADER_METADATA_FILE_PREFIX = MessageFormat.format(
					"TrialMessages_CondBtwn-{0}_CondWin-{1}-StaticMap_Trial-{2}_Team-na_Member-{3}_Vers-{4}",
					trial.getCondition(), trial.getExperiment().getMission(), trial.getTrialNumber(),
					String.join("-", trial.getSubjects()), trial.getTestbedVersion());
			String HEADER_METADATA_FILENAME = HEADER_METADATA_FILE_PREFIX + HEADER_METADATA_FILE_SUFIX;
			File file = File.createTempFile(HEADER_METADATA_FILE_PREFIX, HEADER_METADATA_FILE_SUFIX);
			logger.info(MessageFormat.format("File name: {0}.", HEADER_METADATA_FILENAME));
			PrintWriter printWriter = new PrintWriter(new FileWriter(file));

			// Add metadata json file header.
			MessageTrialExport messageTrialExport = MessageTrialExport.generate(trial, index);
			printWriter.println(objectMapper.writeValueAsString(messageTrialExport));

			final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(30L));
			SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

			BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();

			boolQueryBuilder.must(QueryBuilders.matchQuery("msg.trial_id.keyword", trialId));
			boolQueryBuilder.mustNot(QueryBuilders.existsQuery("msg.replay_id"));

			SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
			searchSourceBuilder.size(1000);
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

	@Override
	@NonNull
	public StreamedFile exportStreamed(@NonNull @NotNull String trialId, @NonNull @NotNull String index) {
		logger.info(MessageFormat.format("Exporting streamed file using trial [{0}] from index {1}.", trialId, index));
		PipedInputStream pipedInputStream = new PipedInputStream();
		PipedOutputStream pipedOutputStream = new PipedOutputStream();
		Trial trial = this.readTrialUUID(trialId);
		if (trial == null) {
			logger.error(MessageFormat.format("Export aborted! No trial found with id: [{0}].", trialId));
			return null; 
		}
		String HEADER_METADATA_FILE_PREFIX = MessageFormat.format(
				"TrialMessages_CondBtwn-{0}_CondWin-{1}-StaticMap_Trial-{2}_Team-na_Member-{3}_Vers-{4}",
				trial.getCondition(), trial.getExperiment().getMission(), trial.getTrialNumber(),
				String.join("-", trial.getSubjects()), trial.getTestbedVersion());
		String HEADER_METADATA_FILENAME = HEADER_METADATA_FILE_PREFIX + HEADER_METADATA_FILE_SUFIX;
		logger.info(MessageFormat.format("File name: {0}.", HEADER_METADATA_FILENAME));
		executorService.execute(() -> {
			try {
				pipedOutputStream.connect(pipedInputStream);

				PrintWriter printWriter = new PrintWriter(pipedOutputStream);

				// Add metadata json file header.
				MessageTrialExport messageTrialExport = MessageTrialExport.generate(trial, index);
				printWriter.println(objectMapper.writeValueAsString(messageTrialExport));

				final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(30L));
				SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

				BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();

				boolQueryBuilder.must(QueryBuilders.matchQuery("msg.trial_id.keyword", trialId));
				boolQueryBuilder.mustNot(QueryBuilders.existsQuery("msg.replay_id"));

				SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
				searchSourceBuilder.size(1000);
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

	@Override
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
					MessageTrialExport messageTrialExport = objectMapper.readValue(json, MessageTrialExport.class);
					
					// Check to see if the trialId is already present in elasticsearch.
					String trialId = messageTrialExport.getMsg().getTrialId();
					// Check to see if index already has a document with this trial id.
					SearchRequest searchRequest = new SearchRequest(index);

					MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("msg.trial_id.keyword", trialId);

					SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
					searchSourceBuilder.size(0);
					searchSourceBuilder.fetchSource(null, "message");
					searchSourceBuilder.query(matchQueryBuilder);

					searchRequest.source(searchSourceBuilder);

					SearchResponse searchResponse = elasticsearchClient.search(searchRequest, RequestOptions.DEFAULT);

					TotalHits totalHits = searchResponse.getHits().getTotalHits();
					totalMessageCount = totalHits.value;
					
					if (totalMessageCount > 0) {
						return new MessageApiResult("failure", MessageFormat.format("Imported aborted! Trial: [{0}] already exists in index: [{1}]", trialId, index), new HashMap<String, String>());
					}
					
					// Create experiment
					Experiment experiment = new Experiment(
						-1,
						messageTrialExport.getMsg().getExperimentId(),
						messageTrialExport.getData().getMetadata().getTrial().getExperimentName(),
						messageTrialExport.getData().getMetadata().getTrial().getExperimentDate(),
						messageTrialExport.getData().getMetadata().getTrial().getExperimentAuthor(),
						messageTrialExport.getData().getMetadata().getTrial().getExperimentMission()
						);
					logger.info(MessageFormat.format("Creating experiment [{0}] found in header.", messageTrialExport.getMsg().getExperimentId()));
					defaultExperimentService.createExperiment(experiment);					
					// Create trial
					logger.info(MessageFormat.format("Creating trial [{0}] found in header.", messageTrialExport.getMsg().getTrialId()));
					createTrial(new Trial(
							-1,
							messageTrialExport.getMsg().getTrialId(),
							messageTrialExport.getData().getMetadata().getTrial().getName(),
							messageTrialExport.getData().getMetadata().getTrial().getDate(),
							messageTrialExport.getData().getMetadata().getTrial().getExperimenter(),
							messageTrialExport.getData().getMetadata().getTrial().getSubjects(),
							messageTrialExport.getData().getMetadata().getTrial().getTrialNumber(),
							messageTrialExport.getData().getMetadata().getTrial().getGroupNumber(),
							messageTrialExport.getData().getMetadata().getTrial().getStudyNumber(),
							messageTrialExport.getData().getMetadata().getTrial().getCondition(),
							messageTrialExport.getData().getMetadata().getTrial().getNotes(),
							messageTrialExport.getData().getMetadata().getTrial().getTestbedVersion(),
							experiment
							));
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

		MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("msg.trial_id.keyword", id);

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
