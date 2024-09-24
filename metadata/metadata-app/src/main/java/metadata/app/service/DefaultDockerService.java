package metadata.app.service;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.file.Paths;
import java.text.MessageFormat;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import javax.annotation.PostConstruct;
import javax.inject.Inject;
import javax.validation.constraints.NotNull;

import org.apache.lucene.search.TotalHits;
import org.elasticsearch.action.search.ClearScrollRequest;
import org.elasticsearch.action.search.ClearScrollResponse;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchScrollRequest;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.index.query.MatchQueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.Scroll;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.sort.SortOrder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.dockerjava.api.DockerClient;
import com.github.dockerjava.api.async.ResultCallback;
import com.github.dockerjava.api.async.ResultCallbackTemplate;
import com.github.dockerjava.api.command.InspectContainerResponse;
import com.github.dockerjava.api.command.LogContainerCmd;
import com.github.dockerjava.api.command.PingCmd;
import com.github.dockerjava.api.command.StatsCmd;
import com.github.dockerjava.api.command.SyncDockerCmd;
import com.github.dockerjava.api.exception.DockerException;
import com.github.dockerjava.api.model.Container;
import com.github.dockerjava.api.model.Frame;
import com.github.dockerjava.api.model.Statistics;
import com.github.dockerjava.core.DefaultDockerClientConfig;
import com.github.dockerjava.core.DockerClientConfig;
import com.github.dockerjava.core.DockerClientImpl;
import com.github.dockerjava.core.InvocationBuilder.AsyncResultCallback;
import com.github.dockerjava.core.command.LogContainerResultCallback;
import com.github.dockerjava.httpclient5.ApacheDockerHttpClient;
import com.github.dockerjava.transport.DockerHttpClient;

import io.micronaut.context.annotation.Context;
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
import metadata.app.model.MessageReplayExport;
import metadata.app.model.Replay;
import metadata.app.model.Trial;
import metadata.app.publisher.ExperimentCreatedPublisher;

@Context
public class DefaultDockerService implements DockerService {
	private static final Logger logger = LoggerFactory.getLogger(DefaultDockerService.class);
	private ObjectMapper objectMapper = new ObjectMapper();

	// private final ExperimentCreatedPublisher experimentCreatedClient;
	@Property(name = "docker.dockerHost")
	private String DOCKER_HOST;
	@Property(name = "docker.dockerTlsVerify")
	private String DOCKER_TLS_VERIFY;

	private DockerClient dockerClient;
	
    private static String OS = System.getProperty("os.name").toLowerCase();
    public static boolean IS_WINDOWS = (OS.indexOf("win") >= 0);
    public static boolean IS_MAC = (OS.indexOf("mac") >= 0);
    public static boolean IS_UNIX = (OS.indexOf("nix") >= 0 || OS.indexOf("nux") >= 0 || OS.indexOf("aix") > 0);
    public static boolean IS_SOLARIS = (OS.indexOf("sunos") >= 0);

	@Inject
	public DefaultDockerService(/* ExperimentCreatedPublisher experimentCreatedClient */) {
//		this.experimentCreatedClient = experimentCreatedClient;

	}

	@PostConstruct
	public void init() {
		DockerClientConfig config = DefaultDockerClientConfig.createDefaultConfigBuilder().withDockerHost(DOCKER_HOST)
				.withDockerTlsVerify(DOCKER_TLS_VERIFY).build();

		DockerHttpClient httpClient = new ApacheDockerHttpClient.Builder().dockerHost(config.getDockerHost())
				.sslConfig(config.getSSLConfig()).build();

		dockerClient = DockerClientImpl.getInstance(config, httpClient);
	}

	@Override
	public List<Container> containerList() {
		List<Container> containers = dockerClient.listContainersCmd().withShowAll(true).exec();
		Collections.sort(containers, new ContainerSort());
		return containers;
	}

	@Override
	public Boolean ping() {
		try {
			dockerClient.pingCmd().exec();
//			getNextStatistics();
		} catch (DockerException e) {
			logger.error(e.getMessage());
			return false;
		}

		return true;
	}

