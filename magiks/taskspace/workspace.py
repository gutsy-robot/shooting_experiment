# BODY
## @file:           workspace.py
#  @brief:    	    This module provides a class containing methods and properties regarding the workspace of a manipulator.
#                   with their associated poses. 
#  @author      	Nima Ramezani Taghiabadi 
#
#               	PhD Researcher 
#               	Faculty of Engineering and Information Technology 
#               	University of Technology Sydney (UTS) 
#               	Broadway, Ultimo, NSW 2007, Australia 
#               	Phone No. :   04 5027 4611 
#               	Email(1)  : nima.ramezani@gmail.com 
#               	Email(2)  : Nima.RamezaniTaghiabadi@uts.edu.au 
#  @version     	2.0
# 
#  Last Revision:  	11 January 2015

import  numpy,copy, pickle

import  general_python as genpy
import  magiks.taskspace.endeffector as endlib
from    math_tools.geometry import rotation
from    packages.matej.artificial_intelligence.data_mining.kdtree import kdtree

## Use this function to load the workspace from a file. 
#  @param path_and_file_name A string specifying the full path and filename containing the workspace data
#  @return An instance of class packages.nima.robotics.kinematics.task_space.workspace.Workspace()
def read_from_file(path_and_file_name):
    FILE_DATA = open(path_and_file_name, "r")
    work_space = pickle.load(FILE_DATA)
    return work_space

'''
key_dic = {
    'NA'            : 'Not Applicable',

    # Forward: 
    'RND'           : 'Random',
    'JSG'           : 'Joint Space Grid',
    'PCL'           : 'Predefined Config List',
    'NTP'           : 'Nearest to Target Pose',
    'NCC'           : 'Nearest to Current Configuration',
    'CLO'           : 'Config List Order',

    # Inverse:
    'Random'                            : 'RND',
    'Nearest to Target Pose'            : 'NTP',
    'Nearest to Current Configuration'  : 'NCC',
}
'''

## This class contains all the required settings of a workspace. 
class Workspace_Settings():
    '''
    '''
    all_search_criteria                 = ['Nearest to Target Pose', 'Nearest to Current Configuration', 'List Order']

    def __init__( self, creation_method = 'JSG', grid_resolution = 2, representation_of_orientation = 'angular_spherical', number_of_search_items = 1, number_of_configs = 10, search_criteria = 'Nearest to Target Pose'):

        '''
        creation_method: Configuration Generation Method
        
        Possible methods are:
        
        'Joint Space Grid'      (key = 'JSG'):  Initial Configurations generated by FK computations of configs of a grid of jointspace
        'Random'                (key = 'RND'):  Initial Configurations generated randomly (Additional time required only for generating random configurations)
        'Constant Set'          (key = 'CST'):  Initial Configurations read from a list of Configurations corresponding to a "Constant Set of Poses" (No additional time required)
        '''
        self.creation_method                  = creation_method
        # "number_of_intervals": determines the number of intervals, each joint takes in the jointspace grid
        self.grid_resolution                  = grid_resolution
        # e.g. 'vectorial_identity'
        self.representation_of_orientation    = representation_of_orientation 
        self.number_of_search_items           = number_of_search_items
        self.number_of_configs                = number_of_configs
        self.search_criteria                  = search_criteria
        
        self.read_workspace                   = False
        self.write_workspace                  = False

        self.predefined_config_list           = None
        
    def represent_orient_key(self):
        if self.representation_of_orientation == 'angular_spherical':
            return 'AngSph'
        elif self.representation_of_orientation == 'vectorial_identity':
            return 'VecIty'
        elif self.representation_of_orientation == 'Rotation Matrix':
            return 'RotMtx'
        else:
            assert False    

    def search_criteria_key(self):
        return self.search_criteria + str(self.number_of_search_items)

    def gen_key(self):
        
        if self.creation_method == 'JSGrid':
            ns = str(self.grid_resolution)
        else:
            ns = str(self.number_of_configs)
        return self.creation_method + ns
            
    def gen_file_name(self, manip_name):
        return manip_name + '_' + self.gen_key() + '_' + self.represent_orient_key() + '.ws'
        
    def __str__(self):
        s  = "\n"
        s += "Workspace Settings: " + "\n" + "\n"
        s += "Creation Method:                " + self.creation_method + "\n"
        s += "Grid Resolution:                " + str(self.grid_resolution) + "\n"
        s += "Representation of Orientation:  " + self.representation_of_orientation  + "\n"
        s += "Number of Configurations:       " + str(self.number_of_configs)  + "\n"
        s += "Number of Search Items:         " + str(self.number_of_search_items)  + "\n"
        s += "Search Criteria:                " + self.search_criteria  + "\n"
        
        return s        
        
        
