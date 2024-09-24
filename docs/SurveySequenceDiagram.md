 ## [DRAFT]Survey Process
 This section contains a sequence diagram for:
  * Setting up the survey in the client map
  * Presenting the survey to the participant
  * the participant filling out the survey response
  * obtaining the survey response from Qualtrics
  * Formatting the response and publishing the response on the message bus

  The experimental sequence of surveys and trials is:
  1. Survey trial: Section1_intake survey, (watch training slides), Section2_training knowledge survey
  2. Hands-on training/competency trial
  3. Start the ASI agents
  4. Trial 1
  5. Section3_Mission 1 reflection survey
  6. End Trial 1
  7. (if necessary) stop ASI agent and start another one
  7. Trial 2
  8. Section4_Mission 2 reflection survey
  9. End Trial 2

 ```mermaid
sequenceDiagram
autonumber
    Player->>+ClientMap: Log into client map
    Experimenter->>+AsistControl: Define Participant id and Uniqe id
    Experimenter->>+AsistControl: start a trial
    AsistControl->>+ClientMap: send participant data for role
    Player->>+ClientMap: Click the Survey button
    ClientMap->>+SurveyFrame: Launch selected survey
    Player->>+SurveyFrame: fill out survey
    Player->>+SurveyFrame: Click Close button
    SurveyFrame->>+Qualtrics: Store response with participant id and unique id
    loop Every 10 seconds until responses found
        DataIngester->>+Qualtrics: Check for responses
    end
    DataIngester->>+DataIngester: Filter responses for all experiment participants
    DataIngester->>+DataIngester: Format survey response
    DataIngester->>+MessageBus: Publish survey response
```
## Notes
1. All of the survey responses for all of the participants in the current experiment should be published in the current trial.  This means that some survey responses will appear in multiple trials and hence in multiple .metadata files.  The purpose of this is to have each metadata file (and hence trial) a complete recording of the participant survey data up to that point.  Otherwise analysis would have to referr to other .metadata files to get previous survey repsonses for the particpants.