	@Override
	public List<String> containerLog(@NonNull String containerId) {
		final List<String> logs = new ArrayList<String>();

		LogContainerCmd logContainerCmd = dockerClient.logContainerCmd(containerId);
		logContainerCmd.withStdErr(true).withStdOut(true);
		// logContainerCmd.withSince(lastLogTime); // UNIX timestamp (integer) to filter
		// logs. Specifying a timestamp will only output log-entries since that
		// timestamp.
		logContainerCmd.withTail(100); // get only the last 100 log entries

//		logContainerCmd.withTimestamps(true);

		try {
			logContainerCmd.exec(new ResultCallback.Adapter<Frame>() {
				@Override
				public void onNext(Frame item) {
					logs.add(item.toString());
				}
			}).awaitCompletion();
		} catch (InterruptedException e) {
			logger.error("Interrupted Exception!" + e.getMessage());
		}

		// lastLogTime = (int) (System.currentTimeMillis() / 1000) + 5; // assumes at
		// least a 5 second wait between calls to getDockerLogs

		return logs;
	}

	@Override
	public Container containerStart(@NonNull String containerId) {
		dockerClient.startContainerCmd(containerId).exec();
		try {
			return dockerClient.listContainersCmd().withShowAll(true)
					.withIdFilter(Collections.singletonList(containerId)).exec().get(0);
		} catch (IndexOutOfBoundsException e) {
			logger.error(e.getMessage());
			return null;
		}
	}

	@Override
	public Container containerStop(@NonNull String containerId) {
		dockerClient.stopContainerCmd(containerId).withTimeout(2).exec();
		try {
			return dockerClient.listContainersCmd().withShowAll(true)
					.withIdFilter(Collections.singletonList(containerId)).exec().get(0);
		} catch (IndexOutOfBoundsException e) {
			logger.error(e.getMessage());
			return null;
		}
	}

//	@Override
//	public List<Container> containerRestart(@NonNull List<String> containerIds) {
//		containerIds.forEach(containerId -> {
//			dockerClient.restartContainerCmd(containerId).withTimeout(2).exec();
//		});
//		try {
//			return dockerClient.listContainersCmd().withShowAll(true).withIdFilter(containerIds).exec();
//		} catch (IndexOutOfBoundsException e) {
//			logger.error(e.getMessage());
//			return new ArrayList<Container>();
//		}
//	}

	@Override
	@NonNull
	public SystemFile containerLogDownload(@NonNull String containerId) {
		try {
			final List<String> logs = new ArrayList<String>();

			String FILE_PREFIX = containerId;
			String FILE_SUFIX = ".txt";
			String FILENAME = FILE_PREFIX + FILE_SUFIX;
			File file = File.createTempFile(FILE_PREFIX, FILE_SUFIX);
			PrintWriter printWriter = new PrintWriter(new FileWriter(file));

			LogContainerCmd logContainerCmd = dockerClient.logContainerCmd(containerId);
			logContainerCmd.withStdErr(true).withStdOut(true);
			logContainerCmd.withTailAll();

//			logContainerCmd.withTimestamps(true);
			logContainerCmd.exec(new ResultCallback.Adapter<Frame>() {
				@Override
				public void onNext(Frame item) {
					logs.add(item.toString());
				}
			}).awaitCompletion();

			logs.forEach(line -> {
				printWriter.println(line);
			});

			printWriter.close();

			return new SystemFile(file).attach(FILENAME);
		} catch (IOException e) {
			logger.error(e.getMessage());
		} catch (InterruptedException e) {
			logger.error("Interrupted Exception!" + e.getMessage());
		}
		throw new HttpStatusException(HttpStatus.SERVICE_UNAVAILABLE, "error downloading log");
	}

