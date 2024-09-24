package metadata.app.controller;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.text.MessageFormat;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.inject.Inject;

import org.apache.lucene.search.TotalHits;
import org.elasticsearch.action.ActionListener;
import org.elasticsearch.action.admin.indices.delete.DeleteIndexRequest;
import org.elasticsearch.action.search.ClearScrollRequest;
import org.elasticsearch.action.search.ClearScrollResponse;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchScrollRequest;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.index.query.BoolQueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.Scroll;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.sort.SortOrder;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

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
import io.reactivex.Flowable;
import io.reactivex.Observable;
import metadata.app.model.ExportTrialBody;
import metadata.app.model.Header;
import metadata.app.model.MessageApiResult;
import metadata.app.model.Msg;
import metadata.app.model.Replay;
import metadata.app.model.ReplayMessageCountMessage;
import metadata.app.model.Trial;
import metadata.app.service.DefaultTrialService;

@Controller("/trials")
public class TrialController {
	
    private final DefaultTrialService crudService;
    private ObjectMapper objectMapper = new ObjectMapper();
    
    @Inject
	private RestHighLevelClient elasticsearchClient;
    
    @Inject
    public TrialController(DefaultTrialService crudService) {
        this.crudService = crudService;
    }
    
    @Post("/")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public HttpResponse<Trial> create(@Body Trial trial) {
    	Trial createdTrial = crudService.createTrial(trial);
    	if (createdTrial == null) {
    		return HttpResponse.serverError(trial);
    	}
    	else if (createdTrial.getId() > 0) {
    		return HttpResponse.ok(createdTrial);
    	} else {
    		return HttpResponse.badRequest(trial);
    	}
    }
    
    @Get("/{trialId}")
    @Produces(MediaType.APPLICATION_JSON)
    public Trial read(long trialId) {
        return crudService.readTrial(trialId);
    }
    
    @Get("/uuid/{uuid}")
    @Produces(MediaType.APPLICATION_JSON)
    public Trial readUUID(String uuid) {
        return crudService.readTrialUUID(uuid);
    }
    
    @Get("/")
    @Produces(MediaType.APPLICATION_JSON)
    public List<Trial> reads() {
        return crudService.readTrials();
    }

    @Put("/{trialId}")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public HttpResponse<Trial> update(@Body Trial trial, long trialId) throws JsonProcessingException {
    	Trial updatedTrial = crudService.updateTrial(trial);
    	if (updatedTrial == null) {
    		return HttpResponse.serverError(trial);
    	}
    	else if (updatedTrial.getId() == trial.getId()) {
    		return HttpResponse.ok(updatedTrial);
    	} else {
    		return HttpResponse.badRequest(trial);
    	}
    }

    @Delete("/{trialId}")
    public HttpResponse<Boolean> delete(long trialId) {
        // return crudService.deleteTrial(trialId) ? HttpStatus.OK : HttpStatus.BAD_REQUEST;
    	boolean deletedTrial = crudService.deleteTrial(trialId);
    	if (deletedTrial == false) {
    		return HttpResponse.serverError(false);
    	}
    	else {
    		return HttpResponse.ok(true);
    	}
    }
    
    @Get(value = "/export/{uuid}")
    @Consumes(MediaType.APPLICATION_JSON) 
    public MutableHttpResponse<StreamedFile> exportStreamed(String uuid, @QueryValue(value = "index") String index) throws IOException {
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
	public MutableHttpResponse<SystemFile> exportFile(String uuid, @QueryValue(value = "index") String index) throws IOException {
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
    public HttpResponse<MessageApiResult> importFile(CompletedFileUpload file, @QueryValue(value = "index") String index, @QueryValue(value = "createIndex") boolean createIndex) {
		try {
			MessageApiResult messageTrialImportResult = crudService.importFile(file.getBytes(), file.getFilename(), index, createIndex);
			return HttpResponse.ok(messageTrialImportResult);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return HttpResponse.serverError(new MessageApiResult("failure", "Error reading file!", new HashMap<String, String>()));
		}		
    }
	
	@Get("/{uuid}/exist")
	public Boolean rootId(String uuid, @QueryValue(value = "index") String index) {
		return crudService.existElasticsearch(uuid, index);
	}
}