export interface Survey {

    id: string;
    name: string;
    ownerId: string;
    lastModified: Date;
    creationDate: Date;
    isActive: string;

  }

  export interface SurveyDialogData {
    id: string;
    name: string;
    unique_id: string;
    participant_id: string;
  }