	@Override
	@NonNull
	public StreamedFile containerLogsDownload() {
		try {
			String ZIP_FILENAME = "dockerlogs.zip";
			ByteArrayOutputStream baos = new ByteArrayOutputStream();
			ZipOutputStream zipOut = new ZipOutputStream(baos);

			List<Container> containers = dockerClient.listContainersCmd().withShowAll(true).exec();
			Collections.sort(containers, new ContainerSort());
			containers.forEach(container -> {
				String containerId = container.getId();
				String FILE_PREFIX = containerId;
				String FILE_SUFIX = ".txt";
				String FILENAME = FILE_PREFIX + FILE_SUFIX;
				try {
					File file = File.createTempFile(FILE_PREFIX, FILE_SUFIX);
					PrintWriter printWriter = new PrintWriter(new FileWriter(file));

					LogContainerCmd logContainerCmd = dockerClient.logContainerCmd(containerId);
					logContainerCmd.withStdErr(true).withStdOut(true);
					logContainerCmd.withTailAll();

					// logContainerCmd.withTimestamps(true);

					logContainerCmd.exec(new ResultCallback.Adapter<Frame>() {
						@Override
						public void onNext(Frame item) {
							printWriter.println(item.toString());
						}
					}).awaitCompletion();

					printWriter.close();

					FileInputStream fis = new FileInputStream(file);
					zipOut.putNextEntry(new ZipEntry(file.getName()));
					zipOut.write(fis.readAllBytes());
					fis.close();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

			});
			zipOut.finish();
			zipOut.close();

			InputStream inputStream = new ByteArrayInputStream(baos.toByteArray());
			baos.close();
			return new StreamedFile(inputStream, MediaType.APPLICATION_OCTET_STREAM_TYPE).attach(ZIP_FILENAME);
		} catch (IOException e) {
			logger.error(e.getMessage());
		}
		throw new HttpStatusException(HttpStatus.SERVICE_UNAVAILABLE, "error downloading log");
	}

	@Override
	public List<Statistics> containerStats(@NonNull String containerId) {
		final List<Statistics> statistics = new ArrayList<Statistics>();

		StatsCmd statsCmd = dockerClient.statsCmd(containerId).withNoStream(true);

		try {
			statsCmd.exec(new ResultCallback.Adapter<Statistics>() {
				@Override
				public void onNext(Statistics item) {
					statistics.add(item);
				}
			}).awaitCompletion();
		} catch (InterruptedException e) {
			logger.error("Interrupted Exception!" + e.getMessage());
		}

		return statistics;
	}
	
//	@Override
//	public List<String> agentList() {
//		List<String> agents = new ArrayList<String>();
//		String[] command = null;
//		if (DefaultDockerService.IS_WINDOWS ) {
//			command = new String[] {"cmd.exe", "/c", MessageFormat.format("cd {0} && dir /b", AGENTS_ROOT_FOLDER)};
//		} else if(DefaultDockerService.IS_UNIX ) {
//			command = new String[] {"/bin/sh","-c", MessageFormat.format("cd {0} && ls", AGENTS_ROOT_FOLDER)};
//		}
//		if(command == null) {
//			return agents;
//		}
//        ProcessBuilder pb = new ProcessBuilder(command).redirectErrorStream(true);
//        Process process = null;
//		try {
//			process = pb.start();
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//			logger.error(e.getMessage());
//			return agents;
//		}
//        StringBuilder result = new StringBuilder(80);
//        try (BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream())))
//        {
//            while (true)
//            {
//                String line = null;
//				try {
//					line = in.readLine();
//				} catch (IOException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				}
//                if (line == null)
//                    break;
//                agents.add(line);
//            }
//        } catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//			logger.error(e.getMessage());
//			return agents;
//		}
//		return agents;
//	}
//	
//	@Override
//	public List<String> dockerComposeStart(String agent) {
//		List<String> output = new ArrayList<String>();
//		String[] command = null;
//		if (DefaultDockerService.IS_WINDOWS ) {
//			command = new String[] {"cmd.exe", "/c", MessageFormat.format("cd {0}/{1} && docker-compose up", AGENTS_ROOT_FOLDER, agent)};
//		} else if(DefaultDockerService.IS_UNIX ) {
//			command = new String[] {"/bin/sh","-c", MessageFormat.format("cd {0}/{1} && docker-compose up", AGENTS_ROOT_FOLDER, agent)};
//		}
//		if(command == null) {
//			return output;
//		}
//        ProcessBuilder pb = new ProcessBuilder(command).redirectErrorStream(true);
//        Map<String, String> env = pb.environment();
//        env.put("DOCKER_TLS_VERIFY", "0");
//        Process process = null;
//		try {
//			process = pb.start();
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//			logger.error(e.getMessage());
//			return output;
//		}
//        StringBuilder result = new StringBuilder(80);
//        try (BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream())))
//        {
//            while (true)
//            {
//                String line = null;
//				try {
//					line = in.readLine();
//				} catch (IOException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				}
//                if (line == null)
//                    break;
//                output.add(line);
//                logger.info(line);
//            }
//        } catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//			logger.error(e.getMessage());
//			return output;
//		}
//		return output;
//	}
//	
//	public void runCommand() {
////		String[] command = {"cd /var/lib/metadata-app/agents", "ls -l"}; // /var/lib/metadata-app/agents
////		Paths.get(AGENTS_ROOT_FOLDER, "uaz_dialog_agent")
//		String[] command = {"/bin/sh","-c", MessageFormat.format("cd {0} && ls", AGENTS_ROOT_FOLDER)};
//        ProcessBuilder pb = new ProcessBuilder(command).redirectErrorStream(true);
//        Process process = null;
//		try {
//			process = pb.start();
//		} catch (IOException e1) {
//			// TODO Auto-generated catch block
//			e1.printStackTrace();
//		}
//        StringBuilder result = new StringBuilder(80);
//        try (BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream())))
//        {
//            while (true)
//            {
//                String line = null;
//				try {
//					line = in.readLine();
//				} catch (IOException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				}
//                if (line == null)
//                    break;
//                result.append(line).append(System.getProperty("line.separator"));
//            }
//        } catch (IOException e1) {
//			// TODO Auto-generated catch block
//			e1.printStackTrace();
//		}
//        logger.info(result.toString());
//	}
	
	private static int NUM_STATS = 1;
	
	public Statistics getNextStatistics() {
	    AsyncResultCallback<Statistics> callback = new AsyncResultCallback<Statistics>() {
	    	@Override
			public void onNext(Statistics stats) {
				logger.info(stats.toString());
			}
	    };
	    
	    dockerClient.statsCmd("139dec757518").exec(callback);
	    Statistics stats = null;
	    try {
	        stats = callback.awaitResult();
//	        callback.close();
	    } catch (RuntimeException e) {
	        // you may want to throw an exception here
	    }
	    return stats; // this may be null or invalid if the container has terminated
	}
	
    public void streamStatisticsStart() throws InterruptedException, IOException {
    	logger.info("streamStatisticsStart()");
        CountDownLatch countDownLatch = new CountDownLatch(1);

        try (StatsCallback statsCallback = dockerClient
            .statsCmd("139dec757518")
            .exec(new StatsCallback())) {
            logger.info("Stats collection started");
        }
        logger.info("Completed callection call.");
    }
	
    public void testStatsStreaming() throws InterruptedException, IOException {
    	logger.info("testStatsStreaming()");
        CountDownLatch countDownLatch = new CountDownLatch(NUM_STATS);

        boolean gotStats = false;
        try (StatsCallbackTest statsCallback = dockerClient
            .statsCmd("139dec757518")
            .exec(new StatsCallbackTest(countDownLatch))) {
        	countDownLatch.await(10, TimeUnit.SECONDS);
//            assertTrue(countDownLatch.await(10, TimeUnit.SECONDS));
            gotStats = statsCallback.gotStats();

            logger.info("Stop stats collection");
        }
        
        Thread.sleep(5000);

//        logger.info("Stopping container");
//        containerStop("139dec757518");

        logger.info("Completed test");
    }
    
    private class StatsCallback extends ResultCallbackTemplate<StatsCallback, Statistics> {
        private final CountDownLatch countDownLatch = new CountDownLatch(1);
        private ObjectMapper objectMapper = new ObjectMapper();

        public StatsCallback() {
        	try {
				countDownLatch.await(10, TimeUnit.SECONDS);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
        }

        @Override
        public void onNext(Statistics stats) {
        	try {
				logger.info("Received stats: {}", objectMapper.writeValueAsString(stats));
			} catch (JsonProcessingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
        }

        public void stop() {
            this.countDownLatch.countDown();
            try {
				this.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
        }
    }
	
    private static class StatsCallbackTest extends ResultCallbackTemplate<StatsCallbackTest, Statistics> {
        private final CountDownLatch countDownLatch;
        private ObjectMapper objectMapper = new ObjectMapper();
        private Boolean gotStats = false;

        public StatsCallbackTest(CountDownLatch countDownLatch) {
            this.countDownLatch = countDownLatch;
        }

        @Override
        public void onNext(Statistics stats) {
        	try {
				logger.info("Received stats: {}", objectMapper.writeValueAsString(stats));
			} catch (JsonProcessingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
            if (stats != null) {
                gotStats = true;
            }
            //countDownLatch.countDown();
        }

        public Boolean gotStats() {
            return gotStats;
        }
    }

	class ContainerSort implements Comparator<Container> {
		// Used for sorting in ascending order of
		// roll number
		public int compare(Container a, Container b) {
			return (int) (a.getCreated() - b.getCreated());
		}
	}
}
