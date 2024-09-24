import { Experiment } from '../experiment/experiment';

export interface Trial {
  id: number;
  trial_id: string;
  name: string;
  date: string;
  experimenter: string;
  trial_number: string;
  group_number: string;
  study_number: string;
  condition: string;
  subjects: string[];
  notes: string[];
  testbed_version: string;
  experiment: Experiment;
}
