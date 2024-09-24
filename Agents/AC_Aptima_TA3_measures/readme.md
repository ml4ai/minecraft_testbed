# Overview
This section documents metrics and procedure by which TA3 will evaluate ASI and Analytic Components (ACs). Additioanl measures are defined in documentation of AC agents. The metrics and measures described here are designed to advance the science and provide quantitative support for the program's claims that social science measures influence the design of ASI Machine Theory of Teams, which drives interventions, which influence team process, which may influence teamwork effects. Further detail is available in the [Evaluation section of the Study-3 Pre-Registration](https://docs.google.com/document/d/1GF7VsNF9R95IAaj6mVZUDV2mAX5ok1Bh6Tcm8zDpIkg/edit#heading=h.49x2ik5)

# Measure id: AC-M1: AC Use 
## Measurements (output)
- For each TA2, 1 point for each AC created that is produced and used by or in any ASI. 
## Observables (input)
- Survey responses
- Which TA1 team do you represent? [List of TA1 teams + radio button]
- Which Analytic Components does your ASI use? [List of ACs (and 'other') with checkboxes, and comment field]
- Why do use each AC?
## Bus message format
- None. This is a survey of TA1s.
## Measurement procedure & frequency
- TA3 provides a survey instrument: a google form. TA1 provides responses.
- Measurements are published in a TA3 report after Study-3 is completed. 
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: AC-M2: AC Influence 
## Measurements (output)
- For each TA2, the count of its used ACs that influence interventions by at least one ASI. 
## Observables (input)
- Survey responses
- Which TA1 team do you represent? [List of TA1 teams + radio button]
- For each Analytic Components you used
- Describe concisely how you tested for influence 
- Indicate whether the AC did or did not influence interventions
- Provide any elaborative comments about your findings
- If the ASI cannot be run without an AC, please report this.
## Bus message format
- None. This is a survey of TA1s.
## Measurement procedure & frequency
- TA3 provides a survey instrument. TA1 provides responses.
- A TA1 or TA2 can prove that an AC has influence on interventions in an offline computational study in which (1) in a replay the ASI ignores AC input at the scenario start and following each Intervention (I), (2) the ASI generates a new intervention (I') or no intervention (!I) at all at the moment of the next intervention, (3) the researchers compare I with !I on existence, or compare I with I' on the differences such as the specificity, accuracy, relevance, clarity, timing, or targeting (to recipient(s)). - 
- Measurements are published in a TA3 report after Study-3 is completed.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: AC-M3: AC Effectiveness 
## Measurements (output)
- For each TA2, 1 if any of its used ACs support more effective teamwork interventions by any ASI; 0 otherwise.
## Observables (input)
- Survey responses
- Which TA1 team do you represent? [List of TA1 teams + radio button]
- For each Analytic Components you used
- Describe concisely how you tested for impact
- Indicate whether the intervention influenced by the AC did or did not affect participant behavior.
- Provide any elaborative comments about your findings
## Bus message format
- None. This is a survey of TA1s.
## Measurement procedure & frequency
- TA3 provides a survey instrument. TA1 provides responses.
- A TA1 or TA2 can prove that an AC enables effective interventions in a controlled, empirical or computational experiment. In such an experiment, an ASI generates interventions with and without the AC, team score is measured, and scores are found to be greater at the mean with interventions that are informed by AC than with interventions that are not informed by the AC. 
- Measurements are published in a TA3 report after Study-3 is completed.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M1: ASI Utility
## Type
- Teamwork Effects Measure
## Measurements (output)
- Mission score per trial.
## Observables (input)
- Mission score at mission end
## Bus message format
- Testbed measurement message schema
## Measurement procedure & frequency
- TA3 takes this measure from testbed messages
- Measurements are published in the measurement message on the message bus at the end of the trial.
## How to generate assessments from measures 
- Higher scores on effects are better. The acceptable tradeoff with team process scores is undefined at this time. 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M2: Synchronization
## Type
- Teamwork Process Measure
## Measurements (output)
-  Mean latency between subtasks of teamwork tasks per trial. Specifically, the mean latency between victim discovery and victim rescue computed as the average over all correctly rescued victims (time of delivery of victim to correct rescue site - time victim was discovered). Where time victim was discovered = the earliest (or minimum) of (1) Transporter signalling device for the room containing the victim, or (2) Medic completes stabilization of the victim.
## Observables (input)
- Observed start time for instance i of a teamwork task. Here, a reliable and computationally simple measure of victim discovery or, when that is unavailable, of victim treatment.
- Observed end time for instance of a teamwork task. Specifically, the time when a stabilized victim is delivered to the correct rescue site.
## Bus message format
- Testbed measurement message schema
## Measurement procedure & frequency
- TA3 takes this measure from testbed messages
- Measurements are published in the measurement message on the message bus upon each successful victim evacuation and at the end of the trial.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M3: Error Rate 
## Type
- Teamwork Process Measure
## Measurements (output)
- Percentage of subtasks of teamwork tasks that are completed per trial, measured as below. Specifically, the percentage of discovered victims who are not evacuated. 
- Measure = 1- (# victims rescued / # victims discovered)
- Score for execution (1) or omission (0) of each task. 
## Observables (input)
- Defined sequences of subtasks in team tasks
- Victims rescued
- Victims discovered
## Bus message format
- Testbed measurement message schema
## Measurement procedure & frequency
- TA3 takes this measure from testbed messages
- Measurements are published in the measurement message on the message bus upon each victim discovery, each evacuation, and at the end of the trial.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M4: Adaptation / Resilience
## Type
- Teamwork Process Measure
## Measurements (output)
- Percentage of pre-perturbation score per minute attained in post perturbation period (defined as the time from perturbation start to end of trial) normalized by the opportunity to score. 
- Measure:
- (post-perturbation period score/post-perturbation period mins)/(points available to score at start of post-perturbation period)
- /
- (pre-perturbation period score/pre-perturbation period mins)/(points available to score at start of pre-perturbation period)
## Observables (input)
- Time mark of perturbation 
- Time mark of end of trial
- Points available to score at start of trial 
- Points available to score at start of trial perturbation time
## Bus message format
- Testbed measurement message schema
## Measurement procedure & frequency
- TA3 takes this measure from testbed messages
- Measurements are published in the measurement message at the start of each perturbation and at the end of the mission.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M5: Coordinative Comms
## Type
- Teamwork Process Measure
## Measurements (output)
- A quantitative characterization of the complexity of team communication using entropy in the dynamical system. Entropy is defined as the level of irregularity in the flow of communications between team members.(i.e., Team Communication Dynamics). 
## Observables (input)
- Team verbal communication data including:
- Message start timestamps
- Message end timestamps
- Message sender
- Content (optional)
## Bus message format
- Testbed measurement message schema
## Measurement procedure & frequency
- TA3 captures this measure via ASR speech transcription and/or Zoom transcripts
- Intensity and distributions of team communications are calculated using calculations of over message frequency, duration, and intra-team variance.
- Temporal patterns of team communications are captured using timestamped communication events and analyzed with recurrence quantification analysis.
- Measurements are published in a report by TA3 after Study-3, not dynamically on the message bus.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M6: Perceived Utility of ASI
## Type
- Perceived Intervention Quality Measure
## Measurements (output)
- For each ASI, the mean score on a survey of trial participants concerning their assessment of the utility of the ASI. 
## Observables (input)
- Participant responses to survey 
- The advisor's recommendations improved our team score: 1 = strongly disagree, 7 = strongly agree
- The advisor's recommendations improved our team coordination: 1 = strongly disagree, 7 = strongly agree
## Bus message format
- Testbed measurement message schema
## Measurement procedure & frequency
- TA3 takes this measure in survey items at the end of each mission
- Measurements are published in the measurement message on the message bus after the post-mission survey is completed.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M7: Trust in ASI
## Type
- Perceived Intervention Quality Measure
## Measurements (output)
- For each ASI, the mean score on a survey of trial participants concerning their level of trust in the ASI. 
## Observables (input)
- Participant responses to survey 
- Purpose / Goal alignment: I felt comfortable depending on the ASIST agent: 1 = strongly disagree, 7 = strongly agree
- Process: I understand why the advisor made its recommendations: 1 = strongly disagree, 7 = strongly agree
## Bus message format
- Testbed measurement message schema
## Measurement procedure & frequency
- TA3 takes this measure in survey items at the end of each mission
- Measurements are published in the measurement message on the message bus after the post-mission survey is completed.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M8: Interventions
## Type
- ASI Intervention Quality
## Measurements (output)
- Count of interventions issued. 
## Observables (input)
- Defined by TA1
## Bus message format
- Defined by TA1
## Measurement procedure & frequency
- Defined by TA1, taken by TA1
- Measurements are reported to TA3 in after Study-3 data collection is completed
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M9: Compliance
## Type
- ASI Intervention Quality
## Measurements (output)
- Percentage of interventions issued with which team complied with interventions.
## Observables (input)
- Defined by TA1
## Bus message format
- Defined by TA1
## Measurement procedure & frequency
- Defined by TA1, taken by TA1, reported to TA3 in format tbd.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M10: Explanations
## Type
- ASI Intervention Quality
## Measurements (output)
- An analysis of TA1-defined classes of ASI-issued explanations for interventions issued and, optionally, for interventions generated but not issued. The explanation should cite the ACs that are influential in (not) making the intervention and in shaping its content.
## Observables (input)
- Defined by TA1
## Bus message format
- Defined by TA1, but probably reported after the experiment and not published to the message bus
## Measurement procedure & frequency
- Defined by TA1, taken by TA1, reported to TA3 in format tbd.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M11: MToT Existence Proof
## Type
- MToT
## Measurements (output)
- Defined by TA1
## Observables (input)
- Defined by TA1
## Bus message format
- Defined by TA1, but probably reported after the experiment and not published to the message bus
## Measurement procedure & frequency
- Defined by TA1, taken by TA1, reported to TA3 in format tbd.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M12: Inference
## Type
- MToT
## Measurements (output)
- As defined by TA1, the NRMSE of accuracy of an inference concerning the state of a participant or team (e.g., emergent leadership).
## Observables (input)
- Defined by TA1
## Bus message format
- Defined by TA1
## Measurement procedure & frequency
- Defined by TA1, taken by TA1, reported to TA3 in format tbd.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M13: Prediction
## Type
- MToT
## Measurements (output)
- As defined by TA1, the NRMSE of accuracy of a prediction concerning the actions of a participant or team (e.g., the co-performance of some task, latency between subtasks, number of subtasks executed)
## Observables (input)
- Defined by TA1
## Bus message format
- Defined by TA1
## Measurement procedure & frequency
- Defined by TA1, taken by TA1, reported to TA3 in format tbd.
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None

# Measure id: ASI-M14: Risk
## Type
- Teamwork Effects Measure
## Measurements (output)
- Sum of seconds that team member(s) were caught in trap rooms (threat rooms). Specifically: 
- When a team member escapes from a triggered trap room, report the seconds that the trap-triggering member exits room minus time of trigger.
- As the terminal score, report the sum of all above
## Observables (input)
- Time of room trigger event
- Team member who triggered the trap and is trapped in the room
- Time team member leaves the room
## Measurement procedure & frequency
- TA3 takes this measure from testbed messages
- Measurements are published in the measurement message on the message bus when the player that triggers the trap exits the room and at the end of the trial.
### Bus message format
- Testbed measurement message schema
## How to generate assessments from measures 
- There is no criterion for measurements to support assessment 
## Potential applications of the measurements 
- This measure is designed to support evaluation, not ASI MToT modeling or intervention
## Prior validation of the measure 
- None
	
# Agent Use (configuration, running, etc.) 
- This agent runs automatically with the testbed. There are no configuration parameters.
