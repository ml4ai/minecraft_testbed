export interface FirstLookResultSummary {
  'message_type': string;
  'sub_type': string;
  'comparison': {
    'operator': string;
    'value': number;
  };
  'result': boolean;
  'count': number;
}
