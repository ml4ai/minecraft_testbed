import { Component, OnInit, Inject, ViewChild } from "@angular/core";
import { MatDialogRef } from "@angular/material/dialog";
import {
  MatSelectionList,
  MatSelectionListChange,
} from "@angular/material/list";
import {
  ExperimentDTO,
  TrialDTO,
  FetchedExperimentDTO,
  MissionDTO,
  InterventionAgentsDTO,

} from "../Interface/DTO";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { ExperimentService } from "../Services/experiment.service";
import { MatSnackBar } from "@angular/material/snack-bar";

@Component({
  selector: "app-experiment-dialog",
  templateUrl: "./experiment-dialog.component.html",
  styleUrls: ["./experiment-dialog.component.css"],
})
export class ExperimentDialogComponent implements OnInit {
  @ViewChild(MatSelectionList, { static: true }) list: MatSelectionList;
  @ViewChild("asistMissionSelect", { static: true })
  asistMissionSelect: HTMLSelectElement;
  @ViewChild("malmoMissionSelect", { static: true })
  malmoMissionSelect: HTMLSelectElement;

  baseUrl;
  current_experiment_id;
  current_trial_id;

  missionScript = "TestScript.py";
  associatedFile = " Not Set ";
  mapName = "Test";
  PIP = true;
  instanceNumber = "0";

  experimentDTO: ExperimentDTO = null;
  trialDTO: TrialDTO = null;

  experiment_name = "NOT SET";
  experiment_author = "ENTER EXPERIMENT AUTHOR";
  mission_name = "ENTER MISSION NAME";

  fetchedExperiments: FetchedExperimentDTO[];

  // MISSION SELECTOR

  showAsistMissions = true;

  //malmoMissions: MissionDTO[] = [
  //  {value: 'TestScript.py', display: 'Test'},
  //  {value: 'mdf_load_sparky.py', display: 'Sparky'},
  //  {value: 'mdf_load_falcon.py', display: 'Falcon'}
  // ];

  asistMissions: MissionDTO[] = [];
  interventionAgents: InterventionAgentsDTO[] = [];

  

  constructor(
    private http: HttpClient,
    @Inject("BASE_URL") baseUrl: string,
    public dialogRef: MatDialogRef<ExperimentDialogComponent>,
    public experimentService: ExperimentService,
    private _snackBar: MatSnackBar
  ) {
    this.baseUrl = baseUrl;
    this.experimentService = experimentService;
    this.showAsistMissions = experimentService.mod === "asist";
    this.interventionAgents = this.experimentService.intervention_agents;

    this.asistMissions = this.experimentService.mission_list;
    

    console.log("Show Asist Missions : " + this.showAsistMissions);

    this.fetchExperiments();
  }

  ngOnInit() {
    this.list.selectionChange.subscribe((s: MatSelectionListChange) => {
      this.list.deselectAll();
      s.option.selected = true;

      console.log(s.option.value);
      this.experimentService.experiment_id = s.option.value[0];
      this.experimentService.experiment_name = s.option.value[1];
      this.experimentService.experiment_author = s.option.value[2];
      this.experimentService.experiment_mission = s.option.value[3];
    });
  }

  async createExperiment() {
    this.experimentDTO = {
      data: {
        name: this.experiment_name,
        author: this.experiment_author,
        mission: this.mission_name,
      },
    };

    this.http
      .post<ExperimentDTO>(
        this.baseUrl + "api/Experiment/createExperiment",
        this.experimentDTO
      )
      .subscribe(
        (response) => {
          this.experimentDTO = response;
          console.log(this.experimentDTO);
        },
        (error) => console.log(error),
        () => {
          setTimeout(() => this.fetchExperiments(), 1000);
        }
      );
  }

  cancel() {
    this.dialogRef.close("canceled");
  }

  async createTrialAndStartMission() {
    if (
      this.experimentService.experiment_id &&
      this.experimentService.trial_name &&
      this.experimentService.trial_experimenter &&
      this.experimentService.trial_subjects &&
      this.experimentService.trial_number &&
      this.experimentService.trial_group_number &&
      this.experimentService.trial_study_number &&
      this.experimentService.trial_condition &&
      this.experimentService.trial_notes &&
      this.experimentService.experiment_name &&
      this.experimentService.experiment_author &&
      this.experimentService.trial_experiment_mission
    ) {
      // Update Client Info
      this.experimentService.clientInfo = [];
      this.experimentService.gridOptions.api.forEachNode((rowNode, index) => {
        this.experimentService.clientInfo.push(rowNode.data);
      });

      
      // 1. CREATE THE TRIAL DTO
      this.trialDTO = {
        msg: {
          experiment_id: this.experimentService.experiment_id,
        },
        data: {
          name: this.experimentService.trial_name,
          experimenter: this.experimentService.trial_experimenter,
          subjects: this.experimentService.trial_subjects.split(","),
          trial_number: this.experimentService.trial_number,
          group_number: this.experimentService.trial_group_number,
          study_number: this.experimentService.trial_study_number,
          condition: this.experimentService.trial_condition,
          notes: this.experimentService.trial_notes.split(","),
          experiment_name: this.experimentService.experiment_name,
          experiment_author: this.experimentService.experiment_author,
          experiment_mission: this.experimentService.trial_experiment_mission,
          intervention_agents: [this.experimentService.trial_intervention_agent],
          map_name: this.experimentService.missionDTO.MapName,
          map_block_filename: this.experimentService.missionDTO.MapBlockFilename,
          client_info: this.experimentService.clientInfo,          
        },
      };     
     
      console.log(this.trialDTO);

      // set AsistMod is Ready/ MinecraftContainer is up to false ( redundant accept the first time )

      this.experimentService.asistModIsReady = "False";
      this.experimentService.minecraftContainerInitialized = "False";
      this.experimentService.modLoadingProgress = 5;
      // START THE TRIAL AND RUN MISSION
      await this.startTrial().then(() => this.runMission());
      this.dialogRef.close({
        trialDTO: this.trialDTO,
        experimentDTO: this.experimentDTO,
      });
    } else {
      // tslint:disable-next-line: max-line-length
      alert(
        " Please make sure every Trial Creation field has been filled out before starting a Trial."
      );
    }
  }

