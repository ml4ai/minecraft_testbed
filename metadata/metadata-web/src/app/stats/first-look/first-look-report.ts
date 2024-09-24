import { Trial } from '../../trial/trial';
import { FirstLookResultSummary } from './first-look-result-summary';

export interface FirstLookReport {
  'trial': Trial;
  'is_replay': boolean;
  'id': string;
  'index': string;
  'total_documents': number;
  'results': FirstLookResultSummary[];
}
