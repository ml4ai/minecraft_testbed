export interface FirstLook {
  message_type: string;
  sub_type: string;
  comparison: {
    operator: string;
    value: number;
  };
}
