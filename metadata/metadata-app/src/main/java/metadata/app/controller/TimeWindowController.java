package metadata.app.controller;

import java.io.IOException;
import javax.inject.Inject;

import io.micronaut.http.HttpResponse;
import io.micronaut.http.MediaType;
import io.micronaut.http.MutableHttpResponse;
import io.micronaut.http.annotation.Consumes;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Produces;
import io.micronaut.http.annotation.QueryValue;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import metadata.app.service.DefaultTimeWindowService;

@Controller("/timewindow")
public class TimeWindowController {
	
    private final DefaultTimeWindowService crudService;
       
    @Inject
    public TimeWindowController(DefaultTimeWindowService crudService) {
        this.crudService = crudService;
    }
    
    @Get(value = "/export")
    @Consumes(MediaType.APPLICATION_JSON) 
    public MutableHttpResponse<StreamedFile> exportStreamed(@QueryValue(value = "beginDateTime") String beginDateTime, @QueryValue(value = "endDateTime") String endDateTime, @QueryValue(value = "index") String index) throws IOException {
    	StreamedFile streamedFile = crudService.exportStreamed(beginDateTime, endDateTime, index);
    	if (streamedFile != null) {
    		return HttpResponse.ok(streamedFile);
    	} else {
    		return HttpResponse.notFound();
    	}
    }
    
	@Get(value = "/export/file")
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_OCTET_STREAM)    
	public MutableHttpResponse<SystemFile> exportFile(@QueryValue(value = "beginDateTime") String beginDateTime, @QueryValue(value = "endDateTime") String endDateTime, @QueryValue(value = "index") String index) throws IOException {
		SystemFile systemFile = (crudService.exportFile(beginDateTime, endDateTime, index));
    	if (systemFile != null) {
    		return HttpResponse.ok(systemFile);
    	} else {
    		return HttpResponse.notFound();
    	}
	}
}