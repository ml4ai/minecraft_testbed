import sys
import re

from AgentTestFunctions.atomic_agent_test import atomic_agent_test
from AgentTestFunctions.asi_sift_asistant_test import asi_sift_asistant_test
from AgentTestFunctions.asi_uaz_ta1_tomcat import asi_uaz_ta1_tomcat_test
from AgentTestFunctions.asi_doll_ta1_rita import asi_doll_ta1_rita_test
from AgentTestFunctions.asi_cmu_ta1_atlas import asi_cmu_ta1_atlas_test
from AgentTestFunctions.asi_cra_ta1_psicoach import asi_cra_ta1_psicoach_test
from AgentTestFunctions.ac_rutgers_ta2_utility import ac_rutgers_ta2_utility_test
from AgentTestFunctions.as_cmu_ta2_ted import as_cmu_ta2_ted_test
from AgentTestFunctions.ac_cmu_ta2_beard import ac_cmu_ta2_beard_test
from AgentTestFunctions.ac_ihmc_ta2_location_monitor import ac_ihmc_ta2_location_monitor_test
from AgentTestFunctions.ac_ihmc_ta2_player_proximity import ac_ihmc_ta2_player_proximity_test
from AgentTestFunctions.ac_ihmc_ta2_dyad_reporting import ac_ihmc_ta2_dyad_reporting_test
from AgentTestFunctions.ac_ihmc_ta2_joint_activity_interdependence import ac_ihmc_ta2_joint_activity_interdependence_test
from AgentTestFunctions.ac_cmufms_ta2_cognitive import ac_cmufms_ta2_cognitive_test
from AgentTestFunctions.ac_gallup_ta2_gelp import ac_gallup_ta2_gelp_test
from AgentTestFunctions.ac_gallup_ta2_gold import ac_gallup_ta2_gold_test
from AgentTestFunctions.ac_ucf_ta2_playerprofiler import ac_ucf_ta2_playerprofiler_test
from AgentTestFunctions.ac_cmu_ta1_pyglfovagent import ac_cmu_ta1_pyglfovagent_test
from AgentTestFunctions.ac_cornell_ta2_teamtrust import ac_cornell_ta2_teamtrust_test
from AgentTestFunctions.ac_uaz_ta1_asr_agent import ac_uaz_ta1_asr_agent_test
from AgentTestFunctions.ac_uaz_ta1_speechanalyzer import ac_uaz_ta1_speechanalyzer_test
from AgentTestFunctions.uaz_dialog_agent import uaz_dialog_agent_test

class Test:
 
    
    def __init__(self,agent_name,lines,test_function,table):        
        self.run_tests = test_function
        self.agent_name = agent_name 
        self.ingest_lines_and_tests(agent_name,lines,table)
   

    def ingest_lines_and_tests(self,agent_name,lines,table): 

        self.run_tests(agent_name,lines,table)

if __name__ == "__main__":

    print('------------------------------------------------------------------------')
    print('Supplied Arguments : ')
    print(sys.argv)
    print(len(sys.argv))
    print('------------------------------------------------------------------------')


    incoming_file = sys.argv[1]
    outgoing_file = sys.argv[2]
    agents_to_test = re.split('\s', sys.argv[3])

    print("Testing agents .... this will take a bit of time.")    

    f = open(incoming_file, 'r',encoding='utf-8')

    lines = f.readlines()    

    print ( 'Read ' + str(len(lines)) + ' lines from source file.')

    f.close()

    table = {}
    
    test_dict = {
        # this mapping follows the naming scheme from the Agents/* subdirectories
        'atomic_agent': atomic_agent_test,
        'SIFT_Asistant_Agent': asi_sift_asistant_test,
        'ASI_UAZ_TA1_ToMCAT': asi_uaz_ta1_tomcat_test,
        'Rita_Agent': asi_doll_ta1_rita_test,
        'ASI_CMU_TA1_ATLAS': asi_cmu_ta1_atlas_test,
        'ASI_CRA_TA1_psicoach': asi_cra_ta1_psicoach_test,
        'RutgersUtilityAC':ac_rutgers_ta2_utility_test,
        'AC_CMU_TA2_TED':as_cmu_ta2_ted_test,
        'AC_CMU_TA2_BEARD':ac_cmu_ta2_beard_test,
        'AC_IHMC_TA2_Location-Monitor':ac_ihmc_ta2_location_monitor_test,
        'AC_IHMC_TA2_Player-Proximity':ac_ihmc_ta2_player_proximity_test,
        'AC_IHMC_TA2_Dyad-Reporting':ac_ihmc_ta2_dyad_reporting_test,
        'AC_IHMC_TA2_Joint-Activity-Interdependence':ac_ihmc_ta2_joint_activity_interdependence_test,
        'AC_CMUFMS_TA2_Cognitive':ac_cmufms_ta2_cognitive_test,
        'gallup_agent_gelp':ac_gallup_ta2_gelp_test,
        'gallup_agent_gold':ac_gallup_ta2_gold_test,
        'AC_UCF_TA2_PlayerProfiler':ac_ucf_ta2_playerprofiler_test,
        'AC_CMU_TA1_PyGLFoVAgent':ac_cmu_ta1_pyglfovagent_test,
        'ac_cornell_ta2_teamtrust':ac_cornell_ta2_teamtrust_test,
        'AC_UAZ_TA1_ASR_Agent':ac_uaz_ta1_asr_agent_test,
        'AC_UAZ_TA1_SpeechAnalyzer':ac_uaz_ta1_speechanalyzer_test,
        'uaz_dialog_agent':uaz_dialog_agent_test
    }

    for a in agents_to_test:
        Test(a,lines,test_dict[a],table)

    print('------------------------------------------------------------------------')


    print ("{:<28} {:<28} {:<10} {:<32} {:<30}".format('AC/ASI','Test ID','Success','Relevant Data', 'Predicate'))

    for k, v in table.items():
        test_id, success, data, predicate = v
        print ("{:<28} {:<28} {:<10} {:<32} {:<30}".format(test_id, k, success, data, predicate))
        

    
    print('------------------------------------------------------------------------')

    f = open(outgoing_file, 'a',encoding='utf-8')

    for k, v in table.items():
        test_id, success, data, predicate = v
        f.write("{:<28} {:<28} {:<10} {:<32} {:<30}".format(test_id, k, success, data, predicate))
        f.write("\n")
    
    f.close()
 
