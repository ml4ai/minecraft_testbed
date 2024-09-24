package metadata.app.service;

import io.micronaut.http.server.types.files.StreamedFile;
import io.micronaut.http.server.types.files.SystemFile;

public interface TimeWindowService {
    SystemFile exportFile(String beginDateTime, String endDateTime, String index);
    StreamedFile exportStreamed(String beginDateTime, String endDateTime, String index);
}