  public runMission() {
    const httpOptions = {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
      }),
    };

    console.log("Starting Mission : " + this.missionScript);

    //  if ( this.experimentService.mod === 'malmo') {

    //    const missionDTO: MissionDTO = { 'missionName': this.missionScript, 'associatedFile': 'None',
    //     'instanceNumber': this.instanceNumber, 'PIP': false};

    //    this.http.put<MissionDTO>(this.baseUrl + 'api/Malmo/startMission', missionDTO, httpOptions)
    //    .subscribe((returned) => console.log(returned));

    //}
    if (this.experimentService.mod === "asist") {
      console.log(
        "MissionName : " + this.experimentService.missionDTO.MissionName
      );
      console.log("MapName : " + this.experimentService.missionDTO.MapName);
      console.log(
        "Associated Block File : " +
          this.experimentService.missionDTO.MapBlockFilename
      );
      console.log(
        "Associated Info File : " +
          this.experimentService.missionDTO.MapInfoFilename
      );

      // Update Observer Info
      this.experimentService.observerInfo = [];
      this.experimentService.obsGridOptions.api.forEachNode((rowNode, index) => {
        this.experimentService.observerInfo.push(rowNode.data);
      });
      
      const missionDTO: MissionDTO = {
        MissionName: this.experimentService.missionDTO.MissionName,
        MapName: this.experimentService.missionDTO.MapName,
        MapBlockFilename: this.experimentService.missionDTO.MapBlockFilename,
        MapInfoFilename: this.experimentService.missionDTO.MapInfoFilename,
        ObserverInfo: this.experimentService.observerInfo
      };

      this.http
        .put<MissionDTO>(
          this.baseUrl + "api/Minecraft/startMission",
          missionDTO,
          httpOptions
        )
        .subscribe((returned) => console.log(returned));
    }

    // MatSnackBar
    let snackBarRef = this._snackBar.open(
      "Running Mission : " +
      this.experimentService.missionDTO.MapName +
        ". Please wait for Minecraft Server initialization.",
      null,
      { duration: 5000 }
    );
  }

  fetchExperiments() {
    return this.http
      .get<any>(this.baseUrl + "api/Experiment/fetchExperiments")
      .subscribe((response) => {
        console.log(response);
        this.fetchedExperiments = JSON.parse(
          response.experiments
        ) as FetchedExperimentDTO[];
        console.log(this.fetchedExperiments);
      });
  }

  public assignMission(event) {
    console.log(event.target);
    // MALMO
    this.missionScript = event.target.value;
    // ASISTMOD

    const indexFromSelect = event.target.selectedIndex;

    this.experimentService.missionDTO = this.experimentService.mission_list[
      indexFromSelect
    ];

    this.experimentService.trial_experiment_mission =
      event.target.options[event.target.selectedIndex].text;

    this.experimentService.trial_experiment_missionIndex =
      event.target.selectedIndex;

    console.log(
      "MissionName : " + this.experimentService.missionDTO.MissionName
    );
    console.log("MapName : " + this.experimentService.missionDTO.MapName);
    console.log(
      "Associated Block File : " +
        this.experimentService.missionDTO.MapBlockFilename
    );
    console.log(
      "Associated Info File : " +
        this.experimentService.missionDTO.MapInfoFilename
    );
  }

 

  public setLastMission(event) {
    console.log(event);
    // TAB INDEX
    if (event.index === 2) {
      console.log(
        "Attemptin to set last mission index : " +
          this.experimentService.trial_experiment_missionIndex
      );
      if (this.showAsistMissions) {
        const asistSelect: HTMLSelectElement = document.getElementById(
          "asistSelect"
        ) as HTMLSelectElement;
        asistSelect.selectedIndex = this.experimentService.trial_experiment_missionIndex;
      } else {
        const malmoSelect: HTMLSelectElement = document.getElementById(
          "malmoSelect"
        ) as HTMLSelectElement;
        malmoSelect.selectedIndex = this.experimentService.trial_experiment_missionIndex;
      }
     
    }
  }

  public async startTrial(): Promise<any> {
    return new Promise<void>((resolve, reject) => {
      this.http
        .post<TrialDTO>(
          this.baseUrl + "api/Experiment/startTrial",
          this.trialDTO
        )
        .subscribe((response) => {
          console.log(response);
          this.trialDTO = response;
          this.experimentService.trialDTO = response;
          this.experimentService.trial_running = "True";
          this.experimentService.trial_id = response.msg.trial_id;
        });
      resolve();
    });
  }

}
