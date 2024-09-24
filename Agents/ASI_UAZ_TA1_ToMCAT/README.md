# ToMCAT

## Study 3

### Interventions

1. **Introduction** 

    - **Category**: AI
    - **Team Process:** Affect Management 
    - **Process Item:** Share a sense of togetherness
    - **Goal:** Ensure the team knows about the agent's existence and goals. 
    - **Situation:** In the beginning of mission 2, the agent makes a brief introduction to the team and explains its goals.
    - **Prompt (team)**: "Hi, team. My name is ToMCAT. I will assist you throughout this mission to ..."
    - **Evaluation**: n.a. 
    - **Short-term Effects:**
        1. The team will know the agent will assist them in the trial.        
    - **Long-term Effects:**
        1. The team will get the sense the agent is part of the team.
    - **Used ACs**: None. No data is processed in this intervention.       

2. **Information Consistency** 

    - **Category**: SC
    - **Team Process:** Systems Monitoring    
    - **Process Item:** Reliable Information Sharing
    - **Goal:** Ensure the team has the right information in hand
    - **Situation:** The agent detects that participants marked victims with the incorrect types or vocalized the types wrong and are unlikely to correct their mistakes (e.g. the player is moving away from the location).
    - **Prompt (individual)**: "\[_Player Color_\], I see you \[placed the wrong marker / said the incorrect type\] for the last victim you interacted with."
    - **Evaluation**: By computing the variance in the rate of wrong information shared in mission 1 and mission 2. The value must be compared with the variance in the control group for statistical significance analysis.
    - **Short-term Effects:**
        1. If the mistake was with the marker placement. Players will go back to fix their mistakes immediately if they are in a searching phase. Otherwise, they will do so after they finish their current task. 
        2. If the problem was with the verbalization, they will fix their mistakes right away by communicating the right victim type to others.
    - **Long-term Effects:**
        1. Players will pay more attention next time they inform others about victim types.
    - **Used ACs**:
        1. AC_IHMC_TA2_Joint-Activity-Interdependence to evaluate short-term effect (detect if players are engaged on another task).
        2. uaz_dialog_agent AC + AC_UAZ_TA1_ToMCAT-SpeechAnalyzer to check if the intervention must be triggered.

3. **Assistance** 

    - **Category**: SC
    - **Team Process:** Team Monitoring   
    - **Process Item:** Assistance
    - **Goal:** Ensure teammates are helping each other when they need assistance.
    - **Situation:** The agent detects when players ask for help and are not assisted. This can happen in 3 different scenarios: 
        1. When saving a critical victim. 
        2. When trapped in a room. 
        3. When rubble is preventing the medic from rescuing victims.         
    - **Prompt (individual)**: 
        - "\[_Player Color_\], don't forget \[_Player Color_\] asked for your assistance recently."        
    - **Evaluation**: By computing:
        1. The reduction in time to assist others from mission 1 to mission 2 normalized by a distance factor.
    - **Short-term Effects:**
        1. Reduces idleness.  
    - **Long-term Effects:**
        1. Improves the players' sense of attention towards each other. 
    - **Used ACs**:         
        1. uaz_dialog_agent AC + AC_UAZ_TA1_ToMCAT-SpeechAnalyzer to check if the intervention must be triggered.    

4. **Communication** 

    - **Category**: SC
    - **Team Process:** Coordination   
    - **Process Item:** Communication/Information sharing
    - **Goal:** Ensure teammates properly ask for help, decrease in the probability of mistakes and reduction in wasted time (e.g. players revisit areas already cleared)
    - **Situation:** The agent detects opportunities for intervening to improve team communication. We consider the intervention to be successful if participants that failed to share knowledge with each other via marker placement or verbally for these kinds of situations before the intervention start to do so. More concretely, this intervention is triggered when:
        1. Participants are trapped, but fail to ask their teammates for help.
        2. Participants do not inform their teammates about mission-relevant information (threat room existence, victim type, victim existence/absence). 
    - **Prompt (individual)**: 
        - "\[_Player Color_\], I see you have been trapped in a threat room for a while but have not asked the engineer to help you out. Please make sure to ask your teammates for help when you need it."
        - "\[_Player Color_\], I see you are waiting for another player to rescue the critical victim but have not let your team know."
        - "\[_Player Color_\], I see you are waiting for the engineer to clear a section of rubble but have not asked them for help. Please make sure to ask your teammates for help when you need it."
        - "\[_Player Color_\], I see you did not place a marker or tell the others the room you \[just left/passed by\] contains a threat. Consider placing a marker outside the threat room to warn your teammates."
        - "\[_Player Color_\], I see you did not place a marker or tell the others the type of victim you just rescued."
    - **Evaluation**: By computing:
        1. The increase in communication measured as the rate of markers placed or verbalizations made to mark victims, their types and threat rooms. 
        2. The decrease in time to let others know when help is needed.
    - **Short-term Effects:**
        1. Players will be encouraged to act on potentially irreversible mistakes. For instance, if a player does not let the others know about a victim type that was left for others to rescue, the player might forget about the victim type and the team won't be able to move the victim to the correct location. 
    - **Long-term Effects:**
        1. Improves communication and increases knowledge sharing. Additionally, it decreases the number of spurious tasks, like revisiting areas that were previously cleared.
    - **Used ACs**:
        1. AC_IHMC_TA2_Joint-Activity-Interdependence to check if the intervention must be triggered. 
        2. uaz_dialog_agent AC + AC_UAZ_TA1_ToMCAT-SpeechAnalyzer to check if the intervention must be triggered.  

5. **Motivation** 

    - **Category**: TM
    - **Team Process:** Confidence Building   
    - **Process Item:** Encouragement
    - **Goal:** Ensure the team stays motivated.
    - **Situation:** The agent keeps track of the rate of encouragement among team members (extracted from ASR extractions) and compare against the average among pilot teams (and possibly study 2 HSR data). If it is too small compared to the average, the agent intervenes.         
    - **Prompt (team)**: 
        - "Team, I suggest you encourage each other more during the mission to increase motivation."        
    - **Evaluation**: By computing:
        1. The increase in encouragement utterances. 
    - **Short-term Effects:** n.a.         
    - **Long-term Effects:**
        1. Keeps the team motivated.
    - **Used ACs**:        
        1. uaz_dialog_agent AC + AC_UAZ_TA1_ToMCAT-SpeechAnalyzer to identify utterances of the type _encouragement_.



