from sys import *
from math import *
from borg import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from  random import randint
import pyswmm
from pyswmm import Simulation, LidControls, LidGroups, Subcatchments
import os
import swmmio as sio
from scipy.signal import find_peaks
from statistics import mean

nvars = 156
nobjs = 3
nconstrs = 2

def pySWMMio(*vars):
    
    borgvarslist = []
    objs = [1]*nobjs
    constrs = [1]*nconstrs

    #_____________________Cast Borg decision variables to a list________________________
    for i in range(156):
        
        borgvarslist.append(vars[i])

    #_______________________Organize variable file and folder names______________________

    subbasin_attributes = pd.read_csv(r"/LID_Optimization_Model/SubBasinAttributes.csv")
    subbasin_attributes = subbasin_attributes.set_index('Subbasin')
    swmm_folder = (r"/SWMM_Model")
    swmmio_altered_inp_file_name = (r"/SWMMIO_Altered_INPUTS/35-40_Mil")
    pyswmm_results_txt_folder =  (r"/SWMM_Output/35-40_Mil_Results")

    #____________________Set cost constraints________________________

    upper_cost_limit = 40000000
    lower_cost_limit = 0
    
    #_________________Create duplicate files for parallel simulation_________

    rando_n = str(randint(0,99999999))
    random_number = rando_n
    output_text_file = ("/SWMM_RESULTS"+random_number+".txt")
    altered_SWMMIO_inp = ("/SWMMIO_Altered_Inputs"+random_number+".inp")
    altered_SWMMIO_out = ("/SWMMIO_Altered_Inputs"+random_number+".out")

    
  #_________________________________Pass in Borg decision variables corresponding to fraction of feasible LID space allocated______________________________________


    subbasin_attributes.at[1,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[1,'Feasible_PermeablePavement_Space']*borgvarslist[0] 
    subbasin_attributes.at[1,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[1,'Feasible_GrassSwale_Space']*borgvarslist[1] 
    subbasin_attributes.at[1,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[1,'Feasible_GreenRoof_Space']*borgvarslist[2] 
    subbasin_attributes.at[1,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[1,'Feasible_Bioretention_Space']*borgvarslist[3] 
    subbasin_attributes.at[1,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[1,'Feasible_RainGarden_Space']*borgvarslist[4] 
    subbasin_attributes.at[1,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[1,'Perc_Imperv']-subbasin_attributes.at[1,'Removable_Imp']*borgvarslist[5] 

    subbasin_attributes.at[2,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[2,'Feasible_PermeablePavement_Space']*borgvarslist[6]
    subbasin_attributes.at[2,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[2,'Feasible_GrassSwale_Space']*borgvarslist[7]
    subbasin_attributes.at[2,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[2,'Feasible_GreenRoof_Space']*borgvarslist[8]
    subbasin_attributes.at[2,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[2,'Feasible_Bioretention_Space']*borgvarslist[9]
    subbasin_attributes.at[2,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[2,'Feasible_RainGarden_Space']*borgvarslist[10]
    subbasin_attributes.at[2,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[2,'Perc_Imperv']-subbasin_attributes.at[2,'Removable_Imp']*borgvarslist[11] 

    subbasin_attributes.at[3,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[3,'Feasible_PermeablePavement_Space']*borgvarslist[12]
    subbasin_attributes.at[3,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[3,'Feasible_GrassSwale_Space']*borgvarslist[13]
    subbasin_attributes.at[3,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[3,'Feasible_GreenRoof_Space']*borgvarslist[14] 
    subbasin_attributes.at[3,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[3,'Feasible_Bioretention_Space']*borgvarslist[15] 
    subbasin_attributes.at[3,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[3,'Feasible_RainGarden_Space']*borgvarslist[16]
    subbasin_attributes.at[3,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[3,'Perc_Imperv']-subbasin_attributes.at[3,'Removable_Imp']*borgvarslist[17] 
 
    subbasin_attributes.at[4,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[4,'Feasible_PermeablePavement_Space']*borgvarslist[18]
    subbasin_attributes.at[4,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[4,'Feasible_GrassSwale_Space']*borgvarslist[19] 
    subbasin_attributes.at[4,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[4,'Feasible_GreenRoof_Space']*borgvarslist[20] 
    subbasin_attributes.at[4,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[4,'Feasible_Bioretention_Space']*borgvarslist[21] 
    subbasin_attributes.at[4,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[4,'Feasible_RainGarden_Space']*borgvarslist[22]
    subbasin_attributes.at[4,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[4,'Perc_Imperv']-subbasin_attributes.at[4,'Removable_Imp']*borgvarslist[23] 


    subbasin_attributes.at[5,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[5,'Feasible_PermeablePavement_Space']*borgvarslist[24]
    subbasin_attributes.at[5,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[5,'Feasible_GrassSwale_Space']*borgvarslist[25] 
    subbasin_attributes.at[5,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[5,'Feasible_GreenRoof_Space']*borgvarslist[26] 
    subbasin_attributes.at[5,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[5,'Feasible_Bioretention_Space']*borgvarslist[27] 
    subbasin_attributes.at[5,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[5,'Feasible_RainGarden_Space']*borgvarslist[28]
    subbasin_attributes.at[5,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[5,'Perc_Imperv']-subbasin_attributes.at[5,'Removable_Imp']*borgvarslist[29] 
 
    subbasin_attributes.at[6,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[6,'Feasible_PermeablePavement_Space']*borgvarslist[30]
    subbasin_attributes.at[6,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[6,'Feasible_GrassSwale_Space']*borgvarslist[31] 
    subbasin_attributes.at[6,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[6,'Feasible_GreenRoof_Space']*borgvarslist[32] 
    subbasin_attributes.at[6,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[6,'Feasible_Bioretention_Space']*borgvarslist[33] 
    subbasin_attributes.at[6,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[6,'Feasible_RainGarden_Space']*borgvarslist[34] 
    subbasin_attributes.at[6,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[6,'Perc_Imperv']-subbasin_attributes.at[6,'Removable_Imp']*borgvarslist[35] 


    subbasin_attributes.at[7,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[7,'Feasible_PermeablePavement_Space']*borgvarslist[36]
    subbasin_attributes.at[7,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[7,'Feasible_GrassSwale_Space']*borgvarslist[37] 
    subbasin_attributes.at[7,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[7,'Feasible_GreenRoof_Space']*borgvarslist[38] 
    subbasin_attributes.at[7,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[7,'Feasible_Bioretention_Space']*borgvarslist[39] 
    subbasin_attributes.at[7,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[7,'Feasible_RainGarden_Space']*borgvarslist[40]
    subbasin_attributes.at[7,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[7,'Perc_Imperv']-subbasin_attributes.at[7,'Removable_Imp']*borgvarslist[41]


    subbasin_attributes.at[8,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[8,'Feasible_PermeablePavement_Space']*borgvarslist[42]
    subbasin_attributes.at[8,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[8,'Feasible_GrassSwale_Space']*borgvarslist[43] 
    subbasin_attributes.at[8,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[8,'Feasible_GreenRoof_Space']*borgvarslist[44] 
    subbasin_attributes.at[8,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[8,'Feasible_Bioretention_Space']*borgvarslist[45] 
    subbasin_attributes.at[8,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[8,'Feasible_RainGarden_Space']*borgvarslist[46] 
    subbasin_attributes.at[8,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[8,'Perc_Imperv']-subbasin_attributes.at[8,'Removable_Imp']*borgvarslist[47] 


    subbasin_attributes.at[9,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[9,'Feasible_PermeablePavement_Space']*borgvarslist[48]
    subbasin_attributes.at[9,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[9,'Feasible_GrassSwale_Space']*borgvarslist[49] 
    subbasin_attributes.at[9,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[9,'Feasible_GreenRoof_Space']*borgvarslist[50] 
    subbasin_attributes.at[9,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[9,'Feasible_Bioretention_Space']*borgvarslist[51] 
    subbasin_attributes.at[9,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[9,'Feasible_RainGarden_Space']*borgvarslist[52]
    subbasin_attributes.at[9,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[9,'Perc_Imperv']-subbasin_attributes.at[9,'Removable_Imp']*borgvarslist[53] 

 
    subbasin_attributes.at[10,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[10,'Feasible_PermeablePavement_Space']*borgvarslist[54]
    subbasin_attributes.at[10,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[10,'Feasible_GrassSwale_Space']*borgvarslist[55] 
    subbasin_attributes.at[10,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[10,'Feasible_GreenRoof_Space']*borgvarslist[56] 
    subbasin_attributes.at[10,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[10,'Feasible_Bioretention_Space']*borgvarslist[57] 
    subbasin_attributes.at[10,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[10,'Feasible_RainGarden_Space']*borgvarslist[58]
    subbasin_attributes.at[10,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[10,'Perc_Imperv']-subbasin_attributes.at[10,'Removable_Imp']*borgvarslist[59] 
    

    subbasin_attributes.at[11,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[11,'Feasible_PermeablePavement_Space']*borgvarslist[60]
    subbasin_attributes.at[11,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[11,'Feasible_GrassSwale_Space']*borgvarslist[61]
    subbasin_attributes.at[11,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[11,'Feasible_GreenRoof_Space']*borgvarslist[62]
    subbasin_attributes.at[11,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[11,'Feasible_Bioretention_Space']*borgvarslist[63] 
    subbasin_attributes.at[11,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[11,'Feasible_RainGarden_Space']*borgvarslist[64]
    subbasin_attributes.at[11,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[11,'Perc_Imperv']-subbasin_attributes.at[11,'Removable_Imp']*borgvarslist[65] 
    

    subbasin_attributes.at[12,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[12,'Feasible_PermeablePavement_Space']*borgvarslist[66]
    subbasin_attributes.at[12,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[12,'Feasible_GrassSwale_Space']*borgvarslist[67]
    subbasin_attributes.at[12,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[12,'Feasible_GreenRoof_Space']*borgvarslist[68]
    subbasin_attributes.at[12,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[12,'Feasible_Bioretention_Space']*borgvarslist[69]
    subbasin_attributes.at[12,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[12,'Feasible_RainGarden_Space']*borgvarslist[70]
    subbasin_attributes.at[12,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[12,'Perc_Imperv']-subbasin_attributes.at[12,'Removable_Imp']*borgvarslist[71] 


    subbasin_attributes.at[13,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[13,'Feasible_PermeablePavement_Space']*borgvarslist[72]
    subbasin_attributes.at[13,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[13,'Feasible_GrassSwale_Space']*borgvarslist[73]
    subbasin_attributes.at[13,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[13,'Feasible_GreenRoof_Space']*borgvarslist[74] 
    subbasin_attributes.at[13,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[13,'Feasible_Bioretention_Space']*borgvarslist[75]
    subbasin_attributes.at[13,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[13,'Feasible_RainGarden_Space']*borgvarslist[76] 
    subbasin_attributes.at[13,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[13,'Perc_Imperv']-subbasin_attributes.at[13,'Removable_Imp']*borgvarslist[77] 


    subbasin_attributes.at[14,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[14,'Feasible_PermeablePavement_Space']*borgvarslist[78]
    subbasin_attributes.at[14,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[14,'Feasible_GrassSwale_Space']*borgvarslist[79] 
    subbasin_attributes.at[14,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[14,'Feasible_GreenRoof_Space']*borgvarslist[80] 
    subbasin_attributes.at[14,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[14,'Feasible_Bioretention_Space']*borgvarslist[81] 
    subbasin_attributes.at[14,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[14,'Feasible_RainGarden_Space']*borgvarslist[82]
    subbasin_attributes.at[14,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[14,'Perc_Imperv']-subbasin_attributes.at[14,'Removable_Imp']*borgvarslist[83] 


    subbasin_attributes.at[15,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[15,'Feasible_PermeablePavement_Space']*borgvarslist[84]
    subbasin_attributes.at[15,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[15,'Feasible_GrassSwale_Space']*borgvarslist[85] 
    subbasin_attributes.at[15,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[15,'Feasible_GreenRoof_Space']*borgvarslist[86] 
    subbasin_attributes.at[15,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[15,'Feasible_Bioretention_Space']*borgvarslist[87] 
    subbasin_attributes.at[15,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[15,'Feasible_RainGarden_Space']*borgvarslist[88]
    subbasin_attributes.at[15,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[15,'Perc_Imperv']-subbasin_attributes.at[15,'Removable_Imp']*borgvarslist[89] 


    subbasin_attributes.at[16,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[16,'Feasible_PermeablePavement_Space']*borgvarslist[90]
    subbasin_attributes.at[16,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[16,'Feasible_GrassSwale_Space']*borgvarslist[91] 
    subbasin_attributes.at[16,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[16,'Feasible_GreenRoof_Space']*borgvarslist[92] 
    subbasin_attributes.at[16,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[16,'Feasible_Bioretention_Space']*borgvarslist[93] 
    subbasin_attributes.at[16,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[16,'Feasible_RainGarden_Space']*borgvarslist[94] 
    subbasin_attributes.at[16,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[16,'Perc_Imperv']-subbasin_attributes.at[16,'Removable_Imp']*borgvarslist[95] 


    subbasin_attributes.at[17,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[17,'Feasible_PermeablePavement_Space']*borgvarslist[96]
    subbasin_attributes.at[17,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[17,'Feasible_GrassSwale_Space']*borgvarslist[97] 
    subbasin_attributes.at[17,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[17,'Feasible_GreenRoof_Space']*borgvarslist[98] 
    subbasin_attributes.at[17,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[17,'Feasible_Bioretention_Space']*borgvarslist[99] 
    subbasin_attributes.at[17,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[17,'Feasible_RainGarden_Space']*borgvarslist[100]
    subbasin_attributes.at[17,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[17,'Perc_Imperv']-subbasin_attributes.at[17,'Removable_Imp']*borgvarslist[101] 
    

    subbasin_attributes.at[18,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[18,'Feasible_PermeablePavement_Space']*borgvarslist[102]
    subbasin_attributes.at[18,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[18,'Feasible_GrassSwale_Space']*borgvarslist[103] 
    subbasin_attributes.at[18,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[18,'Feasible_GreenRoof_Space']*borgvarslist[104] 
    subbasin_attributes.at[18,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[18,'Feasible_Bioretention_Space']*borgvarslist[105] 
    subbasin_attributes.at[18,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[18,'Feasible_RainGarden_Space']*borgvarslist[106]
    subbasin_attributes.at[18,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[18,'Perc_Imperv']-subbasin_attributes.at[18,'Removable_Imp']*borgvarslist[107] 
    

    subbasin_attributes.at[19,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[19,'Feasible_PermeablePavement_Space']*borgvarslist[108]
    subbasin_attributes.at[19,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[19,'Feasible_GrassSwale_Space']*borgvarslist[109] 
    subbasin_attributes.at[19,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[19,'Feasible_GreenRoof_Space']*borgvarslist[110] 
    subbasin_attributes.at[19,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[19,'Feasible_Bioretention_Space']*borgvarslist[111] 
    subbasin_attributes.at[19,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[19,'Feasible_RainGarden_Space']*borgvarslist[112]
    subbasin_attributes.at[19,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[19,'Perc_Imperv']-subbasin_attributes.at[19,'Removable_Imp']*borgvarslist[113] 


    subbasin_attributes.at[20,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[20,'Feasible_PermeablePavement_Space']*borgvarslist[114]
    subbasin_attributes.at[20,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[20,'Feasible_GrassSwale_Space']*borgvarslist[115] 
    subbasin_attributes.at[20,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[20,'Feasible_GreenRoof_Space']*borgvarslist[116] 
    subbasin_attributes.at[20,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[20,'Feasible_Bioretention_Space']*borgvarslist[117] 
    subbasin_attributes.at[20,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[20,'Feasible_RainGarden_Space']*borgvarslist[118] 
    subbasin_attributes.at[20,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[20,'Perc_Imperv']-subbasin_attributes.at[20,'Removable_Imp']*borgvarslist[119] 


    subbasin_attributes.at[21,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[21,'Feasible_PermeablePavement_Space']*borgvarslist[120]
    subbasin_attributes.at[21,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[21,'Feasible_GrassSwale_Space']*borgvarslist[121] 
    subbasin_attributes.at[21,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[21,'Feasible_GreenRoof_Space']*borgvarslist[122] 
    subbasin_attributes.at[21,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[21,'Feasible_Bioretention_Space']*borgvarslist[123] 
    subbasin_attributes.at[21,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[21,'Feasible_RainGarden_Space']*borgvarslist[124] 
    subbasin_attributes.at[21,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[21,'Perc_Imperv']-subbasin_attributes.at[21,'Removable_Imp']*borgvarslist[125] 


    subbasin_attributes.at[22,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[22,'Feasible_PermeablePavement_Space']*borgvarslist[126]
    subbasin_attributes.at[22,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[22,'Feasible_GrassSwale_Space']*borgvarslist[127] 
    subbasin_attributes.at[22,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[22,'Feasible_GreenRoof_Space']*borgvarslist[128] 
    subbasin_attributes.at[22,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[22,'Feasible_Bioretention_Space']*borgvarslist[129]
    subbasin_attributes.at[22,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[22,'Feasible_RainGarden_Space']*borgvarslist[130]
    subbasin_attributes.at[22,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[22,'Perc_Imperv']-subbasin_attributes.at[22,'Removable_Imp']*borgvarslist[131] 


    subbasin_attributes.at[23,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[23,'Feasible_PermeablePavement_Space']*borgvarslist[132]
    subbasin_attributes.at[23,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[23,'Feasible_GrassSwale_Space']*borgvarslist[133]
    subbasin_attributes.at[23,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[23,'Feasible_GreenRoof_Space']*borgvarslist[134] 
    subbasin_attributes.at[23,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[23,'Feasible_Bioretention_Space']*borgvarslist[135] 
    subbasin_attributes.at[23,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[23,'Feasible_RainGarden_Space']*borgvarslist[136] 
    subbasin_attributes.at[23,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[23,'Perc_Imperv']-subbasin_attributes.at[23,'Removable_Imp']*borgvarslist[137] 


    subbasin_attributes.at[24,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[24,'Feasible_PermeablePavement_Space']*borgvarslist[138]
    subbasin_attributes.at[24,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[24,'Feasible_GrassSwale_Space']*borgvarslist[139]
    subbasin_attributes.at[24,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[24,'Feasible_GreenRoof_Space']*borgvarslist[140] 
    subbasin_attributes.at[24,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[24,'Feasible_Bioretention_Space']*borgvarslist[141] 
    subbasin_attributes.at[24,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[24,'Feasible_RainGarden_Space']*borgvarslist[142]
    subbasin_attributes.at[24,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[24,'Perc_Imperv']-subbasin_attributes.at[24,'Removable_Imp']*borgvarslist[143] 


    subbasin_attributes.at[25,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[25,'Feasible_PermeablePavement_Space']*borgvarslist[144]
    subbasin_attributes.at[25,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[25,'Feasible_GrassSwale_Space']*borgvarslist[145]
    subbasin_attributes.at[25,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[25,'Feasible_GreenRoof_Space']*borgvarslist[146] 
    subbasin_attributes.at[25,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[25,'Feasible_Bioretention_Space']*borgvarslist[147] 
    subbasin_attributes.at[25,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[25,'Feasible_RainGarden_Space']*borgvarslist[148]
    subbasin_attributes.at[25,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[25,'Perc_Imperv']-subbasin_attributes.at[25,'Removable_Imp']*borgvarslist[149] 
  

    subbasin_attributes.at[26,'PermeablePavement_Assigned_Areas'] = subbasin_attributes.at[26,'Feasible_PermeablePavement_Space']*borgvarslist[150]
    subbasin_attributes.at[26,'GrassSwale_Assigned_Areas'] = subbasin_attributes.at[26,'Feasible_GrassSwale_Space']*borgvarslist[151] 
    subbasin_attributes.at[26,'GreenRoof_Assigned_Areas'] = subbasin_attributes.at[26,'Feasible_GreenRoof_Space']*borgvarslist[152] 
    subbasin_attributes.at[26,'Bioretention_Assigned_Areas'] = subbasin_attributes.at[26,'Feasible_Bioretention_Space']*borgvarslist[153] 
    subbasin_attributes.at[26,'RainGarden_Assigned_Areas'] = subbasin_attributes.at[26,'Feasible_RainGarden_Space']*borgvarslist[154]
    subbasin_attributes.at[26,'New_Perc_Imp_Post_Removal'] = subbasin_attributes.at[26,'Perc_Imperv']-subbasin_attributes.at[26,'Removable_Imp']*borgvarslist[155] 
  
    

  #__________________________Generate SWMM Subcatchment and LID Control Updates and Cost Constraints_____________________________
        
    # ## Calculate total implemented LID areas for each subbasin


    subbasin_attributes["Total_LID_Area"] = ""
    subbasin_attributes["Total_Green_LID_Area"] = ""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Total_LID_Area'] = (((subbasin_attributes.at[subbasin,'Perc_Imperv']*subbasin_attributes.at[subbasin,'Areas']/100)-(subbasin_attributes.at[subbasin,'New_Perc_Imp_Post_Removal']*subbasin_attributes.at[subbasin,'Areas']/100))+subbasin_attributes.at[subbasin,'RainGarden_Assigned_Areas'] + subbasin_attributes.at[subbasin,'Bioretention_Assigned_Areas']+ subbasin_attributes.at[subbasin,'GreenRoof_Assigned_Areas'] +subbasin_attributes.at[subbasin,'PermeablePavement_Assigned_Areas']+subbasin_attributes.at[subbasin,'GrassSwale_Assigned_Areas'])
        subbasin_attributes.at[subbasin,'Total_Green_LID_Area'] = (((subbasin_attributes.at[subbasin,'Perc_Imperv']*subbasin_attributes.at[subbasin,'Areas']/100)-(subbasin_attributes.at[subbasin,'New_Perc_Imp_Post_Removal']*subbasin_attributes.at[subbasin,'Areas']/100))+subbasin_attributes.at[subbasin,'RainGarden_Assigned_Areas'] + subbasin_attributes.at[subbasin,'Bioretention_Assigned_Areas']+ subbasin_attributes.at[subbasin,'GreenRoof_Assigned_Areas']+subbasin_attributes.at[subbasin,'GrassSwale_Assigned_Areas'])

# ## Update impervious, Perv, and LID areas for each subbasin after LID implementation


    subbasin_attributes['Updated_Imp_Areas']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Updated_Imp_Areas']= ((subbasin_attributes.at[subbasin,'New_Perc_Imp_Post_Removal']/100)*subbasin_attributes.at[subbasin,'Areas'] - subbasin_attributes.at[subbasin,'GreenRoof_Assigned_Areas']-subbasin_attributes.at[subbasin,'PermeablePavement_Assigned_Areas'])


    subbasin_attributes['Updated_Perv_Areas']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Updated_Perv_Areas']= (subbasin_attributes.at[subbasin,'Areas'] - subbasin_attributes.at[subbasin,'Updated_Imp_Areas'] - subbasin_attributes.at[subbasin,'Bioretention_Assigned_Areas']-subbasin_attributes.at[subbasin,'RainGarden_Assigned_Areas'] - subbasin_attributes.at[subbasin,'GrassSwale_Assigned_Areas'])


    subbasin_attributes['Updated_%Imp']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Updated_%Imp'] = subbasin_attributes.at[subbasin,'New_Perc_Imp_Post_Removal']
        


    # # Permeable Pavement LID Usage Editor Parameter Changes!
    # ## Permeable Pavement Percent Impervious Treated Calculation for each Subbasin



    subbasin_attributes['PermeablePavement_%ImpArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'PermeablePavement_%ImpArea_Treated'] = ((subbasin_attributes.at[subbasin,'PermeablePavement_Assigned_Areas']*2.5/subbasin_attributes.at[subbasin,'Updated_Imp_Areas'])*100)



# # Percent Impervious area and Percent Pervious area treated changes according to total LID area implemented
# # Following blocks calculate updated percent impervious area treated and percent impervious  changes for each subbasin based on LID scenario
# 

# ## RainGarden LID Usage Editor Parameter Changes!

# ### Calculations for RainGarden Percent Impervious Area Treated for each Subbasin


    subbasin_attributes['RainGarden_DrainageArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'RainGarden_DrainageArea_Treated']= subbasin_attributes.at[subbasin,'RainGarden_Assigned_Areas']*20


    subbasin_attributes['RainGarden_ImpervArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'RainGarden_ImpervArea_Treated'] = subbasin_attributes.at[subbasin,'RainGarden_DrainageArea_Treated']* 0.25


    subbasin_attributes['RainGarden_%ImpArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated'] = (subbasin_attributes.at[subbasin,'RainGarden_ImpervArea_Treated']*100/subbasin_attributes.at[subbasin,'Updated_Imp_Areas'])



    for subbasin in subbasin_attributes.index:
        if subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated'] > 100:
            subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated'] = 100



# ### Calculations for RainGarden Percent Pervious Area Treated for each Subbasin


    subbasin_attributes['RainGarden_PervArea_Treated'] =""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'RainGarden_PervArea_Treated'] = subbasin_attributes.at[subbasin,'RainGarden_DrainageArea_Treated'] * 0.75


    subbasin_attributes['RainGarden_%PervArea_Treated']=""
    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated'] = 100*subbasin_attributes.at[subbasin,'RainGarden_PervArea_Treated']/subbasin_attributes.at[subbasin,'Perv_Area']  


    for subbasin in subbasin_attributes.index:
        if subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated'] > 100:
            subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated'] = 100


# ## Bioretention LID Usage Editor Parameter Changes!

# ### Percent of Impervious Area Treated Calculations for each Subbasin


    subbasin_attributes['Bioretention_DrainageArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Bioretention_DrainageArea_Treated']= subbasin_attributes.at[subbasin,'Bioretention_Assigned_Areas']*20  


    subbasin_attributes['Bioretention_ImpervArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Bioretention_ImpervArea_Treated'] = subbasin_attributes.at[subbasin,'Bioretention_DrainageArea_Treated']* 0.3


    subbasin_attributes['Bioretention_%ImpArea_Treated']=""
    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated'] = (subbasin_attributes.at[subbasin,'Bioretention_ImpervArea_Treated']*100/subbasin_attributes.at[subbasin,'Updated_Imp_Areas'])

    for subbasin in subbasin_attributes.index:
        if subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated'] > 100:
            subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated'] = 100


# ### Bioretention Percent Pervious Area Treated for each Subbasin


    subbasin_attributes['Bioretention_PervArea_Treated'] =""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Bioretention_PervArea_Treated'] = subbasin_attributes.at[subbasin,'Bioretention_DrainageArea_Treated'] * 0.7

    subbasin_attributes['Bioretention_%PervArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated'] = 100*subbasin_attributes.at[subbasin,'Bioretention_PervArea_Treated']/subbasin_attributes.at[subbasin,'Perv_Area']


    for subbasin in subbasin_attributes.index:
        if subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated'] > 100:
            subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated'] = 100      


# ## Grass Swale LID Usage Editor Parameter Changes!

# ### Percent of Impervious Area Treated Calculations for each Subbasin


    subbasin_attributes['GrassSwale_DrainageArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GrassSwale_DrainageArea_Treated']= subbasin_attributes.at[subbasin,'GrassSwale_Assigned_Areas']*25   


    subbasin_attributes['GrassSwale_ImpervArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GrassSwale_ImpervArea_Treated'] = subbasin_attributes.at[subbasin,'GrassSwale_DrainageArea_Treated']* 0.3


    subbasin_attributes['GrassSwale_%ImpArea_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated'] = (subbasin_attributes.at[subbasin,'GrassSwale_ImpervArea_Treated']*100/subbasin_attributes.at[subbasin,'Updated_Imp_Areas'])


    for subbasin in subbasin_attributes.index:
        if subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated'] > 100:
            subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated'] = 100


# ### Percent of pervious Area Treated Calculations for each Subbasin


    subbasin_attributes['GrassSwale_PervArea_Treated'] =""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GrassSwale_PervArea_Treated'] = subbasin_attributes.at[subbasin,'GrassSwale_DrainageArea_Treated'] * 0.7


    subbasin_attributes['GrassSwale_%PervArea_Treated']=""
    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated'] = 100*subbasin_attributes.at[subbasin,'GrassSwale_PervArea_Treated']/subbasin_attributes.at[subbasin,'Perv_Area']   


    for subbasin in subbasin_attributes.index:
        if subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated'] > 100:
            subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated'] = 100    
            
        ##Setting Grass Swale Widths
    subbasin_attributes['GrassSwale_Widths']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GrassSwale_Widths'] = (subbasin_attributes.at[subbasin,'GrassSwale_Assigned_Areas']**0.5)/2
        if subbasin_attributes.at[subbasin,'GrassSwale_Widths'] == 0:
            subbasin_attributes.at[subbasin,'GrassSwale_Widths'] = 1

            
# ## Capping total %impervious and %pervious area treated at 100% for each subcatchment-LID combo. 


    subbasin_attributes['%Imp_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'%Imp_Treated'] = (subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated'] + subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated'] +subbasin_attributes.at[subbasin,'PermeablePavement_%ImpArea_Treated']+subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated'])


    subbasin_attributes['%Perv_Treated']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'%Perv_Treated']= (subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated']+ subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated']+subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated'])


# Pervious Surface Treated "Shaving"

    for subbasin in subbasin_attributes.index:

        while subbasin_attributes.at[subbasin,'%Perv_Treated'] > 100:
            subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated']= subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated']-0.25
            subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated']=subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated']-0.25
            subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated']=subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated']-0.25

            if subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated'] < 0:
                subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated'] = 0
            if subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated'] < 0:
                subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated'] = 0
            if subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated'] < 0:
                subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated'] = 0

            subbasin_attributes.at[subbasin, '%Perv_Treated'] = (subbasin_attributes.at[subbasin,'RainGarden_%PervArea_Treated']+subbasin_attributes.at[subbasin,'Bioretention_%PervArea_Treated']+subbasin_attributes.at[subbasin,'GrassSwale_%PervArea_Treated'])


# Impervious Surface Treated "Shaving"

    for subbasin in subbasin_attributes.index:

        while subbasin_attributes.at[subbasin,'%Imp_Treated'] > 100:
            subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated']=subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated']-0.25
            subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated']=subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated']-0.25
            subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated']=subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated']-0.25        


            if subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated'] < 0:
                subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated'] = 0
            if subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated'] < 0:
                subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated'] = 0
            if subbasin_attributes.at[subbasin,'PermeablePavement_%ImpArea_Treated'] < 0:
                subbasin_attributes.at[subbasin,'PermeablePavement_%ImpArea_Treated'] = 0
            if subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated'] < 0:
                subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated'] = 0


            subbasin_attributes.at[subbasin, '%Imp_Treated'] = (subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated']+subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated']+subbasin_attributes.at[subbasin,'PermeablePavement_%ImpArea_Treated']+subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated'])



#calculating costs for different LID scenarios

    subbasin_attributes["PermeablePavement_Costs"]=""

#assuming pervious concrete, installation ONLY - O&M unclear/makes price too high

    for subbasin in subbasin_attributes.index:
            subbasin_attributes.at[subbasin,'PermeablePavement_Costs'] = subbasin_attributes.at[subbasin,'PermeablePavement_Assigned_Areas'] * 8.16


    subbasin_attributes["GreenRoof_Costs"]=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GreenRoof_Costs'] = subbasin_attributes.at[subbasin,'GreenRoof_Assigned_Areas'] * 31.37        


# # Calculating Rain Garden Costs

    subbasin_attributes["Updated_RainGarden_ImpArea_Treated"] = ""
    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Updated_RainGarden_ImpArea_Treated'] = (subbasin_attributes.at[subbasin,'RainGarden_%ImpArea_Treated']/100) * subbasin_attributes.at[subbasin,'Updated_Imp_Areas']


    subbasin_attributes['Updated_RainGarden_ImpArea_Treated']    


    subbasin_attributes['RainGarden_Costs']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'RainGarden_Costs'] = subbasin_attributes.at[subbasin,'Updated_RainGarden_ImpArea_Treated'] * 3.27

# # Calculating Bioretention Costs

    subbasin_attributes["Updated_Bioretention_ImpArea_Treated"] = ""
    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Updated_Bioretention_ImpArea_Treated'] = (subbasin_attributes.at[subbasin,'Bioretention_%ImpArea_Treated']/100) * subbasin_attributes.at[subbasin,'Updated_Imp_Areas']


    subbasin_attributes['Updated_Bioretention_ImpArea_Treated']  


    subbasin_attributes['Bioretention_Costs']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Bioretention_Costs'] = 4.67 * subbasin_attributes.at[subbasin,'Updated_Bioretention_ImpArea_Treated']    


# # Calculating Grass Swale Costs


    subbasin_attributes["Updated_GrassSwale_ImpArea_Treated"] = ""
    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Updated_GrassSwale_ImpArea_Treated'] = (subbasin_attributes.at[subbasin,'GrassSwale_%ImpArea_Treated']/100) * subbasin_attributes.at[subbasin,'Updated_Imp_Areas']


    subbasin_attributes['GrassSwale_Costs']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'GrassSwale_Costs'] = 5.53 * subbasin_attributes.at[subbasin,'Updated_GrassSwale_ImpArea_Treated']
        
    subbasin_attributes['Subbasin_Total_LID_Costs']=""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Subbasin_Total_LID_Costs'] = (subbasin_attributes.at[subbasin,'Bioretention_Costs']+subbasin_attributes.at[subbasin,'GrassSwale_Costs']+subbasin_attributes.at[subbasin,'RainGarden_Costs']+subbasin_attributes.at[subbasin,'GreenRoof_Costs'] + subbasin_attributes.at[subbasin,'PermeablePavement_Costs'])
        
    
    subbasin_attributes['Imp_Removal_Costs'] =""

    for subbasin in subbasin_attributes.index:
        subbasin_attributes.at[subbasin,'Imp_Removal_Costs'] = 5.00*(((subbasin_attributes.at[subbasin,'Perc_Imperv']/100)*subbasin_attributes.at[subbasin,'Areas']) - subbasin_attributes.at[subbasin,'Updated_Imp_Areas'])
        


    #Cost Constraint
    
    cost_check = subbasin_attributes['GrassSwale_Costs'].sum()+subbasin_attributes['Bioretention_Costs'].sum()+subbasin_attributes['RainGarden_Costs'].sum()+subbasin_attributes['GreenRoof_Costs'].sum()+subbasin_attributes['PermeablePavement_Costs'].sum()+subbasin_attributes['Imp_Removal_Costs'].sum()

    subbasin_attributes['Percent_of_Green_LID_Space_Assigned'] = ''
    subbasin_attributes['Percent_of_LID_Space_Assigned'] = ''
    subbasin_attributes['Green_LID_Area_Ratio'] = ''

    for subbasin in subbasin_attributes.index:
        if subbasin_attributes.at[subbasin,'Total_LID_Area'] == 0:
            pass
        elif subbasin_attributes.at[subbasin,'Total_Green_LID_Area'] == 0:
            pass
        elif subbasin_attributes.at[subbasin,'Total_LID_Feasible_Area'] == 0:
            pass
        elif subbasin_attributes.at[subbasin,'Total_Green_LID_Feasible_Area'] == 0:
            pass
        else:
            subbasin_attributes.at[subbasin,'Percent_of_LID_Space_Assigned'] = (subbasin_attributes.at[subbasin,'Total_LID_Area']/subbasin_attributes.at[subbasin,'Total_LID_Feasible_Area'])*100
            subbasin_attributes.at[subbasin,'Percent_of_Green_LID_Space_Assigned'] = (subbasin_attributes.at[subbasin,'Total_Green_LID_Area']/subbasin_attributes.at[subbasin,'Total_Green_LID_Feasible_Area'])*100
            subbasin_attributes.at[subbasin,'Green_LID_Area_Ratio'] = (subbasin_attributes.at[subbasin,'Total_Green_LID_Area']/subbasin_attributes.at[subbasin,'Areas'])
            
    subbasin_attributes.to_csv(r"/sfs/lustre/bahamut/scratch/rsh6pb/C/Borg/Borg-1.8/temp_export_file_"+random_number+".csv")        
    temp_SB_csv = pd.read_csv(r"/sfs/lustre/bahamut/scratch/rsh6pb/C/Borg/Borg-1.8/temp_export_file_"+random_number+".csv")
    subbasinSEI = temp_SB_csv['MC_Index']
    green_LID_ratio = temp_SB_csv['Green_LID_Area_Ratio']

    correlation = (-1)*subbasinSEI.corr(green_LID_ratio)    

    correlation = round(correlation, 3)    







#________________________________SWMM Model Function and Results Analysis_____________________________________________________


    
#SWMMIO input file modifications



    baseline = sio.Model(swmm_folder)

    #isolate subcatchments dataframe
    subcatchments = baseline.inp.subcatchments


    #Set subcatchment parameters

    #Percent Impervious Adjustments

    subcatchments.loc['1','PercImperv'] = float(subbasin_attributes.at[1,'Updated_%Imp']) 
    subcatchments.loc['2','PercImperv'] = float(subbasin_attributes.at[2,'Updated_%Imp'])
    subcatchments.loc['3','PercImperv'] = float(subbasin_attributes.at[3,'Updated_%Imp'])
    subcatchments.loc['4','PercImperv'] = float(subbasin_attributes.at[4,'Updated_%Imp'])
    subcatchments.loc['5','PercImperv'] = float(subbasin_attributes.at[5,'Updated_%Imp'])
    subcatchments.loc['6','PercImperv'] = float(subbasin_attributes.at[6,'Updated_%Imp'])
    subcatchments.loc['7','PercImperv'] = float(subbasin_attributes.at[7,'Updated_%Imp'])
    subcatchments.loc['8','PercImperv'] = float(subbasin_attributes.at[8,'Updated_%Imp'])
    subcatchments.loc['9','PercImperv'] = float(subbasin_attributes.at[9,'Updated_%Imp']) 
    subcatchments.loc['10','PercImperv'] = float(subbasin_attributes.at[10,'Updated_%Imp'])
    subcatchments.loc['11','PercImperv'] = float(subbasin_attributes.at[11,'Updated_%Imp'])
    subcatchments.loc['12','PercImperv'] = float(subbasin_attributes.at[12,'Updated_%Imp'])
    subcatchments.loc['13','PercImperv'] = float(subbasin_attributes.at[13,'Updated_%Imp'])
    subcatchments.loc['14','PercImperv'] = float(subbasin_attributes.at[14,'Updated_%Imp'])
    subcatchments.loc['15','PercImperv'] = float(subbasin_attributes.at[15,'Updated_%Imp'])
    subcatchments.loc['16','PercImperv'] = float(subbasin_attributes.at[16,'Updated_%Imp'])
    subcatchments.loc['17','PercImperv'] = float(subbasin_attributes.at[17,'Updated_%Imp'])
    subcatchments.loc['18','PercImperv'] = float(subbasin_attributes.at[18,'Updated_%Imp'])
    subcatchments.loc['19','PercImperv'] = float(subbasin_attributes.at[19,'Updated_%Imp'])
    subcatchments.loc['20','PercImperv'] = float(subbasin_attributes.at[20,'Updated_%Imp'])
    subcatchments.loc['21','PercImperv'] = float(subbasin_attributes.at[21,'Updated_%Imp'])
    subcatchments.loc['22','PercImperv'] = float(subbasin_attributes.at[22,'Updated_%Imp'])
    subcatchments.loc['23','PercImperv'] = float(subbasin_attributes.at[23,'Updated_%Imp'])
    subcatchments.loc['24','PercImperv'] = float(subbasin_attributes.at[24,'Updated_%Imp'])
    subcatchments.loc['25','PercImperv'] = float(subbasin_attributes.at[25,'Updated_%Imp'])
    subcatchments.loc['26','PercImperv'] = float(subbasin_attributes.at[26,'Updated_%Imp'])

    #Width Adjustment((SUBBASIN AREA/Flow Length) - LID Width) or total width minus LID width)


    subcatchments.loc['1','Width'] = float(((subcatchments.loc['1','Area'] * 43560)/subbasin_attributes.at[1,'FlowLengths']) - (subbasin_attributes.at[1,'Total_LID_Area']/subbasin_attributes.at[1,'FlowLengths']))
    subcatchments.loc['2','Width'] = float(((subcatchments.loc['2','Area'] * 43560)/subbasin_attributes.at[2,'FlowLengths']) - (subbasin_attributes.at[2,'Total_LID_Area']/subbasin_attributes.at[2,'FlowLengths']))
    subcatchments.loc['3','Width'] = float(((subcatchments.loc['3','Area'] * 43560)/subbasin_attributes.at[3,'FlowLengths']) - (subbasin_attributes.at[3,'Total_LID_Area']/subbasin_attributes.at[3,'FlowLengths']))
    subcatchments.loc['4','Width'] = float(((subcatchments.loc['4','Area'] * 43560)/subbasin_attributes.at[4,'FlowLengths']) - (subbasin_attributes.at[4,'Total_LID_Area']/subbasin_attributes.at[4,'FlowLengths']))
    subcatchments.loc['5','Width'] = float(((subcatchments.loc['5','Area'] * 43560)/subbasin_attributes.at[5,'FlowLengths']) - (subbasin_attributes.at[5,'Total_LID_Area']/subbasin_attributes.at[5,'FlowLengths']))
    subcatchments.loc['6','Width'] = float(((subcatchments.loc['6','Area'] * 43560)/subbasin_attributes.at[6,'FlowLengths']) - (subbasin_attributes.at[6,'Total_LID_Area']/subbasin_attributes.at[6,'FlowLengths']))
    subcatchments.loc['7','Width'] = float(((subcatchments.loc['7','Area'] * 43560)/subbasin_attributes.at[7,'FlowLengths']) - (subbasin_attributes.at[7,'Total_LID_Area']/subbasin_attributes.at[7,'FlowLengths']))
    subcatchments.loc['8','Width'] = float(((subcatchments.loc['8','Area'] * 43560)/subbasin_attributes.at[8,'FlowLengths']) - (subbasin_attributes.at[8,'Total_LID_Area']/subbasin_attributes.at[8,'FlowLengths']))
    subcatchments.loc['9','Width'] = float(((subcatchments.loc['9','Area'] * 43560)/subbasin_attributes.at[9,'FlowLengths']) - (subbasin_attributes.at[9,'Total_LID_Area']/subbasin_attributes.at[9,'FlowLengths']))
    subcatchments.loc['10','Width'] = float(((subcatchments.loc['10','Area'] * 43560)/subbasin_attributes.at[10,'FlowLengths']) - (subbasin_attributes.at[10,'Total_LID_Area']/subbasin_attributes.at[10,'FlowLengths']))
    subcatchments.loc['11','Width'] = float(((subcatchments.loc['11','Area'] * 43560)/subbasin_attributes.at[11,'FlowLengths']) - (subbasin_attributes.at[11,'Total_LID_Area']/subbasin_attributes.at[11,'FlowLengths']))
    subcatchments.loc['12','Width'] = float(((subcatchments.loc['12','Area'] * 43560)/subbasin_attributes.at[12,'FlowLengths']) - (subbasin_attributes.at[12,'Total_LID_Area']/subbasin_attributes.at[12,'FlowLengths']))
    subcatchments.loc['13','Width'] = float(((subcatchments.loc['13','Area'] * 43560)/subbasin_attributes.at[13,'FlowLengths']) - (subbasin_attributes.at[13,'Total_LID_Area']/subbasin_attributes.at[13,'FlowLengths']))
    subcatchments.loc['14','Width'] = float(((subcatchments.loc['14','Area'] * 43560)/subbasin_attributes.at[14,'FlowLengths']) - (subbasin_attributes.at[14,'Total_LID_Area']/subbasin_attributes.at[14,'FlowLengths']))
    subcatchments.loc['15','Width'] = float(((subcatchments.loc['15','Area'] * 43560)/subbasin_attributes.at[15,'FlowLengths']) - (subbasin_attributes.at[15,'Total_LID_Area']/subbasin_attributes.at[15,'FlowLengths']))
    subcatchments.loc['16','Width'] = float(((subcatchments.loc['16','Area'] * 43560)/subbasin_attributes.at[16,'FlowLengths']) - (subbasin_attributes.at[16,'Total_LID_Area']/subbasin_attributes.at[16,'FlowLengths']))
    subcatchments.loc['17','Width'] = float(((subcatchments.loc['17','Area'] * 43560)/subbasin_attributes.at[17,'FlowLengths']) - (subbasin_attributes.at[17,'Total_LID_Area']/subbasin_attributes.at[17,'FlowLengths']))
    subcatchments.loc['18','Width'] = float(((subcatchments.loc['18','Area'] * 43560)/subbasin_attributes.at[18,'FlowLengths']) - (subbasin_attributes.at[18,'Total_LID_Area']/subbasin_attributes.at[18,'FlowLengths']))
    subcatchments.loc['19','Width'] = float(((subcatchments.loc['19','Area'] * 43560)/subbasin_attributes.at[19,'FlowLengths']) - (subbasin_attributes.at[19,'Total_LID_Area']/subbasin_attributes.at[19,'FlowLengths']))
    subcatchments.loc['20','Width'] = float(((subcatchments.loc['20','Area'] * 43560)/subbasin_attributes.at[20,'FlowLengths']) - (subbasin_attributes.at[20,'Total_LID_Area']/subbasin_attributes.at[20,'FlowLengths']))
    subcatchments.loc['21','Width'] = float(((subcatchments.loc['21','Area'] * 43560)/subbasin_attributes.at[21,'FlowLengths']) - (subbasin_attributes.at[21,'Total_LID_Area']/subbasin_attributes.at[21,'FlowLengths']))
    subcatchments.loc['22','Width'] = float(((subcatchments.loc['22','Area'] * 43560)/subbasin_attributes.at[22,'FlowLengths']) - (subbasin_attributes.at[22,'Total_LID_Area']/subbasin_attributes.at[22,'FlowLengths']))
    subcatchments.loc['23','Width'] = float(((subcatchments.loc['23','Area'] * 43560)/subbasin_attributes.at[23,'FlowLengths']) - (subbasin_attributes.at[23,'Total_LID_Area']/subbasin_attributes.at[23,'FlowLengths']))
    subcatchments.loc['24','Width'] = float(((subcatchments.loc['24','Area'] * 43560)/subbasin_attributes.at[24,'FlowLengths']) - (subbasin_attributes.at[24,'Total_LID_Area']/subbasin_attributes.at[24,'FlowLengths']))
    subcatchments.loc['25','Width'] = float(((subcatchments.loc['25','Area'] * 43560)/subbasin_attributes.at[25,'FlowLengths']) - (subbasin_attributes.at[25,'Total_LID_Area']/subbasin_attributes.at[25,'FlowLengths']))
    subcatchments.loc['26','Width'] = float(((subcatchments.loc['26','Area'] * 43560)/subbasin_attributes.at[26,'FlowLengths']) - (subbasin_attributes.at[26,'Total_LID_Area']/subbasin_attributes.at[26,'FlowLengths']))



    #save subcatchment dataframe changes to whole inp dataframe
    baseline.inp.subcatchments = subcatchments   

    #create the new inp file to use. 
    newfilepath = os.path.join(swmmio_altered_inp_file_name+altered_SWMMIO_inp)

    #Write the subcatchment section of the new model with the adjusted data

    baseline.inp.save(newfilepath)

    #PYSWMM LID Edits and SWMM Simulation

    #For parallelization, each output file needs to be unique


    with Simulation(swmmio_altered_inp_file_name+altered_SWMMIO_inp, reportfile = pyswmm_results_txt_folder+output_text_file) as sim:

        control_time_step = 86400*2
        sim.step_advance(control_time_step)
            #Load in subcatchment lid list
        lid_sub_1 = LidGroups(sim)['1']
        lid_sub_2 = LidGroups(sim)['2']                                                                                                                              
        lid_sub_3 = LidGroups(sim)['3']                                                                                                                              
        lid_sub_4 = LidGroups(sim)['4']
        lid_sub_5 = LidGroups(sim)['5']                                                                                                                              
        lid_sub_6 = LidGroups(sim)['6']                                                                                                                              
        lid_sub_7 = LidGroups(sim)['7']                                                                                                                              
        lid_sub_8 = LidGroups(sim)['8']                                                                                                                              
        lid_sub_9 = LidGroups(sim)['9']                                                                                                                              
        lid_sub_10 = LidGroups(sim)['10']                                                                                                                              
        lid_sub_11 = LidGroups(sim)['11']                                                                                                                              
        lid_sub_12 = LidGroups(sim)['12']                                                                                                                              
        lid_sub_13 = LidGroups(sim)['13']                                                                                                                              
        lid_sub_14 = LidGroups(sim)['14']                                                                                                                              
        lid_sub_15 = LidGroups(sim)['15']                                                                                                                              
        lid_sub_16 = LidGroups(sim)['16']                                                                                                                              
        lid_sub_17 = LidGroups(sim)['17']                                                                                                                              
        lid_sub_18 = LidGroups(sim)['18']                                                                                                                              
        lid_sub_19 = LidGroups(sim)['19']                                                                                                                              
        lid_sub_20 = LidGroups(sim)['20']                                                                                                                              
        lid_sub_21 = LidGroups(sim)['21']                                                                                                                              
        lid_sub_22 = LidGroups(sim)['22']                                                                                                                              
        lid_sub_23 = LidGroups(sim)['23']                                                                                                                              
        lid_sub_24 = LidGroups(sim)['24']                                                                                                                              
        lid_sub_25 = LidGroups(sim)['25']
        lid_sub_26 = LidGroups(sim)['26']                                                                                                                              
                                                                                                                                        
                                                                                                                                        
                                                                                                                                        #     #Set LID Areas!

    #Set LID Assigned areas in pyswmm
                                                                                                                                        
        lid_sub_1[0].unit_area = subbasin_attributes.at[1,'GreenRoof_Assigned_Areas']
        lid_sub_1[1].unit_area = subbasin_attributes.at[1,'PermeablePavement_Assigned_Areas']
        lid_sub_1[2].unit_area = subbasin_attributes.at[1,'RainGarden_Assigned_Areas']
        lid_sub_1[3].unit_area = subbasin_attributes.at[1,'Bioretention_Assigned_Areas']
        lid_sub_1[4].unit_area = subbasin_attributes.at[1,'GrassSwale_Assigned_Areas']
        
        lid_sub_2[0].unit_area = subbasin_attributes.at[2,'GreenRoof_Assigned_Areas']
        lid_sub_2[1].unit_area = subbasin_attributes.at[2,'PermeablePavement_Assigned_Areas']
        lid_sub_2[2].unit_area = subbasin_attributes.at[2,'RainGarden_Assigned_Areas']
        lid_sub_2[3].unit_area = subbasin_attributes.at[2,'Bioretention_Assigned_Areas']
        lid_sub_2[4].unit_area = subbasin_attributes.at[2,'GrassSwale_Assigned_Areas']  
                                                                                                                                        
        lid_sub_3[0].unit_area = subbasin_attributes.at[3,'GreenRoof_Assigned_Areas']
        lid_sub_3[1].unit_area = subbasin_attributes.at[3,'PermeablePavement_Assigned_Areas']
        lid_sub_3[2].unit_area = subbasin_attributes.at[3,'RainGarden_Assigned_Areas']
        lid_sub_3[3].unit_area = subbasin_attributes.at[3,'Bioretention_Assigned_Areas']
        lid_sub_3[4].unit_area = subbasin_attributes.at[3,'GrassSwale_Assigned_Areas'] 
                                                                                                                                        
        lid_sub_4[0].unit_area = subbasin_attributes.at[4,'GreenRoof_Assigned_Areas']
        lid_sub_4[1].unit_area = subbasin_attributes.at[4,'PermeablePavement_Assigned_Areas']
        lid_sub_4[2].unit_area = subbasin_attributes.at[4,'RainGarden_Assigned_Areas']
        lid_sub_4[3].unit_area = subbasin_attributes.at[4,'Bioretention_Assigned_Areas']
        lid_sub_4[4].unit_area = subbasin_attributes.at[4,'GrassSwale_Assigned_Areas']                                                                                                                                                                                                            
                                                                                                                                        
        lid_sub_5[0].unit_area = subbasin_attributes.at[5,'GreenRoof_Assigned_Areas']
        lid_sub_5[1].unit_area = subbasin_attributes.at[5,'PermeablePavement_Assigned_Areas']
        lid_sub_5[2].unit_area = subbasin_attributes.at[5,'RainGarden_Assigned_Areas']
        lid_sub_5[3].unit_area = subbasin_attributes.at[5,'Bioretention_Assigned_Areas']
        lid_sub_5[4].unit_area = subbasin_attributes.at[5,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_6[0].unit_area = subbasin_attributes.at[6,'GreenRoof_Assigned_Areas']
        lid_sub_6[1].unit_area = subbasin_attributes.at[6,'PermeablePavement_Assigned_Areas']
        lid_sub_6[2].unit_area = subbasin_attributes.at[6,'RainGarden_Assigned_Areas']
        lid_sub_6[3].unit_area = subbasin_attributes.at[6,'Bioretention_Assigned_Areas']
        lid_sub_6[4].unit_area = subbasin_attributes.at[6,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                
        lid_sub_7[0].unit_area = subbasin_attributes.at[7,'GreenRoof_Assigned_Areas']
        lid_sub_7[1].unit_area = subbasin_attributes.at[7,'PermeablePavement_Assigned_Areas']
        lid_sub_7[2].unit_area = subbasin_attributes.at[7,'RainGarden_Assigned_Areas']
        lid_sub_7[3].unit_area = subbasin_attributes.at[7,'Bioretention_Assigned_Areas']
        lid_sub_7[4].unit_area = subbasin_attributes.at[7,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_8[0].unit_area = subbasin_attributes.at[8,'GreenRoof_Assigned_Areas']
        lid_sub_8[1].unit_area = subbasin_attributes.at[8,'PermeablePavement_Assigned_Areas']
        lid_sub_8[2].unit_area = subbasin_attributes.at[8,'RainGarden_Assigned_Areas']
        lid_sub_8[3].unit_area = subbasin_attributes.at[8,'Bioretention_Assigned_Areas']
        lid_sub_8[4].unit_area = subbasin_attributes.at[8,'GrassSwale_Assigned_Areas']                                                                                                                              
        
        lid_sub_9[0].unit_area = subbasin_attributes.at[9,'GreenRoof_Assigned_Areas']
        lid_sub_9[1].unit_area = subbasin_attributes.at[9,'PermeablePavement_Assigned_Areas']
        lid_sub_9[2].unit_area = subbasin_attributes.at[9,'RainGarden_Assigned_Areas']
        lid_sub_9[3].unit_area = subbasin_attributes.at[9,'Bioretention_Assigned_Areas']
        lid_sub_9[4].unit_area = subbasin_attributes.at[9,'GrassSwale_Assigned_Areas']                                                                                                                              

        lid_sub_10[0].unit_area = subbasin_attributes.at[10,'GreenRoof_Assigned_Areas']
        lid_sub_10[1].unit_area = subbasin_attributes.at[10,'PermeablePavement_Assigned_Areas']
        lid_sub_10[2].unit_area = subbasin_attributes.at[10,'RainGarden_Assigned_Areas']
        lid_sub_10[3].unit_area = subbasin_attributes.at[10,'Bioretention_Assigned_Areas']
        lid_sub_10[4].unit_area = subbasin_attributes.at[10,'GrassSwale_Assigned_Areas']
                                                                                                                                        
        lid_sub_11[0].unit_area = subbasin_attributes.at[11,'GreenRoof_Assigned_Areas']
        lid_sub_11[1].unit_area = subbasin_attributes.at[11,'PermeablePavement_Assigned_Areas']
        lid_sub_11[2].unit_area = subbasin_attributes.at[11,'RainGarden_Assigned_Areas']
        lid_sub_11[3].unit_area = subbasin_attributes.at[11,'Bioretention_Assigned_Areas']
        lid_sub_11[4].unit_area = subbasin_attributes.at[11,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_12[0].unit_area = subbasin_attributes.at[12,'GreenRoof_Assigned_Areas']
        lid_sub_12[1].unit_area = subbasin_attributes.at[12,'PermeablePavement_Assigned_Areas']
        lid_sub_12[2].unit_area = subbasin_attributes.at[12,'RainGarden_Assigned_Areas']
        lid_sub_12[3].unit_area = subbasin_attributes.at[12,'Bioretention_Assigned_Areas']
        lid_sub_12[4].unit_area = subbasin_attributes.at[12,'GrassSwale_Assigned_Areas']                                                                                                                              

        lid_sub_13[0].unit_area = subbasin_attributes.at[13,'GreenRoof_Assigned_Areas']
        lid_sub_13[1].unit_area = subbasin_attributes.at[13,'PermeablePavement_Assigned_Areas']
        lid_sub_13[2].unit_area = subbasin_attributes.at[13,'RainGarden_Assigned_Areas']
        lid_sub_13[3].unit_area = subbasin_attributes.at[13,'Bioretention_Assigned_Areas']
        lid_sub_13[4].unit_area = subbasin_attributes.at[13,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_14[0].unit_area = subbasin_attributes.at[14,'GreenRoof_Assigned_Areas']
        lid_sub_14[1].unit_area = subbasin_attributes.at[14,'PermeablePavement_Assigned_Areas']
        lid_sub_14[2].unit_area = subbasin_attributes.at[14,'RainGarden_Assigned_Areas']
        lid_sub_14[3].unit_area = subbasin_attributes.at[14,'Bioretention_Assigned_Areas']
        lid_sub_14[4].unit_area = subbasin_attributes.at[14,'GrassSwale_Assigned_Areas']   
                                                                                                                                        
        lid_sub_15[0].unit_area = subbasin_attributes.at[15,'GreenRoof_Assigned_Areas']
        lid_sub_15[1].unit_area = subbasin_attributes.at[15,'PermeablePavement_Assigned_Areas']
        lid_sub_15[2].unit_area = subbasin_attributes.at[15,'RainGarden_Assigned_Areas']
        lid_sub_15[3].unit_area = subbasin_attributes.at[15,'Bioretention_Assigned_Areas']
        lid_sub_15[4].unit_area = subbasin_attributes.at[15,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_16[0].unit_area = subbasin_attributes.at[16,'GreenRoof_Assigned_Areas']
        lid_sub_16[1].unit_area = subbasin_attributes.at[16,'PermeablePavement_Assigned_Areas']
        lid_sub_16[2].unit_area = subbasin_attributes.at[16,'RainGarden_Assigned_Areas']
        lid_sub_16[3].unit_area = subbasin_attributes.at[16,'Bioretention_Assigned_Areas']
        lid_sub_16[4].unit_area = subbasin_attributes.at[16,'GrassSwale_Assigned_Areas']
                                                                                                                                        
        lid_sub_17[0].unit_area = subbasin_attributes.at[17,'GreenRoof_Assigned_Areas']
        lid_sub_17[1].unit_area = subbasin_attributes.at[17,'PermeablePavement_Assigned_Areas']
        lid_sub_17[2].unit_area = subbasin_attributes.at[17,'RainGarden_Assigned_Areas']
        lid_sub_17[3].unit_area = subbasin_attributes.at[17,'Bioretention_Assigned_Areas']
        lid_sub_17[4].unit_area = subbasin_attributes.at[17,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_18[0].unit_area = subbasin_attributes.at[18,'GreenRoof_Assigned_Areas']
        lid_sub_18[1].unit_area = subbasin_attributes.at[18,'PermeablePavement_Assigned_Areas']
        lid_sub_18[2].unit_area = subbasin_attributes.at[18,'RainGarden_Assigned_Areas']
        lid_sub_18[3].unit_area = subbasin_attributes.at[18,'Bioretention_Assigned_Areas']
        lid_sub_18[4].unit_area = subbasin_attributes.at[18,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_19[0].unit_area = subbasin_attributes.at[19,'GreenRoof_Assigned_Areas']
        lid_sub_19[1].unit_area = subbasin_attributes.at[19,'PermeablePavement_Assigned_Areas']
        lid_sub_19[2].unit_area = subbasin_attributes.at[19,'RainGarden_Assigned_Areas']
        lid_sub_19[3].unit_area = subbasin_attributes.at[19,'Bioretention_Assigned_Areas']
        lid_sub_19[4].unit_area = subbasin_attributes.at[19,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_20[0].unit_area = subbasin_attributes.at[20,'GreenRoof_Assigned_Areas']
        lid_sub_20[1].unit_area = subbasin_attributes.at[20,'PermeablePavement_Assigned_Areas']
        lid_sub_20[2].unit_area = subbasin_attributes.at[20,'RainGarden_Assigned_Areas']
        lid_sub_20[3].unit_area = subbasin_attributes.at[20,'Bioretention_Assigned_Areas']
        lid_sub_20[4].unit_area = subbasin_attributes.at[20,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_21[0].unit_area = subbasin_attributes.at[21,'GreenRoof_Assigned_Areas']
        lid_sub_21[1].unit_area = subbasin_attributes.at[21,'PermeablePavement_Assigned_Areas']
        lid_sub_21[2].unit_area = subbasin_attributes.at[21,'RainGarden_Assigned_Areas']
        lid_sub_21[3].unit_area = subbasin_attributes.at[21,'Bioretention_Assigned_Areas']
        lid_sub_21[4].unit_area = subbasin_attributes.at[21,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_22[0].unit_area = subbasin_attributes.at[22,'GreenRoof_Assigned_Areas']
        lid_sub_22[1].unit_area = subbasin_attributes.at[22,'PermeablePavement_Assigned_Areas']
        lid_sub_22[2].unit_area = subbasin_attributes.at[22,'RainGarden_Assigned_Areas']
        lid_sub_22[3].unit_area = subbasin_attributes.at[22,'Bioretention_Assigned_Areas']
        lid_sub_22[4].unit_area = subbasin_attributes.at[22,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_23[0].unit_area = subbasin_attributes.at[23,'GreenRoof_Assigned_Areas']
        lid_sub_23[1].unit_area = subbasin_attributes.at[23,'PermeablePavement_Assigned_Areas']
        lid_sub_23[2].unit_area = subbasin_attributes.at[23,'RainGarden_Assigned_Areas']
        lid_sub_23[3].unit_area = subbasin_attributes.at[23,'Bioretention_Assigned_Areas']
        lid_sub_23[4].unit_area = subbasin_attributes.at[23,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_24[0].unit_area = subbasin_attributes.at[24,'GreenRoof_Assigned_Areas']
        lid_sub_24[1].unit_area = subbasin_attributes.at[24,'PermeablePavement_Assigned_Areas']
        lid_sub_24[2].unit_area = subbasin_attributes.at[24,'RainGarden_Assigned_Areas']
        lid_sub_24[3].unit_area = subbasin_attributes.at[24,'Bioretention_Assigned_Areas']
        lid_sub_24[4].unit_area = subbasin_attributes.at[24,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_25[0].unit_area = subbasin_attributes.at[25,'GreenRoof_Assigned_Areas']
        lid_sub_25[1].unit_area = subbasin_attributes.at[25,'PermeablePavement_Assigned_Areas']
        lid_sub_25[2].unit_area = subbasin_attributes.at[25,'RainGarden_Assigned_Areas']
        lid_sub_25[3].unit_area = subbasin_attributes.at[25,'Bioretention_Assigned_Areas']
        lid_sub_25[4].unit_area = subbasin_attributes.at[25,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        lid_sub_26[0].unit_area = subbasin_attributes.at[26,'GreenRoof_Assigned_Areas']
        lid_sub_26[1].unit_area = subbasin_attributes.at[26,'PermeablePavement_Assigned_Areas']
        lid_sub_26[2].unit_area = subbasin_attributes.at[26,'RainGarden_Assigned_Areas']
        lid_sub_26[3].unit_area = subbasin_attributes.at[26,'Bioretention_Assigned_Areas']
        lid_sub_26[4].unit_area = subbasin_attributes.at[26,'GrassSwale_Assigned_Areas']                                                                                                                              
                                                                                                                                        
        #Set Impervious areas treated

        lid_sub_1[1].from_impervious = subbasin_attributes.at[1,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_1[2].from_impervious = subbasin_attributes.at[1,'RainGarden_%ImpArea_Treated'] 
        lid_sub_1[3].from_impervious = subbasin_attributes.at[1,'Bioretention_%ImpArea_Treated'] 
        lid_sub_1[4].from_impervious = subbasin_attributes.at[1,'GrassSwale_%ImpArea_Treated']                                                                                                                               
                                                                                                                                        
        lid_sub_2[1].from_impervious = subbasin_attributes.at[2,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_2[2].from_impervious = subbasin_attributes.at[2,'RainGarden_%ImpArea_Treated'] 
        lid_sub_2[3].from_impervious = subbasin_attributes.at[2,'Bioretention_%ImpArea_Treated'] 
        lid_sub_2[4].from_impervious = subbasin_attributes.at[2,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                    
        lid_sub_3[1].from_impervious = subbasin_attributes.at[3,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_3[2].from_impervious = subbasin_attributes.at[3,'RainGarden_%ImpArea_Treated'] 
        lid_sub_3[3].from_impervious = subbasin_attributes.at[3,'Bioretention_%ImpArea_Treated'] 
        lid_sub_3[4].from_impervious = subbasin_attributes.at[3,'GrassSwale_%ImpArea_Treated']
                                                                                                                                        
        lid_sub_4[1].from_impervious = subbasin_attributes.at[4,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_4[2].from_impervious = subbasin_attributes.at[4,'RainGarden_%ImpArea_Treated'] 
        lid_sub_4[3].from_impervious = subbasin_attributes.at[4,'Bioretention_%ImpArea_Treated'] 
        lid_sub_4[4].from_impervious = subbasin_attributes.at[4,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_5[1].from_impervious = subbasin_attributes.at[5,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_5[2].from_impervious = subbasin_attributes.at[5,'RainGarden_%ImpArea_Treated'] 
        lid_sub_5[3].from_impervious = subbasin_attributes.at[5,'Bioretention_%ImpArea_Treated'] 
        lid_sub_5[4].from_impervious = subbasin_attributes.at[5,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_6[1].from_impervious = subbasin_attributes.at[6,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_6[2].from_impervious = subbasin_attributes.at[6,'RainGarden_%ImpArea_Treated'] 
        lid_sub_6[3].from_impervious = subbasin_attributes.at[6,'Bioretention_%ImpArea_Treated'] 
        lid_sub_6[4].from_impervious = subbasin_attributes.at[6,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_7[1].from_impervious = subbasin_attributes.at[7,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_7[2].from_impervious = subbasin_attributes.at[7,'RainGarden_%ImpArea_Treated'] 
        lid_sub_7[3].from_impervious = subbasin_attributes.at[7,'Bioretention_%ImpArea_Treated'] 
        lid_sub_7[4].from_impervious = subbasin_attributes.at[7,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_8[1].from_impervious = subbasin_attributes.at[8,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_8[2].from_impervious = subbasin_attributes.at[8,'RainGarden_%ImpArea_Treated'] 
        lid_sub_8[3].from_impervious = subbasin_attributes.at[8,'Bioretention_%ImpArea_Treated'] 
        lid_sub_8[4].from_impervious = subbasin_attributes.at[8,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_9[1].from_impervious = subbasin_attributes.at[9,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_9[2].from_impervious = subbasin_attributes.at[9,'RainGarden_%ImpArea_Treated'] 
        lid_sub_9[3].from_impervious = subbasin_attributes.at[9,'Bioretention_%ImpArea_Treated'] 
        lid_sub_9[4].from_impervious = subbasin_attributes.at[9,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_10[1].from_impervious = subbasin_attributes.at[10,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_10[2].from_impervious = subbasin_attributes.at[10,'RainGarden_%ImpArea_Treated'] 
        lid_sub_10[3].from_impervious = subbasin_attributes.at[10,'Bioretention_%ImpArea_Treated'] 
        lid_sub_10[4].from_impervious = subbasin_attributes.at[10,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_11[1].from_impervious = subbasin_attributes.at[11,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_11[2].from_impervious = subbasin_attributes.at[11,'RainGarden_%ImpArea_Treated'] 
        lid_sub_11[3].from_impervious = subbasin_attributes.at[11,'Bioretention_%ImpArea_Treated'] 
        lid_sub_11[4].from_impervious = subbasin_attributes.at[11,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_12[1].from_impervious = subbasin_attributes.at[12,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_12[2].from_impervious = subbasin_attributes.at[12,'RainGarden_%ImpArea_Treated'] 
        lid_sub_12[3].from_impervious = subbasin_attributes.at[12,'Bioretention_%ImpArea_Treated'] 
        lid_sub_12[4].from_impervious = subbasin_attributes.at[12,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_13[1].from_impervious = subbasin_attributes.at[13,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_13[2].from_impervious = subbasin_attributes.at[13,'RainGarden_%ImpArea_Treated'] 
        lid_sub_13[3].from_impervious = subbasin_attributes.at[13,'Bioretention_%ImpArea_Treated'] 
        lid_sub_13[4].from_impervious = subbasin_attributes.at[13,'GrassSwale_%ImpArea_Treated']                                                                                                                                                                                                                               
                                                                                                                                        
        lid_sub_14[1].from_impervious = subbasin_attributes.at[14,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_14[2].from_impervious = subbasin_attributes.at[14,'RainGarden_%ImpArea_Treated'] 
        lid_sub_14[3].from_impervious = subbasin_attributes.at[14,'Bioretention_%ImpArea_Treated'] 
        lid_sub_14[4].from_impervious = subbasin_attributes.at[14,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_15[1].from_impervious = subbasin_attributes.at[15,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_15[2].from_impervious = subbasin_attributes.at[15,'RainGarden_%ImpArea_Treated'] 
        lid_sub_15[3].from_impervious = subbasin_attributes.at[15,'Bioretention_%ImpArea_Treated'] 
        lid_sub_15[4].from_impervious = subbasin_attributes.at[15,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_16[1].from_impervious = subbasin_attributes.at[16,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_16[2].from_impervious = subbasin_attributes.at[16,'RainGarden_%ImpArea_Treated'] 
        lid_sub_16[3].from_impervious = subbasin_attributes.at[16,'Bioretention_%ImpArea_Treated'] 
        lid_sub_16[4].from_impervious = subbasin_attributes.at[16,'GrassSwale_%ImpArea_Treated']                                                                                                                               
                                                                                                                                        
        lid_sub_17[1].from_impervious = subbasin_attributes.at[17,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_17[2].from_impervious = subbasin_attributes.at[17,'RainGarden_%ImpArea_Treated'] 
        lid_sub_17[3].from_impervious = subbasin_attributes.at[17,'Bioretention_%ImpArea_Treated'] 
        lid_sub_17[4].from_impervious = subbasin_attributes.at[17,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_18[1].from_impervious = subbasin_attributes.at[18,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_18[2].from_impervious = subbasin_attributes.at[18,'RainGarden_%ImpArea_Treated'] 
        lid_sub_18[3].from_impervious = subbasin_attributes.at[18,'Bioretention_%ImpArea_Treated'] 
        lid_sub_18[4].from_impervious = subbasin_attributes.at[18,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_19[1].from_impervious = subbasin_attributes.at[19,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_19[2].from_impervious = subbasin_attributes.at[19,'RainGarden_%ImpArea_Treated'] 
        lid_sub_19[3].from_impervious = subbasin_attributes.at[19,'Bioretention_%ImpArea_Treated'] 
        lid_sub_19[4].from_impervious = subbasin_attributes.at[19,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_20[1].from_impervious = subbasin_attributes.at[20,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_20[2].from_impervious = subbasin_attributes.at[20,'RainGarden_%ImpArea_Treated'] 
        lid_sub_20[3].from_impervious = subbasin_attributes.at[20,'Bioretention_%ImpArea_Treated'] 
        lid_sub_20[4].from_impervious = subbasin_attributes.at[20,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_21[1].from_impervious = subbasin_attributes.at[21,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_21[2].from_impervious = subbasin_attributes.at[21,'RainGarden_%ImpArea_Treated'] 
        lid_sub_21[3].from_impervious = subbasin_attributes.at[21,'Bioretention_%ImpArea_Treated'] 
        lid_sub_21[4].from_impervious = subbasin_attributes.at[21,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_22[1].from_impervious = subbasin_attributes.at[22,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_22[2].from_impervious = subbasin_attributes.at[22,'RainGarden_%ImpArea_Treated'] 
        lid_sub_22[3].from_impervious = subbasin_attributes.at[22,'Bioretention_%ImpArea_Treated'] 
        lid_sub_22[4].from_impervious = subbasin_attributes.at[22,'GrassSwale_%ImpArea_Treated']
                                                                                                                                        
        lid_sub_23[1].from_impervious = subbasin_attributes.at[23,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_23[2].from_impervious = subbasin_attributes.at[23,'RainGarden_%ImpArea_Treated'] 
        lid_sub_23[3].from_impervious = subbasin_attributes.at[23,'Bioretention_%ImpArea_Treated'] 
        lid_sub_23[4].from_impervious = subbasin_attributes.at[23,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_24[1].from_impervious = subbasin_attributes.at[24,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_24[2].from_impervious = subbasin_attributes.at[24,'RainGarden_%ImpArea_Treated'] 
        lid_sub_24[3].from_impervious = subbasin_attributes.at[24,'Bioretention_%ImpArea_Treated'] 
        lid_sub_24[4].from_impervious = subbasin_attributes.at[24,'GrassSwale_%ImpArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_25[1].from_impervious = subbasin_attributes.at[25,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_25[2].from_impervious = subbasin_attributes.at[25,'RainGarden_%ImpArea_Treated'] 
        lid_sub_25[3].from_impervious = subbasin_attributes.at[25,'Bioretention_%ImpArea_Treated'] 
        lid_sub_25[4].from_impervious = subbasin_attributes.at[25,'GrassSwale_%ImpArea_Treated']  

        lid_sub_26[1].from_impervious = subbasin_attributes.at[26,'PermeablePavement_%ImpArea_Treated'] 
        lid_sub_26[2].from_impervious = subbasin_attributes.at[26,'RainGarden_%ImpArea_Treated'] 
        lid_sub_26[3].from_impervious = subbasin_attributes.at[26,'Bioretention_%ImpArea_Treated'] 
        lid_sub_26[4].from_impervious = subbasin_attributes.at[26,'GrassSwale_%ImpArea_Treated']                                                                                                                             
                                                                                                                                        


    #Set pervious area treated

        lid_sub_1[2].from_pervious = subbasin_attributes.at[1,'RainGarden_%PervArea_Treated']  
        lid_sub_1[3].from_pervious = subbasin_attributes.at[1,'Bioretention_%PervArea_Treated']  
        lid_sub_1[4].from_pervious = subbasin_attributes.at[1,'GrassSwale_%PervArea_Treated']
                                                                                                                                        
        lid_sub_2[2].from_pervious = subbasin_attributes.at[2,'RainGarden_%PervArea_Treated']  
        lid_sub_2[3].from_pervious = subbasin_attributes.at[2,'Bioretention_%PervArea_Treated']  
        lid_sub_2[4].from_pervious = subbasin_attributes.at[2,'GrassSwale_%PervArea_Treated']                                                                                                                              
                                                                                                                                        
        lid_sub_3[2].from_pervious = subbasin_attributes.at[3,'RainGarden_%PervArea_Treated']  
        lid_sub_3[3].from_pervious = subbasin_attributes.at[3,'Bioretention_%PervArea_Treated']  
        lid_sub_3[4].from_pervious = subbasin_attributes.at[3,'GrassSwale_%PervArea_Treated']                                                                                                                              
                                                                                                                
        lid_sub_4[2].from_pervious = subbasin_attributes.at[4,'RainGarden_%PervArea_Treated']  
        lid_sub_4[3].from_pervious = subbasin_attributes.at[4,'Bioretention_%PervArea_Treated']  
        lid_sub_4[4].from_pervious = subbasin_attributes.at[4,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_5[2].from_pervious = subbasin_attributes.at[5,'RainGarden_%PervArea_Treated']  
        lid_sub_5[3].from_pervious = subbasin_attributes.at[5,'Bioretention_%PervArea_Treated']  
        lid_sub_5[4].from_pervious = subbasin_attributes.at[5,'GrassSwale_%PervArea_Treated']                                                                                                                                
        
        lid_sub_6[2].from_pervious = subbasin_attributes.at[6,'RainGarden_%PervArea_Treated']  
        lid_sub_6[3].from_pervious = subbasin_attributes.at[6,'Bioretention_%PervArea_Treated']  
        lid_sub_6[4].from_pervious = subbasin_attributes.at[6,'GrassSwale_%PervArea_Treated'] 
        
        lid_sub_7[2].from_pervious = subbasin_attributes.at[7,'RainGarden_%PervArea_Treated']  
        lid_sub_7[3].from_pervious = subbasin_attributes.at[7,'Bioretention_%PervArea_Treated']  
        lid_sub_7[4].from_pervious = subbasin_attributes.at[7,'GrassSwale_%PervArea_Treated']
                                                                                                                                        
        lid_sub_8[2].from_pervious = subbasin_attributes.at[8,'RainGarden_%PervArea_Treated']  
        lid_sub_8[3].from_pervious = subbasin_attributes.at[8,'Bioretention_%PervArea_Treated']  
        lid_sub_8[4].from_pervious = subbasin_attributes.at[8,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_9[2].from_pervious = subbasin_attributes.at[9,'RainGarden_%PervArea_Treated']  
        lid_sub_9[3].from_pervious = subbasin_attributes.at[9,'Bioretention_%PervArea_Treated']  
        lid_sub_9[4].from_pervious = subbasin_attributes.at[9,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                
        lid_sub_10[2].from_pervious = subbasin_attributes.at[10,'RainGarden_%PervArea_Treated']  
        lid_sub_10[3].from_pervious = subbasin_attributes.at[10,'Bioretention_%PervArea_Treated']  
        lid_sub_10[4].from_pervious = subbasin_attributes.at[10,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_11[2].from_pervious = subbasin_attributes.at[11,'RainGarden_%PervArea_Treated']  
        lid_sub_11[3].from_pervious = subbasin_attributes.at[11,'Bioretention_%PervArea_Treated']  
        lid_sub_11[4].from_pervious = subbasin_attributes.at[11,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_12[2].from_pervious = subbasin_attributes.at[12,'RainGarden_%PervArea_Treated']  
        lid_sub_12[3].from_pervious = subbasin_attributes.at[12,'Bioretention_%PervArea_Treated']  
        lid_sub_12[4].from_pervious = subbasin_attributes.at[12,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_13[2].from_pervious = subbasin_attributes.at[13,'RainGarden_%PervArea_Treated']  
        lid_sub_13[3].from_pervious = subbasin_attributes.at[13,'Bioretention_%PervArea_Treated']  
        lid_sub_13[4].from_pervious = subbasin_attributes.at[13,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_14[2].from_pervious = subbasin_attributes.at[14,'RainGarden_%PervArea_Treated']  
        lid_sub_14[3].from_pervious = subbasin_attributes.at[14,'Bioretention_%PervArea_Treated']  
        lid_sub_14[4].from_pervious = subbasin_attributes.at[14,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_15[2].from_pervious = subbasin_attributes.at[15,'RainGarden_%PervArea_Treated']  
        lid_sub_15[3].from_pervious = subbasin_attributes.at[15,'Bioretention_%PervArea_Treated']  
        lid_sub_15[4].from_pervious = subbasin_attributes.at[15,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_16[2].from_pervious = subbasin_attributes.at[16,'RainGarden_%PervArea_Treated']  
        lid_sub_16[3].from_pervious = subbasin_attributes.at[16,'Bioretention_%PervArea_Treated']  
        lid_sub_16[4].from_pervious = subbasin_attributes.at[16,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_17[2].from_pervious = subbasin_attributes.at[17,'RainGarden_%PervArea_Treated']  
        lid_sub_17[3].from_pervious = subbasin_attributes.at[17,'Bioretention_%PervArea_Treated']  
        lid_sub_17[4].from_pervious = subbasin_attributes.at[17,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_18[2].from_pervious = subbasin_attributes.at[18,'RainGarden_%PervArea_Treated']  
        lid_sub_18[3].from_pervious = subbasin_attributes.at[18,'Bioretention_%PervArea_Treated']  
        lid_sub_18[4].from_pervious = subbasin_attributes.at[18,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_19[2].from_pervious = subbasin_attributes.at[19,'RainGarden_%PervArea_Treated']  
        lid_sub_19[3].from_pervious = subbasin_attributes.at[19,'Bioretention_%PervArea_Treated']  
        lid_sub_19[4].from_pervious = subbasin_attributes.at[19,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_20[2].from_pervious = subbasin_attributes.at[20,'RainGarden_%PervArea_Treated']  
        lid_sub_20[3].from_pervious = subbasin_attributes.at[20,'Bioretention_%PervArea_Treated']  
        lid_sub_20[4].from_pervious = subbasin_attributes.at[20,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_21[2].from_pervious = subbasin_attributes.at[21,'RainGarden_%PervArea_Treated']  
        lid_sub_21[3].from_pervious = subbasin_attributes.at[21,'Bioretention_%PervArea_Treated']  
        lid_sub_21[4].from_pervious = subbasin_attributes.at[21,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_22[2].from_pervious = subbasin_attributes.at[22,'RainGarden_%PervArea_Treated']  
        lid_sub_22[3].from_pervious = subbasin_attributes.at[22,'Bioretention_%PervArea_Treated']  
        lid_sub_22[4].from_pervious = subbasin_attributes.at[22,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_23[2].from_pervious = subbasin_attributes.at[23,'RainGarden_%PervArea_Treated']  
        lid_sub_23[3].from_pervious = subbasin_attributes.at[23,'Bioretention_%PervArea_Treated']  
        lid_sub_23[4].from_pervious = subbasin_attributes.at[23,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_24[2].from_pervious = subbasin_attributes.at[24,'RainGarden_%PervArea_Treated']  
        lid_sub_24[3].from_pervious = subbasin_attributes.at[24,'Bioretention_%PervArea_Treated']  
        lid_sub_24[4].from_pervious = subbasin_attributes.at[24,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_25[2].from_pervious = subbasin_attributes.at[25,'RainGarden_%PervArea_Treated']  
        lid_sub_25[3].from_pervious = subbasin_attributes.at[25,'Bioretention_%PervArea_Treated']  
        lid_sub_25[4].from_pervious = subbasin_attributes.at[25,'GrassSwale_%PervArea_Treated']                                                                                                                                
                                                                                                                                        
        lid_sub_26[2].from_pervious = subbasin_attributes.at[26,'RainGarden_%PervArea_Treated']  
        lid_sub_26[3].from_pervious = subbasin_attributes.at[26,'Bioretention_%PervArea_Treated']  
        lid_sub_26[4].from_pervious = subbasin_attributes.at[26,'GrassSwale_%PervArea_Treated']                                                                                                                                
        
        #Set Swale Widths


        lid_sub_1[4].full_width = subbasin_attributes.at[1,'GrassSwale_Widths']                                                                                                                                                                                                                                                                                                                                                                     
        lid_sub_2[4].full_width = subbasin_attributes.at[2,'GrassSwale_Widths']
        lid_sub_3[4].full_width = subbasin_attributes.at[3,'GrassSwale_Widths']                                                                                                                                                                                                                            
        lid_sub_4[4].full_width = subbasin_attributes.at[4,'GrassSwale_Widths']                                                                                                                                                                                                                                                               
        lid_sub_5[4].full_width = subbasin_attributes.at[5,'GrassSwale_Widths']                                                                                                                             
        lid_sub_6[4].full_width = subbasin_attributes.at[6,'GrassSwale_Widths']
        lid_sub_7[4].full_width = subbasin_attributes.at[7,'GrassSwale_Widths']
        lid_sub_8[4].full_width = subbasin_attributes.at[8,'GrassSwale_Widths']                                                                                                                                                                                                                                                              
        lid_sub_9[4].full_width = subbasin_attributes.at[9,'GrassSwale_Widths']                                                                                                                                                                                                                                                    
        lid_sub_10[4].full_width = subbasin_attributes.at[10,'GrassSwale_Widths']                                                                                                                                                                                                                                                         
        lid_sub_11[4].full_width = subbasin_attributes.at[11,'GrassSwale_Widths']                                                                                                                                                                                                                                                      
        lid_sub_12[4].full_width = subbasin_attributes.at[12,'GrassSwale_Widths']                                                                                                                                                                                                                                                             
        lid_sub_13[4].full_width = subbasin_attributes.at[13,'GrassSwale_Widths']                                                                                                                                                                                                                                                          
        lid_sub_14[4].full_width = subbasin_attributes.at[14,'GrassSwale_Widths']                                                                                                                                                                                                                                                         
        lid_sub_15[4].full_width = subbasin_attributes.at[15,'GrassSwale_Widths']                                                                                                                           
        lid_sub_16[4].full_width = subbasin_attributes.at[16,'GrassSwale_Widths']                                                                                                                             
        lid_sub_17[4].full_width = subbasin_attributes.at[17,'GrassSwale_Widths']                                                                                                                          
        lid_sub_18[4].full_width = subbasin_attributes.at[18,'GrassSwale_Widths']                                                                                                                                                                                                                                                          
        lid_sub_19[4].full_width = subbasin_attributes.at[19,'GrassSwale_Widths']                                                                                                                              
        lid_sub_20[4].full_width = subbasin_attributes.at[20,'GrassSwale_Widths']                                                                                                                                                                                                                                                           
        lid_sub_21[4].full_width = subbasin_attributes.at[21,'GrassSwale_Widths']                                                                                                                              
        lid_sub_22[4].full_width = subbasin_attributes.at[22,'GrassSwale_Widths']                                                                                                                            
        lid_sub_23[4].full_width = subbasin_attributes.at[23,'GrassSwale_Widths']                                                                                                                            
        lid_sub_24[4].full_width = subbasin_attributes.at[24,'GrassSwale_Widths']                                                                                                                                                                                                                                                              
        lid_sub_25[4].full_width = subbasin_attributes.at[25,'GrassSwale_Widths']                                                                                                                              
        lid_sub_26[4].full_width = subbasin_attributes.at[26,'GrassSwale_Widths']                                                                                                                            
                                                                                                            
                                                                                                                                        
        #Run the simulation
        for step in sim:
            pass
        sim.report()
        sim.close()


# _________________Get average peak flow across 10 stream reaches_____________________________________________________________

    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43811 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =31186, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43811.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43811['Flow over 10'] = rpt_43811['Flow over 10'].fillna(0)
    rpt_43811['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43811.index:
        j = rpt_43811.at[t,'Flow over 10'] * rpt_43811.at[t,'Flow under 10']
        if j == 0:
            rpt_43811.at[t,'Flow (CFS)'] = rpt_43811.at[t,'Flow under 10']
        else:
            rpt_43811.at[t,'Flow (CFS)'] = rpt_43811.at[t,'Flow over 10']

    x1 = rpt_43811['Flow (CFS)'].max()

    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43771 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =31035, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43771.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43771['Flow over 10'] = rpt_43771['Flow over 10'].fillna(0)
    rpt_43771['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43771.index:
        j = rpt_43771.at[t,'Flow over 10'] * rpt_43771.at[t,'Flow under 10']
        if j == 0:
            rpt_43771.at[t,'Flow (CFS)'] = rpt_43771.at[t,'Flow under 10']
        else:
            rpt_43771.at[t,'Flow (CFS)'] = rpt_43771.at[t,'Flow over 10']

    x2 = rpt_43771['Flow (CFS)'].max()


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43631 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =30431, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43631.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43631['Flow over 10'] = rpt_43631['Flow over 10'].fillna(0)
    rpt_43631['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43631.index:
        j = rpt_43631.at[t,'Flow over 10'] * rpt_43631.at[t,'Flow under 10']
        if j == 0:
            rpt_43631.at[t,'Flow (CFS)'] = rpt_43631.at[t,'Flow under 10']
        else:
            rpt_43631.at[t,'Flow (CFS)'] = rpt_43631.at[t,'Flow over 10']

    x3 = rpt_43631['Flow (CFS)'].max()


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43581 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =30129, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43581.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43581['Flow over 10'] = rpt_43581['Flow over 10'].fillna(0)
    rpt_43581['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43581.index:
        j = rpt_43581.at[t,'Flow over 10'] * rpt_43581.at[t,'Flow under 10']
        if j == 0:
            rpt_43581.at[t,'Flow (CFS)'] = rpt_43581.at[t,'Flow under 10']
        else:
            rpt_43581.at[t,'Flow (CFS)'] = rpt_43581.at[t,'Flow over 10']

    x4 = rpt_43581['Flow (CFS)'].max()


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43481 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows = 29525, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python') 
    rpt_43481.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43481['Flow over 10'] = rpt_43481['Flow over 10'].fillna(0)
    rpt_43481['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43481.index:
        j = rpt_43481.at[t,'Flow over 10'] * rpt_43481.at[t,'Flow under 10']
        if j == 0:
            rpt_43481.at[t,'Flow (CFS)'] = rpt_43481.at[t,'Flow under 10']
        else:
            rpt_43481.at[t,'Flow (CFS)'] = rpt_43481.at[t,'Flow over 10']

    x5 = rpt_43481['Flow (CFS)'].max()


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43391 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =28921, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43391.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43391['Flow over 10'] = rpt_43391['Flow over 10'].fillna(0)
    rpt_43391['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43391.index:
        j = rpt_43391.at[t,'Flow over 10'] * rpt_43391.at[t,'Flow under 10']
        if j == 0:
            rpt_43391.at[t,'Flow (CFS)'] = rpt_43391.at[t,'Flow under 10']
        else:
            rpt_43391.at[t,'Flow (CFS)'] = rpt_43391.at[t,'Flow over 10']

    x6 = rpt_43391['Flow (CFS)'].max()


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43301 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =28317, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43301.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43301['Flow over 10'] = rpt_43301['Flow over 10'].fillna(0)
    rpt_43301['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43301.index:
        j = rpt_43301.at[t,'Flow over 10'] * rpt_43301.at[t,'Flow under 10']
        if j == 0:
            rpt_43301.at[t,'Flow (CFS)'] = rpt_43301.at[t,'Flow under 10']
        else:
            rpt_43301.at[t,'Flow (CFS)'] = rpt_43301.at[t,'Flow over 10']

    x7 = rpt_43301['Flow (CFS)'].max()


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43241 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =28166, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43241.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43241['Flow over 10'] = rpt_43241['Flow over 10'].fillna(0)
    rpt_43241['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43241.index:
        j = rpt_43241.at[t,'Flow over 10'] * rpt_43241.at[t,'Flow under 10']
        if j == 0:
            rpt_43241.at[t,'Flow (CFS)'] = rpt_43241.at[t,'Flow under 10']
        else:
            rpt_43241.at[t,'Flow (CFS)'] = rpt_43241.at[t,'Flow over 10']

    x8 = rpt_43241['Flow (CFS)'].max()

    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43201 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =27562, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_43201.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43201['Flow over 10'] = rpt_43201['Flow over 10'].fillna(0)
    rpt_43201['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43201.index:
        j = rpt_43201.at[t,'Flow over 10'] * rpt_43201.at[t,'Flow under 10']
        if j == 0:
            rpt_43201.at[t,'Flow (CFS)'] = rpt_43201.at[t,'Flow under 10']
        else:
            rpt_43201.at[t,'Flow (CFS)'] = rpt_43201.at[t,'Flow over 10']

    x9 = rpt_43201['Flow (CFS)'].max()


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_42831 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =26203, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')    
    rpt_42831.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_42831['Flow over 10'] = rpt_42831['Flow over 10'].fillna(0)
    rpt_42831['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_42831.index:
        j = rpt_42831.at[t,'Flow over 10'] * rpt_42831.at[t,'Flow under 10']
        if j == 0:
            rpt_42831.at[t,'Flow (CFS)'] = rpt_42831.at[t,'Flow under 10']
        else:
            rpt_42831.at[t,'Flow (CFS)'] = rpt_42831.at[t,'Flow over 10']

    x10 = rpt_42831['Flow (CFS)'].max()



    peak_flow_avg = (x1+x2+x3+x4+x5+x6+x7+x8+x9+x10)/10
        
 # _________  # Get Total Runoff Score


    reportColumns = [str(i) for i in np.arange(0,8)]
    rpt_43811 = pd.read_csv(pyswmm_results_txt_folder+output_text_file, skiprows =31186, nrows = 144, sep="   |    ", names = reportColumns, header = None, engine = 'python')
    rpt_43811.rename(columns = {'0':'Date Time','1':'Flow over 10','2':'Flow under 10','3':'Velocity (ft/s)','4':'Depth (ft)','5':'Capacity Setting','6':'Total Nitrogen Load (lbs)','7':'Total Phosphorous Load (lbs)'},inplace = True)
    rpt_43811['Flow over 10'] = rpt_43811['Flow over 10'].fillna(0)
    rpt_43811['Flow (CFS)'] = ""

    #Build flow Column with 10 and over 10 CFS values
    for t in rpt_43811.index:
        j = rpt_43811.at[t,'Flow over 10'] * rpt_43811.at[t,'Flow under 10']
        if j == 0:
            rpt_43811.at[t,'Flow (CFS)'] = rpt_43811.at[t,'Flow under 10']
        else:
            rpt_43811.at[t,'Flow (CFS)'] = rpt_43811.at[t,'Flow over 10']

    rpt_43811['Total Flow (CF)'] = ""

    for t in rpt_43811.index:
        rpt_43811.at[t,'Total Flow (CF)'] = rpt_43811.at[t,'Flow (CFS)'] *60*15

    total_flow = (rpt_43811['Total Flow (CF)'].sum())


    objs[0] = correlation
    objs[1] = peak_flow_avg
    objs[2] = total_flow  

    # print(peakflow_SEI_corr)
    # print(totalflow_SEI_corr)
    print(correlation)
    print(peak_flow_avg)
    print(total_flow)
    print(cost_check)


    os.remove(pyswmm_results_txt_folder+output_text_file)
    os.remove(swmmio_altered_inp_file_name+altered_SWMMIO_inp)
    os.remove(swmmio_altered_inp_file_name+altered_SWMMIO_out)
    os.remove(r"/sfs/lustre/bahamut/scratch/rsh6pb/C/Borg/Borg-1.8/temp_export_file_"+random_number+".csv")



    constrs[0] = max(0,(cost_check - upper_cost_limit))
    constrs[1] = max(0,(lower_cost_limit - cost_check))

    
    
    return (objs,constrs)


from borg import *

Configuration.startMPI()

borg = Borg(nvars, nobjs, nconstrs, pySWMMio)
borg.setBounds(*[[0, 1]]*nvars)
borg.setEpsilons(0.01,0.1,10)


result = borg.solveMPI(maxEvaluations=150000,runtime='mpi_pySWMMio_35-40Mil_HE_epsilon.runtime', frequency = 1500)


if result:

               # Create/write objective values and decision variable values to files in folder "sets", 1 file per seed.
    f = open('mpi_pySWMMio_35-40Mil_HE_epsilon.set', 'w')
    for solution in result:
        line = ''
        for v in solution.getVariables():
            line += str(v) + ' '
        for o in solution.getObjectives():
            line += str(o) + ' '
        f.write(line[:-1] + '\n')
    f.write('#')
    f.close()

#_____Print nondominated decision variables and objective values___
    all_raw_optimal_decision_lists = []
    all_raw_optimal_objective_values = []

    for solution in result:

        all_raw_optimal_decision_lists.append(solution.getVariables())
        all_raw_optimal_objective_values.append(solution.getObjectives())
        print(solution.getObjectives())
        print(solution.getVariables())

    print(all_raw_optimal_decision_lists)
    print(all_raw_optimal_objective_values)

Configuration.stopMPI()


