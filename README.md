# Basic Overview
The Optimal-Equitable-LID-Mgt repository contains python code that was developed at the University of Virginia and parallelized to run on linux clusters using an open-source tool called Slurm. Please see the University of Virginia High Performance Computing website to learn more about how parallel code is executed using Slurm at URL: https://www.rc.virginia.edu/userinfo/rivanna/slurm/. The code was developed to explore the impacts of integrating a social equity objective into a low impact development (LID) optimization model and to explore the potential tradeoffs and synergies between near Pareto-optimal solutions under different formulations. We use the Borg python wrapper to implement the Borg multi-objective evolutionary algorithm within our SWMM model. Python libaries included in the python files must be installed and Borg must be compiled before running the code found in the "LID_Optimization_Code" folder. You can visit the Borg website at URL: http://borgmoea.org/ for more information on how to use Borg.

 # Using the Model
 The code for three different formulations can be found in the folder titled "LID_Optimization_Code". The .py files contain the code for the coupled SWMM(Stormwater management mode)-Borg model.The .sh files are batch files used to execute the .py files.

The other folders will be necessary to execute the python code as they temporarily input and result data files that appear in the code.

The folders titled "SWMM_Model" and "Subbasin_attributes" contain example data for the Upper Meadow Creek Watershed located in Charlottesville and Albemarle County Virginia. 
 



  
