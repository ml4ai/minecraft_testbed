# metadata stack
The metadata stack containers allow for experiment and trial metadata to be persisted for use in control operation.

## Prerequisites
- Docker and Docker Compose.
    * Windows users can download [Docker Desktop](https://docs.docker.com/docker-for-windows/install/).
    * Linux users can read the [install instructions](https://docs.docker.com/compose/install/#install-compose) or can install via pip:
    
            pip install docker-compose


- There are four containers and each have their own env file for configuation. The default settings should work but changes can be made as needed. The files are located in the *metadata\metadata-docker* folder:
    * **postgres**: the database container.
        * *postgres.env*
  
                POSTGRES_USER=postgres
                POSTGRES_PASSWORD=postgres
                POSTGRES_DB=metadata
                POSTGRES_HOST=host.docker.internal

                ( The above is for windows only. If you are running the ELK STACK on a separate machine, OR you are running  on LINUX or MAC, replace host.docker.internal above with the IP of the computer hosting the ELK STACK, DO NOT USE localhost )
                
                POSTGRES_PORT=5432
  
    * **pgadmin**: the database admin web gui interface.
        * *pgadmn.env*

                PGADMIN_DEFAULT_EMAIL=pgadmin4@pgadmin.org
                PGADMIN_DEFAULT_PASSWORD=admin

    * **metadata-app**: the metadata server application.
        * *metadata-app.env*

                POSTGRES_USER=postgres
                POSTGRES_PASSWORD=postgres
                POSTGRES_DB=metadata
                POSTGRES_HOST=postgres
                POSTGRES_PORT=5432

    * **metadata-msg**: the metadata mqtt client application.
        * *metadata-msg.env*

                MQTT_BROKER_URL=tcp://host.docker.internal:1883

                ( The above is for windows only. If you are running the ELK STACK on a separate machine, OR you are running  on LINUX or MAC, replace host.docker.internal above with the IP of the computer hosting the ELK STACK, DO NOT USE localhost )

                MQTT_CLIENT_ID=e8fb82c2-67aa-11ea-bc55-0242ac130003
                MQTT_TOPIC=trial,experiment
                MQTT_QOS=2,2
                MQTT_VERBOSE=true
                MQTT_CLEAN_SESSION=true
                MQTT_METADATA_API_URL=https://metadata-app:8080
  
## Starting the metadata stack

Run the following command from the *metadata\metadata-docker* folder:

```
docker-compose up --build
```

> NOTE: use the `-d` option if you want to run the metadata stack in the background. Doing this will prevent any console output from being visible.
