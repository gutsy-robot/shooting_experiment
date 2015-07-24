# DMP Simulation for Gabriel
# HEADER

## @file        	dmp_simulation.py
#  @brief           This test project generates joint trajectories for the taskspace trajectories generated by DMP
#  @author      	Nima Ramezani Taghiabadi
#
#               	PhD Researcher 
#               	Faculty of Engineering and Information Technology 
#               	University of Technology Sydney (UTS) 
#               	Broadway, Ultimo, NSW 2007, Australia 
#               	Phone No. : 04 5027 4611 
#               	Email(1)  : nima.ramezani@gmail.com 
#               	Email(2)  : Nima.RamezaniTaghiabadi@uts.edu.au 
#  @version     	1.0
#
#  Last Revision:  	25 June 2015

# BODY

# Load required libraries from S-PR2:
import scipy.io   # Required for reading Matlab workspace file
import numpy as np

from magiks.specific_geometries.pr2 import pr2_arm_kinematics as armlib
from math_tools.geometry import geometry as geo, trajectory as traj


def read_trajectory():
# Read Matlab Workspace File:
    data_file = "pr2_trajectory_data_v2.mat"
    workspace = scipy.io.loadmat(data_file)
    p       = workspace['p']         
    q       = workspace['q']
    N       = len(p)
    assert N == len(q)

    ## Create a position and orientation trajectory from given data:

    pt = traj.Trajectory_Polynomial(capacity = 5)
    ot = traj.Orientation_Trajectory_Polynomial()

    t  = 0.0
    dt = 0.005

    for i in range(N):
        pos = p[i, :]
        ori = q[i, :]
        # pos = np.array(pos[0], [pos[1], pos[2]])
        pt.add_point(t, pos = pos)
        ot.add_point(t, ori = geo.Orientation_3D(ori, representation = 'quaternion'))
        t   = t + dt

    ot.consistent_velocities()
    pt.consistent_velocities()

    return (pt, ot)

def project_trajectory(pt, ot):

    ## First create an instance of PR2 Arm:
    arm = armlib.PR2_ARM()
    # Take the manipulator to the start point of the trajectory:
    pt.set_phi(0.0)
    ot.set_phi(0.0)
    arm.set_target(pt.current_position, ot.current_orientation.matrix())
    arm.inverse_update(optimize = True, show = False)
    # Project the trajectory into the joint-space:
    arm.max_js = 1.0
    arm.max_ja = 100.0
    arm.max_jj = 3000.0
    jt  = arm.js_project(pos_traj = pt, ori_traj = ot, relative = False, traj_capacity = 20)
    # Match velocities at segment borders and interpolate:
    # jt.consistent_velocities()
    # Your trajectory is now ready to be issued :-)
    return jt

def regen_task_traj(jt):
    arm = armlib.PR2_ARM()
    (pt, ot) = arm.ts_project(jt)
    return (pt, ot)

def write_trajectory(csv_file_name, tr):
    path = 'home/Dropbox/software/python/magiks/projects/s_pr2/'
    tr.write_csv(filename = csv_file_name, path = path, n = 10000)

'''
(pt, ot) = read_trajectory()
jt       = project_trajectory(pt, ot)
write_trajectory('joint_traj.csv',jt)
'''
