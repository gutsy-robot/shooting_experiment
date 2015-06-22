## @file        	vectors_and_matrices.py
#  @brief     		This module provides some useful functions dealing with numpy vectors and matrices
#  @author      	Nima Ramezani Taghiabadi 
#
#               	PhD Researcher 
#               	Faculty of Engineering and Information Technology 
#               	University of Technology Sydney (UTS) 
#               	Broadway, Ultimo, NSW 2007, Australia 
#               	Phone No. :   04 5027 4611 
#               	Email(1)  : nima.ramezani@gmail.com 
#               	Email(2)  : Nima.RamezaniTaghiabadi@uts.edu.au 
#  @version     	5.0
#
#  Last Revision:  	03 January 2015 

import math, numpy

from math_tools import general as gen
from math_tools.geometry import trigonometry as trig



'''
use mgv
# global variables:
f0       = float(0)
f1       = float(1)
'''
err_code = 0

def rep(a, n):
    '''
    returns a numpy vector of length n containing a (all elements of the vector will be a)
    '''
    v = numpy.zeros(n)
    for i in range(n):
        v[i] = a
    return v

def as_matrix(v):
    '''
    gets vector v with n^2 elements and returns n*n matrix
    '''
    n_2 = len(v)
    n = int(math.sqrt(n_2))
    R = numpy.zeros((n,n))
    for i in range(n):
        for j in range(n):
            print "n*i + j = ", n*i + j
            print "R = ", v, n_2, n, R
            
            R[i,j] = v[n*i + j]
    return R            


def value_to_str( value, format="%.3f" ):
    if int(value) == value : 
        return  str(value)
    else : 
        return str(format%value)

def values_to_str( list_of_vals, format="%.3f" ) : 
    '''
    parametrized usage of sprintf
    '''
    formatted = []
    for v in list_of_vals : 
        formatted.append(value_to_str(v, format))
    return formatted

def vector_to_str( vector, format="%.3f" ) : 
    '''
    previous name: format_vector
    parametrized usage of sprintf
    '''
    n = len(vector)
    formatted = numpy.zeros((n))
    
    for i in range(n):
        formatted[i] = format%vector[i]
    return str(formatted)

def matrix_to_str( matrix, format="%.3f" ) : 
    '''
    parametrized usage of sprintf
    '''
    m = matrix.shape[0]
    n = matrix.shape[1]
    formatted = numpy.zeros((m,n))
    
    for i in range(m):
        for j in range(n):
            formatted[i,j] = format%matrix[i,j]          
    return str(formatted)

def which(v, condition, value):
    '''
    Returns the positions of those elements of vector v which satisfy the given condition with the given value
    condition is a string and must be in: '>', '>=', '<', '=='
    
    '''
    s = []
    for i in range(len(v)):
        if condition == '<':
            flag = (v[i] < value)
        elif condition == '>':
            flag = (v[i] > value)
        elif condition == '==':
            flag = (v[i] == value)
        elif condition == '<=':
            flag = (v[i] <= value)
        elif condition == '>=':
            flag = (v[i] >= value)
        else:
            assert False, "Error from vectors_and_matrices.which(): "+ condition+ " is an unknown condition."
        if flag:
            s.append(i)

    return s        

def remove(v, positions):
    '''
    Removes the items from v whose positions are specified in given array "positions" and returns the filtered vector
    '''
    w = []
    for i in range(len(v)):
        if not (i in positions):
            w.append(v[i])
    return w        

def matrix_column_multiply(A,v):
    '''
    equivalent to numpy.dot( A, numpy.diag(v) ) 
    
    multiplies each column of matrix A by the corresponding element in vector v. 
    This is equivalent to A*diag(v) but requires less calculations

    return numpy.dot( A, numpy.diag(v) ) 
    '''
    m = A.shape[0]
    n = A.shape[1]
    assert n == len(v)
    Adiagv = numpy.zeros((m,n))
    for i in range(0,m):
        for j in range(0,n):
            Adiagv[i,j] = A[i,j]*v[j]
    return Adiagv

def normalize(v):
    '''
    Returns the unit vector parallel to the given vector.
    '''
    l = numpy.linalg.norm(v)
    if gen.equal(l, 0.0):
        return(v)
    else:
        return(v/l)

def linear_map(q, f, g):
    '''
    return the linear mapping of vector q by coefficients f and g
        
        u = (q - g) / f
    
    This code should be implemented before:

        for i in range(0,len(f[i])):
            if abs(f[i]) < mgvlib.epsilon:
                print 'Error 01: Division by zero occured'
                print 'Something is wrong with the joint limits or the joint limit multipliers'
                print 'Make sure that the joint limits are well defined, and method "initialize" of the manipulator configuration has been implemented'
                assert False
    '''
        
    u = (q - g) / f
    return u    
 
def inner_product(v1, v2):
    '''
    returns the inner product of the two vectors v1 and v2
    '''
    return numpy.sum(v1*v2)
   
def as_vector(v):
    '''
    Returns a numpy array equal to v. Input argument v must be a normal array of numbers
    '''
    return(numpy.array(v))