class Workspace(endlib.Endeffector):
    '''
    This class inherits DH parameters from class: "Manipulator_Geometry" 
    It contains pre-computed kinematic properties of a manipulator in a discretized grid of the jointspace.
    These properties are in two equivalent lists named "config_list" and "pose_list"
    '''
    
    def __init__( self, config_settings, geo_settings, end_settings, ws_settings):
        '''
        '''
        super(Workspace, self).__init__(config_settings, geo_settings, end_settings)
        self.ws_settings = ws_settings
        # "config_list": List of configurations of a discretized jointspace grid. (Number of values for each joint is identified by property: "number_of_intervals") 
        #  list length  = (number_of_intervals ** DOF)
        self.config_list         = []
        # "pose_list": A List of poses equivalent to "config_list". Each list element is a pose vector corresponding to its equivalent configuration in the "config_list"
        self.pose_list           = []
        # "lower_pose" and "upper_pose" contain the lower and upper bounds of each element in the pose list
        self.lower_pose          = ()
        self.upper_pose          = ()
        
        # kd trees : 
        self.pose_tree           = None
        
        # TODO (principally): distance function for rotational joints ?!
        # ... for second use case ... 
        self.config_tree         = None

    def create_random(self):
        '''
        Generate a number of random configs in the feasible range of the jointspace and computes the forward kinematic of each configuration.
        The number of random points generated are determined by property: "self.ws_settings.number_of_configs" 
        The configurations are stored in property "self.config_list" and the corresponding poses are stored in property "self.pose_list"
        A pose contains 3 elements for each position (reference_position) and 3 elements for each orientation (reference_orientation)
        
        A nun-redundant parametrization for orientation should be introduced by property "self.representation_of_orientation"
        '''

        p                      = self.ws_settings.number_of_configs

        for i in range(0, p):
            print 'Creating Workspace .... ' + str(i) + ' out of: ' + str (p)
            
            assert self.set_config(self.random_config())
            
            '''
            for tp in self.task_point:
                H  = self.transfer_matrices()
                ra = tp.position(H)
                for j in range(0,3):
                    ef_pose += ra[j],
            '''
            ef_pose = self.pose_to_tuple('actual', self.ws_settings.representation_of_orientation)

            self.pose_list.append(ef_pose)
            self.config_list.append(self.free_config(self.q))

        pose_set   = set(self.pose_list)
        config_tuple_list = [ tuple(c) for c in self.config_list  ]
        config_set = set(config_tuple_list)
        
        self.pose_tree      = kdtree.KDTree.construct_from_data(list(pose_set))
        self.config_tree    = kdtree.KDTree.construct_from_data(list(config_set))

    def create_JSG(self):
        '''
        Generate a lattice in the jointspace and computes the forward kinematic of each configuration.
        The feasible range of each jach joint is divided by "self.ws_settings.grid_resolution" + 1 intervals. 
        The configurations are sstored in property "self.config_list" and the corresponding poses are stored in property "self.pose_list"
        A pose contains 3 elements for each position (reference_position) and 3 elements for each orientation (reference_orientation)
        
        A nun-redundant parametrization for orientation should be introduced by property "self.representation_of_orientation"
        
        '''

        p                      = self.ws_settings.grid_resolution ** self.config_settings.DOF
        self.ws_settings.number_of_configs = p
        '''
        fwd_kin.take_to_grid_configuration(0, self.ws_settings.grid_resolution)
        endeff.update(fwd_kin)

        for tp in endeff.reference_positions:
            tp.ru = numpy.copy(tp.ra)
            tp.rl = numpy.copy(tp.ra)
        '''    
        for i in range(0, p):
            print 'Creating Workspace .... ' + str(i) + ' out of: ' + str (p)

            assert self.set_config(self.grid_config(i, self.ws_settings.grid_resolution))
            '''
            for tp in self.task_point:
                for j in range(0,3):
                    if (tp.ra[j] > tp.ru[j]):
                        tp.ru[j] = tp.ra[j]
                        
                    if (tp.ra[j] < tp.rl[j]):
                        tp.rl[j] = tp.ra[j]
            '''
            ef_pose = self.pose_to_tuple('actual', self.ws_settings.representation_of_orientation)

            self.pose_list.append(ef_pose)
            self.config_list.append(self.free_config(self.q))
        '''
        self.lower_pose          = ()
        self.upper_pose          = ()
        for tp in endeff.reference_positions:
            for j in range(0,3):
                self.lower_pose  += tp.rl[j],
                self.upper_pose  += tp.ru[j],
        '''    
            
        pose_set   = set(self.pose_list)
        config_tuple_list = [ tuple(c) for c in self.config_list  ]
        config_set = set(config_tuple_list)
        
        self.pose_tree      = kdtree.KDTree.construct_from_data(list(pose_set))
        self.config_tree    = kdtree.KDTree.construct_from_data(list(config_set))

        self.file_name   = self.ws_settings.gen_file_name(self.geo_settings.name)

    def create(self):
        print "Workspace Creation Started. Creation Method: ",self.ws_settings.creation_method
        if self.ws_settings.creation_method == 'JSG':
            self.create_JSG()
        elif self.ws_settings.creation_method == 'RND':
            self.create_random()
        elif self.ws_settings.creation_method == 'PCL':
            if not self.ws_settings.predefined_config_list == None:
                i = 0
                p = len(self.ws_settings.predefined_config_list)
                for q in self.ws_settings.predefined_config_list:
                    print 'Creating Workspace .... ' + str(i) + ' out of: ' + str (p)
                    qf = self.free_config(q)
                    assert self.set_config(qf)
                    self.config_list.append(qf)    
                    ef_pose = self.pose_to_tuple('actual', self.ws_settings.representation_of_orientation)
                    self.pose_list.append(ef_pose)
                    self.ws_settings.number_of_configs = len(self.config_list)

                pose_set   = set(self.pose_list)
                config_tuple_list = [ tuple(c) for c in self.config_list  ]
                config_set = set(config_tuple_list)
                
                self.pose_tree      = kdtree.KDTree.construct_from_data(list(pose_set))
                self.config_tree    = kdtree.KDTree.construct_from_data(list(config_set))
            else:
                assert False, genpy.err_str(__name__, self.__class__.__name__, 'create', 'predefined_config_list has not been set. Workspace can NOT be created !')
        else:
            assert False, genpy.err_str(__name__, self.__class__.__name__, 'create', self.ws_settings.creation_method+ ' is not a valid value for creation_method')    

    def configs_nearest_to_pose(self, endeff):
        '''
        endeff contains the target pose         
        
        Return a list of configurations which:
            Their corresponding poses are closest to the target pose 
    
        QUESTION : configs_nearest_to_target( EE, distance ? ) ?? 
        '''
        Ns = self.ws_settings.number_of_search_items
        Nc = self.ws_settings.number_of_configs
        assert Ns <= Nc

        #first find the 10 closest poses to target
        target_pose = endeff.pose_to_tuple('desired', self.ws_settings.representation_of_orientation)
        nearest_pose = self.pose_tree.query(query_point = target_pose, t = Ns)
        nearest_config_list = []
        
        for pose in nearest_pose:
            nearest_config_list.append(numpy.copy(self.config_list[self.pose_list.index(pose)]))

        return nearest_config_list

    def configs_nearest_to(self, current_q):

        '''
        Return a list of configurations which:
            Are closest to the starting configuration
        
        (second  / online usecase : time coherence ... ) 
        '''
        if self.ws_settings.number_of_search_items == 0:
            return []
        
        #first find the closest configurations to the current configuration
        nearest_config_list   = self.config_tree.query(query_point = current_q, t = self.ws_settings.number_of_search_items)
        
        return nearest_config_list

    def nearest_configs(self, ik):
        if self.ws_settings.search_criteria   == 'NTP': # (key: NTP) Initial Configuration: Nearest to Target Pose
            nearest_config_list = self.configs_nearest_to_pose(ik)
        elif self.ws_settings.search_criteria == 'NCC': # (key: NCC) Initial Configuration: Nearest to Current Configuration
            nearest_config_list = self.configs_nearest_to(ik.free_config(ik.q))
        elif self.ws_settings.search_criteria == 'CLO': 
            nearest_config_list = []
            for i in range(self.ws_settings.number_of_search_items):
                nearest_config_list.append(self.config_list[i])
        else :
            assert False, genpy.err_str(__name__, self.__class__.__name__, 'nearest_configs', self.ws_settings.search_criteria + ' is not a valid value for search_criteria')
           
        return nearest_config_list
        
    def write_to_file(self, path_and_file_name):
        '''
        Save the class in file specified by "self.file_name"
        '''
        FILE_DATA = open(path_and_file_name, "w")
        pickle.dump(self, FILE_DATA)
        
        

