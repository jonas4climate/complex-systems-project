"""
Replication of 2.3, that the presence of noise can induce
the transition from the configuration with a cluster around
the leader to the unifcation of opinions in the whole group

We want a threshold phenomena graph
based on the critical temperature of the system 
above which we can overcome the leader infuence

"""

# Do simulations for many s_L

################################

import numpy as np
import demos.ca.cellular_automata as ca
import matplotlib.pyplot as plt

################################

GRIDSIZE_X,GRIDSIZE_Y = 15,15
TIMESTEPS = 30
TEMP = 0
BETA = 1
BETA_LEADER = 1
H = 0
P_OCCUPATION = 1
P_OPINION_1 = 0
#a_0 = 1 # Size of innitial cluster around leader

S_LEADER = 50   # Leader influence
S_MEAN = 1

################################

if TEMP == 0:
    expect_cluster = ca.analytical_expect_clusters(
        GRIDSIZE_X/2, BETA, H, S_LEADER)
    print('Expect clusters?', expect_cluster)

model = ca.CA(gridsize_x=GRIDSIZE_X, gridsize_y=GRIDSIZE_Y, temp=TEMP, beta=BETA, beta_leader=BETA_LEADER, h=H, p_occupation=P_OCCUPATION, p_opinion_1=P_OPINION_1, s_leader=S_LEADER, s_mean=S_MEAN)
data = model.evolve(TIMESTEPS)
simulation = data['opinions']
cluster_sizes = data['cluster_sizes']


# Plot it
plt.figure()
plt.imshow(model.starting_grid, cmap='seismic',interpolation='nearest', vmin=-1, vmax=1)
plt.title(f'Start,\n T={TEMP}, H={H}, B={BETA}, Bl={BETA_LEADER}, sL={S_LEADER},c_radius={int(cluster_sizes[0])}')
plt.tight_layout()
plt.show()

# Plot diagram to ensure we are within parabola!

fig, ax = ca.plot_diagram(GRIDSIZE_X/2,BETA,H)

R = GRIDSIZE_X/2
S_L_min = ca.minimun_leader_strength(R,BETA,H)
S_L_max = ca.maximun_leader_strength(R,BETA,H)
cluster_min = ca.a(R,BETA,H,S_L_min)
cluster_max = ca.a(R,BETA,H,S_L_max)
xmin,xmax = 0,2*S_L_max
ymin,ymax = 0,22.5




for time_step in range(1):#range(TIMESTEPS):

    # Get values!!!
    cluster_size = cluster_sizes[time_step]

    # Parabola critical points
    ax.scatter(S_L_min,cluster_min[0],c='black')
    ax.scatter(S_L_min,cluster_min[1],c='black')
    ax.scatter(S_L_max,cluster_max[0],c='black')

    # Floor
    x_floor = np.linspace(0, S_L_min, 100)
    y_floor = np.zeros(100)
    ax.plot(x_floor,y_floor,c='black',linestyle='--')

    # Parabola top arm
    x = np.linspace(0, S_L_max, 100)
    y = ca.a_positive(R,BETA,H,x)
    ax.plot(x,y,c='black',linestyle='--')

    # Parabola under arm
    x = np.linspace(S_L_min, S_L_max, 100)
    y2 = ca.a_negative(R,BETA,H,x)
    ax.plot(x,y2,c='black',linestyle='--')

    # Vertical line
    x = np.linspace(S_L_min, S_L_max, 100)
    ax.vlines(x=S_L_min, ymin=0, ymax=cluster_min[0], colors=['gray'], ls='dotted', lw=1)

    # Complete consensus line
    x_cons = np.linspace(xmin, xmax, 100)
    y_cons = np.ones(100)*R
    ax.plot(x_cons,y_cons,c='black',linestyle='-')

    # Title
    ax.set_title(f'Frame:{(time_step+1)}/{TIMESTEPS}, R={R}, Beta={BETA}, H={H}')
    ax.set_ylabel('a')
    ax.set_xlabel('S_L')

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)

    # Current leader influence!!!
    
    ax.vlines(x=S_LEADER, ymin=0, ymax=ymax, colors=['gray'], ls='dashed', lw=1)


    # Current cluster !!!!!
    
    ax.scatter(S_LEADER,cluster_size)
    
    
    plt.grid()
    plt.tight_layout()
    plt.pause(0.2)
    plt.show(block=False)
    ax.clear()


plt.show(block=True)


################################
# Show starting state
################################



################################
# Simulate for many temperatures
################################


print('Iterating temperatures')

NUMBER_OF_TEMPERATURE_VALUES_TO_TEST = 5
NUMBER_OF_SIMS_PER_TEMPERATURE_VALUE = 5
TMIN = 0
TMAX = 1000

UNIFICATION_THRESHOLD = 10 # MOST NODES

temperatures = np.linspace(TMIN,TMAX,NUMBER_OF_TEMPERATURE_VALUES_TO_TEST)
average_cluster_sizes = np.random.rand(NUMBER_OF_TEMPERATURE_VALUES_TO_TEST)


# Iterate all temperatures
for T in range(NUMBER_OF_TEMPERATURE_VALUES_TO_TEST):


    # Retrieve the T
    TEMP = temperatures[T]

    print(f'Temperature {T+1}/{NUMBER_OF_TEMPERATURE_VALUES_TO_TEST}: {TEMP}')


    # Do many simulations with that T to get av. cluster size
    for sim in range(NUMBER_OF_SIMS_PER_TEMPERATURE_VALUE):

        model = ca.CA(gridsize_x=GRIDSIZE_X, gridsize_y=GRIDSIZE_Y, temp=TEMP,
                beta=BETA, beta_leader=BETA_LEADER, h=H, p_occupation=P_OCCUPATION,
                p_opinion_1=P_OPINION_1, s_leader=S_LEADER, s_mean=S_MEAN)
        data = model.evolve(TIMESTEPS)
        simulation = data['opinions']
        cluster_sizes = data['cluster_sizes']

    # Get average cluster size
    av_cluster_size = np.mean(cluster_sizes)

    # Save it!
    average_cluster_sizes[T] = av_cluster_size



#Print last step of last sim with max temp
# Plot it
plt.figure()
plt.imshow(model.opinion_grid, cmap='seismic',interpolation='nearest', vmin=-1, vmax=1)
plt.title(f'End,\n T={TEMP}, H={H}, B={BETA}, Bl={BETA_LEADER}, sL={S_LEADER},c_radius={int(average_cluster_sizes[T])}')
plt.tight_layout()
plt.show()


plt.figure()

# Max cluster size line
x_cons = np.linspace(xmin, xmax, NUMBER_OF_TEMPERATURE_VALUES_TO_TEST)
y_cons = np.ones(NUMBER_OF_TEMPERATURE_VALUES_TO_TEST)*R
plt.plot(x_cons,y_cons,c='black',linestyle='-')

# Horizontal line with minimun value expected cluster


plt.plot(temperatures,average_cluster_sizes)
plt.title('Temperature of system to overcome leader')
plt.xlabel('Temperature')
plt.ylabel('Average cluster size')
plt.xlim([temperatures[0],temperatures[-1]])
plt.ylim([0,R])

plt.grid()
plt.tight_layout()
plt.show()