def vectors_angle(v1, v2, in_degrees = False, positive_direction = numpy.zeros(3)):
    '''
    Returns the angle between two vectors. The positive direction, specifies which halfspace is used as positive vectors for the cross product of u and v
    if not specified, the returned angle will be always positive. 
    If specified, then if the sign of the returned angle is the same as the inner product of positive_direction and crossproduct(v1,v2)
    '''
        
    l_v1 = numpy.linalg.norm(v1)
    l_v2 = numpy.linalg.norm(v2)
    assert not general.equal(l_v1, 0.0)
    assert not general.equal(l_v2, 0.0)

    cos_theta = inner_product(v1, v2)/(l_v1*l_v2)
    
    theta = trigonometry.arccos(cos_theta)
    if general.equal(numpy.linalg.norm(positive_direction), 0.0):
        return(theta)
    else:
        return math.copysign(theta, inner_product(numpy.cross(v1, v2), positive_direction))

def linear_map_inv(u,f,g):
    '''
    return the inverse linear mapping of vector u by coefficients f and g
    
        q = f * u + g 
    '''
    q = f * u + g 
    return q 
    
def diag_old(v):
    '''
    return an square diagonal matrix whose diagonal elements are elements of vector v
    '''
    # numpy.diag : Use k>0 for diagonals above the main diagonal, and k<0 for diagonals below the main diagonal.
    return numpy.diag(v, k = 0 )
    

def vector_element_multiply_old(v1,v2):
    '''
    elementwise multiplication of two vectors. 
    
    !!! http://www.scipy.org/NumPy_for_Matlab_Users !!!     
    '''
    return v1 * v2
    

def cut_vector_old(v4):
    '''
    returns a three element vector containing the first three elements of v4
    '''
    return v4[0:3]

def extend_vector(v3):
    '''
    get a three element vector and add one element to its end. Return a four element vector
    '''
    v4 = numpy.zeros((4))
    for i in range(0,3):
        v4[i] = v3[i]
    v4[3] = 1
    return v4
    
def equal(v1,v2, epsilon = gen.epsilon):
    '''
    Returns 1 if two vectors or matrices are equal otherwise returns 0
    '''
    return (numpy.linalg.norm(v1-v2) < epsilon)

def uvect(TRM,m):
    '''
    uvect is a shorted phrase of "unit vector"
    
    Returns a vector (3 X 1) containing the first three elements of the m-th column of transformation matrix TRM. 
    (TRM is the 4*4 transformation matrix or a 3X3 rotation matrix) 
    If m is in [0,1,2] the m-th unit vector is returned. If m is 3, then the function returns the position vector
    '''
    return TRM[ 0:3,m ] 

def extract_rotation_matrix(TRM):
    '''
    Returns the rotation matrix (3 X 3) extracted from transformation matrix TRM. TRM is a 4*4 matrix
    '''
    return TRM[ 0:3, 0:3 ] 
    
def cross_old(u,v):
    '''
    Return the cross product of two vectors u and v. u and v are (3 element) vectors
    '''
    return numpy.cross(u,v)

def extended_matrix( R, p ):
    '''
    Convert a (3 X 3) rotation matrix into a (4 X 4) transformation matrix. The added elements will be zero
    '''
    em = numpy.zeros((4,4))
    for i in range(0,3):
        em[i,3] = p[i]
        em[3,i] = 0
        for j in range(0,3):
            em[i,j] = R[i,j]
    return em;

def right_pseudo_inverse(J):
    '''
    Return the right pseudo-inverse of matrix J
    J^T*(J*J^T)^(-1)
    --> take a look at ! numpy.linalg.pinv(a) !
    '''
    A = numpy.dot(J,J.T);
    Jinv = numpy.dot(J.T,numpy.linalg.inv(A))
    return Jinv

def left_pseudo_inverse(J):
    '''
    Return the left pseudo-inverse of matrix J
    (J^T*J)^(-1)*J^T
    '''
    A = numpy.dot(J.T,J);
    Jinv = numpy.dot(numpy.linalg.inv(A), J.T)
    return Jinv

def right_dls_inverse(M, k):
    '''
    returns the right side damped least square inverse of matrix M. k is the damping factor:

    M^T * [M*M^T + (k^2)*I]^(-1)

    '''
    m = M.shape[0]
    A = numpy.dot(M, M.T);
    
    Minv = numpy.dot(M.T, numpy.linalg.inv(A + k*k*numpy.eye(m)))
    return Minv

def left_dls_inverse(M, k):
    '''
    returns the left side damped least square inverse of matrix M. k is the damping factor:

    [M^T*M + (k^2)*I]^(-1) * M^T
    
    --> take a look at ! numpy.linalg.pinv(a, rcond=1.0000000000000001e-15) !
    '''
    m = M.shape[1]
    A = numpy.dot(M.T, M);
    
    Minv = numpy.dot(numpy.linalg.inv(A + k*k*numpy.eye(m)), M.T)
    return Minv

def collapse(v, max_norm):
    '''
    if the magnitude(norm) of the given vector is smaller than max_norm, the given vctor is returned
    otherwise a vector parallel to v with norm max_norm is returned
    '''
    l = numpy.linalg.norm(v)
    if l > max_norm:
        return v*max_norm/l
    else:
        return v

## Use this function to check if all elements of a given vector are positive
def positive(v, non_zero = False):
    permit = True
    n      = len(v)
    i      = 0
    while permit and (i < n):
        permit = permit and (v[i] >= 0) and (not (non_zero and gen.equal(v[i], 0.0)))
        i += 1
    return permit
