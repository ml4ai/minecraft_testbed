package metadata.app.controller;

import java.io.IOException;
import java.util.List;

import javax.inject.Inject;

import com.github.dockerjava.api.command.InspectContainerResponse;
import com.github.dockerjava.api.model.Container;
import com.github.dockerjava.api.model.Statistics;

import io.micronaut.http.HttpResponse;
import io.micronaut.http.MediaType;
import io.micronaut.http.MutableHttpResponse;
import io.micronaut.http.annotation.Consumes;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Produces;
import io.micronaut.http.annotation.Put;
import io.micronaut.http.annotation.QueryValue;
import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;
import metadata.app.model.Experiment;
import metadata.app.service.DefaultDockerService;
import metadata.app.service.DefaultTimeWindowService;

@Controller("/docker")
public class DockerController {
	
    private final DefaultDockerService crudService;
       
    @Inject
    public DockerController(DefaultDockerService crudService) {
        this.crudService = crudService;
    }
    
    @Get(value = "/ping")
    @Produces(MediaType.APPLICATION_JSON)
    public Boolean ping() {
        return crudService.ping();
    }
    
    @Get(value = "/containers/ls")
    @Produces(MediaType.APPLICATION_JSON)
    public List<Container> containerList() {
        return crudService.containerList();
    }
    
    @Get("/containers/{id}/log")
    @Produces(MediaType.APPLICATION_JSON)
    public List<String> containerLog(String id) {
        return crudService.containerLog(id);
    }
    
    @Get("/containers/{id}/log/download")
    @Produces(MediaType.APPLICATION_JSON)
    public SystemFile containerLogDownload(String id) {
        return crudService.containerLogDownload(id);
    }
    
    @Get("/containers/log/download")
    @Produces(MediaType.APPLICATION_OCTET_STREAM)
    public StreamedFile containerLogsDownload() {
        return crudService.containerLogsDownload();
    }
    
    @Put("/containers/{id}/start")
    @Produces(MediaType.APPLICATION_JSON)
    public Container containerStart(String id) {
    	return crudService.containerStart(id);
    }
    
    @Put("/containers/{id}/stop")
    public Container containerStop(String id) {
    	return crudService.containerStop(id);
    }
    
    @Get(value = "/containers/{id}/stats")
    @Produces(MediaType.APPLICATION_JSON)
    public List<Statistics> containerStats(String id) {
        return crudService.containerStats(id);
    }
}