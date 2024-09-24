package metadata.app.service;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;
import java.io.PrintWriter;
import java.text.MessageFormat;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;

import javax.inject.Inject;
import javax.inject.Named;
import javax.inject.Singleton;
import org.apache.lucene.search.TotalHits;
import org.elasticsearch.action.search.ClearScrollRequest;
import org.elasticsearch.action.search.ClearScrollResponse;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchScrollRequest;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.index.query.RangeQueryBuilder;
import org.elasticsearch.search.Scroll;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.sort.SortOrder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.core.annotation.NonNull;
import io.micronaut.http.HttpStatus;
import io.micronaut.http.MediaType;
import io.micronaut.http.exceptions.HttpStatusException;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import io.vertx.reactivex.pgclient.PgPool;

@Singleton
public class DefaultTimeWindowService implements TimeWindowService {
	private static final Logger logger = LoggerFactory.getLogger(DefaultTimeWindowService.class);
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

	private final String HEADER_METADATA_FILE_SUFIX = ".metadata";

	@Inject
	public DefaultTimeWindowService() {
	}

	@Override
	@NonNull
	public SystemFile exportFile(String beginDateTime, String endDateTime, String index) {
		logger.info(MessageFormat.format("Exporting temporary file using export [{0}, {1}] from index {2}.", beginDateTime, endDateTime, index));
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM-DD-YYYY_HH-mm-ss");
		try {
			LocalDateTime localDateTimeBegin = LocalDateTime.ofInstant(Instant.parse(beginDateTime), ZoneOffset.UTC);
			LocalDateTime localDateTimeEnd = LocalDateTime.ofInstant(Instant.parse(endDateTime), ZoneOffset.UTC);

			String HEADER_METADATA_FILE_PREFIX = MessageFormat.format(
					"Begin {0} End-{1} Index-{2}",
					localDateTimeBegin.format(formatter), localDateTimeEnd.format(formatter), index);
			
			String HEADER_METADATA_FILENAME = HEADER_METADATA_FILE_PREFIX + HEADER_METADATA_FILE_SUFIX;
			
			File file = File.createTempFile(HEADER_METADATA_FILE_PREFIX, HEADER_METADATA_FILE_SUFIX);
			logger.info(MessageFormat.format("File name: {0}.", HEADER_METADATA_FILENAME));
			PrintWriter printWriter = new PrintWriter(new FileWriter(file));
		
			final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(30L));
			SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

			RangeQueryBuilder rangeQueryBuilder = QueryBuilders.rangeQuery("msg.timestamp");
			
			rangeQueryBuilder.gte(localDateTimeBegin.toString());
			rangeQueryBuilder.lte(localDateTimeEnd.toString());

			SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
			searchSourceBuilder.size(1000);
			searchSourceBuilder.fetchSource(null, "message");
			searchSourceBuilder.sort("@timestamp", SortOrder.ASC);
			searchSourceBuilder.query(rangeQueryBuilder);

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
	public StreamedFile exportStreamed(String beginDateTime, String endDateTime, String index) {
		logger.info(MessageFormat.format("Exporting temporary file using export [{0}, {1}] from index {2}.", beginDateTime, endDateTime, index));
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM-DD-YYYY_HH-mm-ss");
		PipedInputStream pipedInputStream = new PipedInputStream();
		PipedOutputStream pipedOutputStream = new PipedOutputStream();
		
		LocalDateTime localDateTimeBegin = LocalDateTime.ofInstant(Instant.parse(beginDateTime), ZoneOffset.UTC);
		LocalDateTime localDateTimeEnd = LocalDateTime.ofInstant(Instant.parse(endDateTime), ZoneOffset.UTC);

		String HEADER_METADATA_FILE_PREFIX = MessageFormat.format(
				"Begin {0} End-{1} Index-{2}",
				localDateTimeBegin.format(formatter), localDateTimeEnd.format(formatter), index);
		
		String HEADER_METADATA_FILENAME = HEADER_METADATA_FILE_PREFIX + HEADER_METADATA_FILE_SUFIX;
		
		logger.info(MessageFormat.format("File name: {0}.", HEADER_METADATA_FILENAME));
		executorService.execute(() -> {
			try {
				pipedOutputStream.connect(pipedInputStream);

				PrintWriter printWriter = new PrintWriter(pipedOutputStream);

				final Scroll scroll = new Scroll(TimeValue.timeValueMinutes(30L));
				SearchRequest searchRequest = new SearchRequest(index).scroll(scroll);

				RangeQueryBuilder rangeQueryBuilder = QueryBuilders.rangeQuery("msg.timestamp");
				
				rangeQueryBuilder.gte(localDateTimeBegin.toString());
				rangeQueryBuilder.lte(localDateTimeEnd.toString());

				SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
				searchSourceBuilder.size(1000);
				searchSourceBuilder.fetchSource(null, "message");
				searchSourceBuilder.sort("@timestamp", SortOrder.ASC);
				searchSourceBuilder.query(rangeQueryBuilder);

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

}
