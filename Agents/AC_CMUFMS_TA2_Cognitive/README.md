# CMU FMS Group Cognitive Load Agent

This agent, written in Python, computes the current cognitive load for
the overall team, as well as a related probability of forgetting by
the overall team. These are computed solely with respect to
interactions with victims, not marker blocks.

It publishes on only a coarse grained schedule, publishing a message to the bus
only when there has been an interaction that can be expected to make a substantial
change to the cognitive load, and does not continuously reflect the fine-grained
changes reflecting decay of memories over short periods of time.

## Message data format

The agent publishes one flavor of message to the bus,
on the topic `agent/measure/AC_CMUFMS_TA2_Cognitive/load`, with
message type `agent` and sub_type `Measure:cognitive_load`.

    {
      "id": "587b797e-a0f6-4a0d-8769-877b2bd36785",
      "agent": "AC_CMUFMS_TA2_Cognitive",
      "created": "2022-03-10T01:03:54.022834Z",
      "elapsed_milliseconds": 560236,
      "cognitive_load": {
        "value": 4.654498457656448,
        "confidence": 0.5052246336163365
      },
      "probability_of_forgetting": {
        "value": 0.9724250461356305,
        "confidence": 0.04152453959113148
      }
    }

Each of the `cognitive_load` and the `probability_of_forgetting` members are
sub-objects with two members, the value of those sub-members being the
value of the measure and a confidence estimate of that value. All
these values are non-negative, real numbers.

## Exception handling

Note that this agent is built using the `ihmc-python-agent-helper-package`. The
`on_message` implementation in this helper of exception handling is believed to
be sufficient to keep this agent up and running as well as can be expected should
exceptions be encountered.
