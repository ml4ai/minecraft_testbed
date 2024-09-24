# Msg type Comment Message Format
This Comment subtype is used to communicate. 

## TOPIC

Agent/Commentator

## Message Fields

| Field Name | Type | Description
| --- | --- | --- |
| header | object | From Common_Header Format section
| msg | object | From Common_Message Format section
| data.playername | string | the player the comment is directed to
| data.role | string | the current role of the player which initiated the comment
| data.comment | string | a comment about the newly chosen role


## Message Example(s)

```json
{
  "header": {
    "timestamp": "2021-03-16T22:14:53.393Z", 
    "version": "1.1", 
    "message_type": "comment"
  }, 
  "msg": {
    "sub_type": "snarky_remark", 
    "timestamp": "2021-03-16T22:14:53.393Z", 
    "experiment_id": "a0d638c4-0411-46b1-b88a-66992f14d64b", 
    "trial_id": "9c78662f-0bd4-4269-b402-fa1e8bc6c36a", 
    "version": "1.0", 
    "source": "My_Complex_Agent"
  }, 
  "data": {
    "playername": "IHMC2", 
    "role": "Medical_Specialist", 
    "comment": "Great Choice! Medical_Specialist is the best role to choose!!"
  }
}
```

## CHANGE HISTORY

VERSION | DATE | DETAILS

1.0 | 3/6/2021 | Initial version 


