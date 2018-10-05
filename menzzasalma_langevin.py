import numpy as np #importing needed python packages
import matplotlib.pyplot as plt
import pylab
import argparse
import math

#import command line arguments into program. All must be floats
parser=argparse.ArgumentParser(description="Models 1D motion of a particle.")
parser.add_argument('--temperature', metavar='temperature', type=float, default=300, nargs='?')
parser.add_argument('--total_time', metavar='total_time', type=float, default=1000, nargs='?')
parser.add_argument('--time_step', metavar='time_step', type=float, default=0.1, nargs='?')
parser.add_argument('--initial_position', metavar='initial_position',type=float, default=0, nargs='?')
parser.add_argument('--initial_velocity', metavar='initial_velocity', type=float, default=0, nargs='?')
parser.add_argument('--damping_coefficient', metavar='damping_coefficient', type=float, default=0.1, nargs='?')
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
    kB: Boltzmann constant, reduced to 1 for the purposes of this program
    
    returns:
    the value of the random force acting on the particle at a given point in time'''
    
    variance = 2*temperature*gamma*kB #calculates variance using the equation given in the problem statement
    standardDeviation=np.sqrt(variance) #standard deviation is the square root of variance
    random=np.random.normal(loc=0,scale=standardDeviation) #returns the random force on the particle using a normal ditribution
    return random

def integrator(timeStep, velocity, position, temperature, gamma=1, kB=1):
    '''Uses the Euler method to numerically integrate the force acting on the particle.
    Returns the particle's velocity after a given time step and the 
    particle's position after a given time step. 

    args:
    timeStep: float. The length of one unit of time. This function finds the value of position and velocity after each one of these. 
    velocity: float. The particle's velocity at any given time
    position: float. The particle's position at any given time
    temperature: float. The temperature of the system
    gamma: float. The damping coefficient for the system
    kB: int. Boltzmann constant, reduced to 1 for this program
    
    returns:
    A tuple. Index 0 is the instantaneous velocity after any given time step, and index 1 is the instantaneous position after any given time step'''
    
    acceleration = dragForce(velocity, gamma) + randomForce(temperature,gamma)
    newVelocity = velocity + acceleration*timeStep #from Euler method: y_n+1 = y_n + h*f(y,t)
    newPosition = position + velocity*timeStep
    return newVelocity, newPosition

def particleMotion(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma=1, wallSize=5):
    ''' A function that uses the Euler integrator function defined above to generate the path of a particle undergoing Brownian motion. 

    args:
    timeTotal: The length of time each particle trial is constrained to. 
    wallSize: The distance from the particle's starting point that the other positional boundary is placed. 
    See integrator function for other args.

    Returns:
    A tuple. Index 0 is a list of the particle's instantaneous velocity after each time period. Index 1 is the particle's instantaneous position after each
    time period. Index 3 is the amount of time elapsed before each velocity and position update. Index 4 is the final velocity, and index 5 is the final position. 
    '''
    counter = 0
    trialVelocities=[initialVelocity] #populate velocity and position lists with the initial values that will be used in the first loop of the integrator function
    trialPositions=[initialPosition]
    maxTrials=int(timeTotal/timeStep) #compare this to increasing counter to make sure function does not exceed total time alloted. 
    time=[0] #will give list of time elapsed before each velocity/position update
    for i in range((maxTrials)): 
        results = integrator(timeStep,trialVelocities[i],trialPositions[i],temperature,gamma) #give integrator its args for a given time...
        trialVelocities.append(results[0]) #results of integrator are then added to the end of the velocity/position lists and get used in the next loop of the integrator 
        trialPositions.append(results[1])
        counter=counter+1 
        time.append(timeStep*counter)    
        if trialPositions[i] < 0 or trialPositions[i] > 5 or counter == maxTrials: #the current position of the particle is compared to the wall boundaries. If it's outside the walls or the trial has taken the maximum amount of time, the loop ends 
            return trialVelocities, trialPositions, time, trialVelocities[-1], trialPositions[-1]
            break

def histogramGenerator(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma=1, wallSize=5, numRuns=100):
    '''This funtion uses the particleMotion function to collect information on the amount of time a large sample of runs takes, and plots that data on a histogram.
    
    args:
    numRuns: The number of runs that will be performed using the particleMotion function. This is the number of points that will be plotted on the histogram.
    See particleMotion function for information on other args.
    
    Returns:
    A picture file called "histogram.png" that shows how many runs ended between certain time frames. Be careful, because this file is overwritten every time the program is run.
    '''
    timeToCollision=[] #this list is populated by the final time of each of the completed runs
    for i in range(int(numRuns)):
        trial=particleMotion(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma)
        timeToCollision.append(trial[2][-1]) #appends the last element of the "time" output list from the particleMotion function
    maxIndex=np.argmax(timeToCollision) #finds the index of the largest time needed to complete the run. This is used to help calculate the bins of the histogram
    maxValue=int(timeToCollision[maxIndex]) #takes the maximum time value, and turns it into an integer. This is to prevent having bins with long decimal values
    bins=np.arange(maxValue) #this makes an array with every integer from 0 to the highest time value
    plt.figure(num=1)
    plt.hist(timeToCollision,bins, rwidth=0.9)
    plt.title("Time needed to collide with wall")
    plt.xlabel('Time until wall collision')
    plt.ylabel('Number of runs')
    plt.xticks(bins)
    pylab.savefig("histogram.png") #saves the histogram to a picture file

def trajectory(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma=1, wallSize=5):
    '''Uses the particleMotion function to show a visual representation of a particle's motion during a run. Will plot the 
    position of the particle as a function of time and save it to a file.
    
    args:
    These are the same as the particleMotion function.
    
    Returns:
    A picture file called "trajectory.png" that has position of the particle on the y-axis and elapsed time on the x-axis. '''
    trial=particleMotion(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma) #obtains trial data
    while trial[4] < 5: #this loop is to ensure that the run being plotted is one that ends with the particle travelling to the wall at 5, instead of ending when it moves backwards past zero.
        trial=particleMotion(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma)
    plt.figure(num=2)
    plt.plot(trial[2],trial[1])
    plt.title('Position of the particle over time')
    plt.xlabel('Time')
    plt.ylabel('Position')
    pylab.savefig("trajectory.png")
        
histogramGenerator(timeStep,timeTotal,initialVelocity,initialPosition,temperature,gamma)
trajectory(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma)

def fileWrite(data):
    ''' This function creates a text file that shows the instantaneous velocity, instantaneous position, and elapsed time for each time step before a particle
    exits the boundaries of the trial. 

    args: 
    data: A list. This will be the output from the particleMotion function.

    Returns:
    A file called "Langevin Trial Data.txt" that contains velocity, position, and time logged. This will overwrite each time the program runs.'''
    file=open("Langevin Trial Data.txt", "w")
    file.write("Velocity     |       Position      |      Time \n") #puts a header on each rough "column" in the file
    for i in range(len(data[0])-1):
        file.write(str(data[0][i]) +"     |      "+ str(data[1][i])+"      |      "+ str(data[2][i])+"\n") #adds the values at each index in three of the output tuples from the particleMotion function.
    print("The final position is ", test[4]," and the final velocity is ",test[3]) #prints the final velocity and position of the particle to the command line
    
Trial = particleMotion(timeStep, timeTotal, initialVelocity, initialPosition, temperature, gamma)
fileWrite(Trial)
