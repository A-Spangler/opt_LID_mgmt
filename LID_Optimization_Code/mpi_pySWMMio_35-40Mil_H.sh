#!/bin/bash
#SBATCH -D /scratch/rsh6pb/C/Borg/Borg-1.8		# working directory
#SBATCH -o /scratch/rsh6pb/C/Borg/Borg-1.8/job.%j.%N.out   # Name of the output file (eg. myMPI.oJobID)
#SBATCH -N 3          					# Total number of nodes to request
#SBATCH --ntasks-per-node 20           		# Number of processors per node
#SBATCH -p parallel
#SBATCH -A culvergroup       					# allocation name
#SBATCH -t 72:00:00       					# Run time (hh:mm:ss) - up to 36 hours
##SBATCH --mail-user=rsh6pb@virginia.edu     # address for email notification
##SBATCH --mail-type=ALL                  	# email at Begin and End of job

module purge
#module load goolf/9.2.0_3.1.6 python
module load gcc/9.2.0  openmpi/3.1.6 python

#module load gcc/9.2.0  openmpi/3.1.6 anaconda


# Your commands go here
which python
export OMP_NUM_THREADS=1
mpirun python mpi_pySWMMio_35-40Mil_H.py
