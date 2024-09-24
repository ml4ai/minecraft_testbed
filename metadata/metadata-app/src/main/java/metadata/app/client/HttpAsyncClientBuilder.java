package metadata.app.client;

import io.micronaut.context.annotation.Factory;
import io.micronaut.context.annotation.Replaces;

import javax.inject.Singleton;

import org.apache.http.impl.nio.client.HttpAsyncClientBuilder;

@Factory 
class HttpAsyncClientBuilderFactory {

    @Replaces(HttpAsyncClientBuilder.class)
    @Singleton
    HttpAsyncClientBuilder builder() {
        return HttpAsyncClientBuilder.create();
    }
}