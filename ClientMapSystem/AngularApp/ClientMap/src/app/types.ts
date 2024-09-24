
export interface Intervention {
  start: string;
  end: string;
  type: string;
  id: number;
  status: string;
}

export interface Position {
  x:number;
  y:number;
  z:number;
}

export interface TextIntervention extends Intervention {
  text: string;
  receiver: string;
  time: string;

}
  
export interface HeatmapIntervention extends Intervention {
  topLeft : Position;
  bottomRight: Position;
}

export interface ClientInfo{
  playername : string;
  callsign : string;
  participant_id : string;
  unique_id:string;
}

export interface ClientMapConfig{
  showGlobalPositions: boolean,
  "Saturn_A_Text": {
    "Medic":string[],
    "Transporter":string[],
    "Engineer":string[]
  },
  "Saturn_B_Text": {
    "Medic":string[],
    "Transporter":string[],
    "Engineer":string[]
  },
  "Saturn_C_Text": {
    "Medic":string[],
    "Transporter":string[],
    "Engineer":string[]
  },
  "Training_Text": {
    "Medic":string[],
    "Transporter":string[],
    "Engineer":string[]
  }
}