import numpy as np #importing needed python packages
import matplotlib.pyplot as plt
import argparse

#import command line arguments into program. All must be floats
parser=argparse.ArgumentParser(description="does a thing")
parser.add_argument('--temperature', metavar='temperature', type=float,  nargs='?')
parser.add_argument('--total_time', metavar='total_time', type=float, nargs='?')
parser.add_argument('--time_step', metavar='time_step', type=float, nargs='?')
parser.add_argument('--initial_position', metavar='initial_position', type=float, nargs='?')
parser.add_argument('--initial_velocity', metavar='initial_velocity', type=float, nargs='?')
parser.add_argument('--damping_coefficient', metavar='damping_coefficient', type=float, nargs='?')
args = parser.parse_args()

#take imported values out of parser and convert them into usable variables
temperature = args.temperature
timeTotal=args.total_time
timeStep=args.time_step
initialPosition=args.initial_position
initialVelocity=args.initial_velocity
gamma=args.damping_coefficient
#defining functions for the separate forces acting on the particle and integrator for those forces
def dragForce(velocity, gamma=1):
    '''Returns the drag force on a particle undergoing Brownian motion.
    The result will be a negative value.
    
    args:
    gamma: the damping coefficient for the system
    velocity: the instantaneous velocity of the particle
    
    returns:
    the value of drag force acting on the particle'''
    drag=gamma*velocity
    return drag

def randomForce(temperature,gamma=1,kB=1):
    '''Returns the random force on the particle undergoing Brownian motion based on the input condition.
    The input arguments are used to find the variance, which is used to obtain
    standard deviation and then the normal distribution from which the random force is drawn
    
    args:
    temperature: the temperature of the system
    gamma: the damping coefficient for the system
    kB: int. Boltzmann constant, reduced to 1 for this program
    
    returns:
    the value of the random force acting on the particle at a given point in time'''
    
    variance = 2*temperature*gamma*kB #calculates variance using the equation given in the problem statement
    standardDeviation=np.sqrt(variance) #standard deviation is the square root of variance
    random=np.random.normal(loc=0,scale=standardDeviation) #returns the random force on the particle using a normal ditribution
    return random


def integrator(timeStep, velocity, position, temperature, gamma=1, kB=1, mass=1):
    '''Uses the Euler method to numerically integrate the force acting on the particle.
    Returns the particle's velocity after a given time step and the 
    particle's position after a given time step. 

    args:
    velocity:
    position:
    temperature: float. The temperature of the system
    gamma: float. the damping coefficient for the system
    kB: int. Boltzmann constant, reduced to 1 for this program
    mass: int. Will always be one for this problem
    
    returns:
    The instantaneous velocity after a given time step 
    The instantaneous position after a given time step'''
    
    acceleration = dragForce(velocity, gamma) + randomForce(temperature,gamma)
    newVelocity = velocity + acceleration*timeStep #from Euler method: y_n+1 = y_n + h*f(y,t)
    newPosition = position + velocity*timeStep
    return newVelocity, newPosition

def particleMotion(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma=1, mass=1, wallSize=5):
    index = 0
    trialVelocities=[initialVelocity]
    trialPositions=[initialPosition]
    maxTrials=int(timeTotal/timeStep)
    time=[0]
    for i in range((maxTrials)):
        results = integrator(timeStep,trialVelocities[i],trialPositions[i],temperature,gamma)
        trialVelocities.append(results[0])
        trialPositions.append(results[1])
        index=index+1
        time.append(timeStep*index)    
        if trialPositions[i] < 0 or trialPositions[i] > 5 or index == maxTrials:
            return trialVelocities, trialPositions, time
            break


