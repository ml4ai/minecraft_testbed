package metadata.app.service;

import java.text.MessageFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.LinkedList;
import java.util.List;
import java.util.UUID;

import javax.inject.Inject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import io.micronaut.context.annotation.Context;
import io.vertx.reactivex.pgclient.PgPool;
import io.vertx.reactivex.sqlclient.Row;
import io.vertx.reactivex.sqlclient.RowIterator;
import io.vertx.reactivex.sqlclient.RowSet;
import io.vertx.reactivex.sqlclient.Tuple;
import metadata.app.model.Experiment;
import metadata.app.publisher.ExperimentCreatedPublisher;

@Context
public class DefaultExperimentService implements ExperimentService {
	private static final Logger logger = LoggerFactory.getLogger(DefaultExperimentService.class);
	private ObjectMapper objectMapper = new ObjectMapper();
//	final BeanContext context = BeanContext.run();
	@Inject
	private PgPool client;

	private final ExperimentCreatedPublisher experimentCreatedClient;
	
	@Inject
	public DefaultExperimentService(ExperimentCreatedPublisher experimentCreatedClient) {
		this.experimentCreatedClient = experimentCreatedClient;
//		client = context.getBean(PgPool.class);
//		PgPoolOptions options = new PgPoolOptions().setPort(5432).setHost("localhost").setDatabase("postgres").setUser("postgres").setPassword("example").setMaxSize(5);
//		client = PgClient.pool(options);
	}

	@Override
	public Experiment createExperiment(Experiment experiment) {
		String sqlQuery = "INSERT INTO experiments (experiment_id, name, date, author, mission) VALUES ($1, $2, $3, $4, $5) RETURNING (id)";
		Tuple elements = Tuple.tuple();
		elements.addUUID(UUID.fromString(experiment.getExperimentId()));
		elements.addString(experiment.getName());
		elements.addLocalDateTime(LocalDateTime.ofInstant(Instant.parse(experiment.getDate()), ZoneOffset.UTC));
		elements.addString(experiment.getAuthor());
		elements.addString(experiment.getMission());
		try {
			RowSet<Row> rowSet = client.preparedQuery(sqlQuery).rxExecute(elements).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			if (rowIterator.hasNext()) {
				logger.info("1 row(s) affected.");
				Row row = rowIterator.next();
				Long _id = row.getLong("id");
				logger.info(MessageFormat.format("id returned: {0}.", _id));
				experiment.setId(_id);
			}
			if (experiment.getId() > 0) {
				experimentCreatedClient.send(objectMapper.writeValueAsBytes(experiment)).subscribe(() -> {
	    	        // handle completion
	    	    }, throwable -> {
	    	        // handle error
	    	    });
				return experiment;
			} else {
				logger.error(MessageFormat.format("Experiment id: {0} from database was invalid!", experiment.getId()));
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
	public List<Experiment> readExperiments() {
		List<Experiment> experiments = new LinkedList<>();
		try {
			RowSet<Row> rowSet = client.preparedQuery("SELECT * from experiments ORDER BY id ASC").rxExecute().blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				experiments.add(new Experiment(row.getLong("id"), row.getUUID("experiment_id").toString(),
						row.getString("name"), row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						row.getString("author"), row.getString("mission")));
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		} 
		return experiments;
	}

	@Override
	public Experiment readExperiment(long id) {
		List<Experiment> experiments = new LinkedList<>();
		try {
			RowSet<Row> rowSet = client.preparedQuery("SELECT * FROM experiments WHERE id = $1").rxExecute(Tuple.of((int) id)).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				experiments.add(new Experiment(row.getLong("id"), row.getUUID("experiment_id").toString(),
						row.getString("name"), row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						row.getString("author"), row.getString("mission")));
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		}
		if (experiments.isEmpty()) {
			logger.info(MessageFormat.format("No experiment id: {0} found!", id));
			return null;
		}
		return experiments.iterator().next();
	}

	@Override
	public Experiment readExperimentUUID(String experimentId) {
		List<Experiment> experiments = new LinkedList<>();
		try {
			RowSet<Row> rowSet = client.preparedQuery("SELECT * FROM experiments WHERE experiment_id = $1").rxExecute(Tuple.of(UUID.fromString(experimentId))).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();		
			while (rowIterator.hasNext()) {
				Row row = rowIterator.next();
				experiments.add(new Experiment(row.getLong("id"), row.getUUID("experiment_id").toString(),
						row.getString("name"), row.getLocalDateTime("date").toInstant(ZoneOffset.UTC).toString(),
						row.getString("author"), row.getString("mission")));
			}
		} catch (NullPointerException e) {
			logger.error(MessageFormat.format("NullPointerException: experimentId [{0}]!", experimentId));
			return null;
		}  catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		} 
		if (experiments.isEmpty()) {
			logger.info(MessageFormat.format("No experiment uuid: {0} found!", experimentId));
			return null;
		}
		return experiments.iterator().next();
	}

	@Override
	public Experiment updateExperiment(Experiment experiment) {
		String sqlQuery = "UPDATE experiments SET experiment_id = $1, name = $2, date = $3, author = $4, mission = $5 WHERE id = $6 RETURNING (id)";
		Tuple elements = Tuple.tuple();
		elements.addUUID(UUID.fromString(experiment.getExperimentId()));
		elements.addString(experiment.getName());
		elements.addLocalDateTime(LocalDateTime.ofInstant(Instant.parse(experiment.getDate()), ZoneOffset.UTC));
		elements.addString(experiment.getAuthor());
		elements.addString(experiment.getMission());
		elements.addLong(experiment.getId());
		try {
			RowSet<Row> rowSet = client.preparedQuery(sqlQuery).rxExecute(elements).blockingGet();
			RowIterator<Row> rowIterator = rowSet.iterator();
			if (rowIterator.hasNext()) {
				logger.info("1 row(s) affected.");
				Row row = rowIterator.next();
				Long _id = row.getLong("id");
				logger.info(MessageFormat.format("id returned: {0}.", _id));
				if (experiment.getId() == _id) {
					return experiment;
				} else {
					logger.error(MessageFormat.format("id returned: {0} does not match experiment id.", experiment.getId()));
					return null;
				}
			} else {
				logger.info("No experiments found!");
				return null;
			}
		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return null;
		} 
	}

	@Override
	public boolean deleteExperiment(long id) {
		try {
			RowSet<Row> rowSet = client.preparedQuery("DELETE FROM experiments WHERE id = $1").rxExecute(Tuple.of((int) id)).blockingGet();
			if (rowSet.rowCount() > 0) {
				logger.info(MessageFormat.format("{0} row(s) affected.", rowSet.rowCount()));
				return true;
			} else {
				logger.error(MessageFormat.format("Experiment with id: {0} was not deleted!", id));
				return false;
			}

		} catch (RuntimeException e) {
			logger.error(e.getMessage());
			return false;
		}
//		client.preparedQuery("DELETE FROM experiments WHERE id = $1").execute(Tuple.of((int) id), ar -> {
//			if (ar.succeeded()) {
//				RowSet<Row> rows = ar.result();
//				logger.info(rows.rowCount() + " row(s) affected.");
//			} else {
//				logger.error(ar.cause().getMessage());
//			}
//		});
//		return true;
	}
}
