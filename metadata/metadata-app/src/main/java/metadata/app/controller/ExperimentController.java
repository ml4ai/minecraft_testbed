package metadata.app.controller;

import java.util.List;

import javax.inject.Inject;

import io.micronaut.http.HttpResponse;
import io.micronaut.http.HttpStatus;
import io.micronaut.http.MediaType;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Consumes;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Delete;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.Produces;
import io.micronaut.http.annotation.Put;
import metadata.app.model.Experiment;
import metadata.app.service.DefaultExperimentService;

@Controller("/experiments")
public class ExperimentController {

    private final DefaultExperimentService crudService;

    @Inject
    public ExperimentController(DefaultExperimentService crudService) {
        this.crudService = crudService;
    }

    @Post("/")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public HttpResponse<Experiment> create(@Body Experiment experiment) {
    	Experiment createdExperiment = crudService.createExperiment(experiment);
    	if (createdExperiment == null) {
    		return HttpResponse.serverError(experiment);
    	}
    	else if (createdExperiment.getId() > 0) {
    		return HttpResponse.ok(createdExperiment);
    	} else {
    		return HttpResponse.badRequest(experiment);
    	}
    }
    
    @Get("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Experiment read(long id) {
        return crudService.readExperiment(id);
    }
    
    @Get("/uuid/{uuid}")
    @Produces(MediaType.APPLICATION_JSON)
    public Experiment readUUID(String uuid) {
        return crudService.readExperimentUUID(uuid);
    }
    
    @Get("/")
    @Produces(MediaType.APPLICATION_JSON)
    public List<Experiment> reads() {
        return crudService.readExperiments();
    }

	@Put("/{id}")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public HttpResponse<Experiment> update(@Body Experiment experiment, long id) {
    	Experiment updatedExperiment = crudService.updateExperiment(experiment);
    	if (updatedExperiment == null) {
    		return HttpResponse.serverError(experiment);
    	}
    	else if (updatedExperiment.getId() == experiment.getId()) {
    		return HttpResponse.ok(updatedExperiment);
    	} else {
    		return HttpResponse.badRequest(experiment);
    	}
    }

    @Delete("/{id}")
    public HttpResponse<Boolean> delete(long id) {
        // return crudService.deleteExperiment(id) ? HttpStatus.OK : HttpStatus.BAD_REQUEST;
    	boolean deletedExperiment = crudService.deleteExperiment(id);
    	if (deletedExperiment == false) {
    		return HttpResponse.serverError(false);
    	}
    	else {
    		return HttpResponse.ok(true);
    	}
    }
}