# MODFLOW Modeling with the Python FloPy Package

In this exercise, we will be using the flopy package to build and run some MODFLOW models using Python. 

## Part 1 - Well-Stream Interaction Model

In this exercise, we will build a simple well-stream interaction model using the flopy package. This model is based 
on sample problem illustrated on page 32 of the [USGS Sustainability of Ground-Water Resources (SGWR) Handbook](..
  /13_sustainability/1999%20-%20alley%2C%20reilly%2C%20franke%20%28sustainability%20of%20gw%20resources%29.pdf). 
This example features an aquifer next to a stream as shown below:

![figure_13.png](images/figure_13.png)

Part (A) illustrates the aquifer in a pre-development state. Water enters the aquifer via recharge and exits to the 
stream. Part (B) illustrates the aquifer shortly after the construction of a well near the stream. Initially, the 
well draws water that is entered the aquifer via recharge and it withdraws water from storage in the aquifer. Part 
(C) illustrates the state of the aquifer after the system has come to equilibrium. At this point, the well no longer 
takes water from storage and it pulls water both from aquifer recharge and stream discharge.

We will use the flopy package to build this model and anlyze the evolution of the aquifer over time. We will examine 
how much water is drawn from the aquifer and how much is pulled from the stream vs time. We will also examine the 
total amount of water removed from storage in the time it takes for the system to equilibrate.

You can download a solution to this exercise in GMS/MODFLOW format here: [well_stream.zip](files/well_stream.zip)

Click here to open a Google Colab notebook with the FloPy solution the problem:



### 1a. Pre-development model.

First we will build the pre-development model where the aquifer is in a steady state condition with recharge as the 
input and stream discharge as the sole output. The model will have the following characteristics:

grid x-dimension: 1000 ft (50 cells)<br>
grid y-dimension: 800 ft (40 cells)<br>
grid z-dimension: 200 ft (1 cell)

Stream: speficied head BC on the right = 150 ft.

K = 1 ft/day<br>
Recharge = 0.01 ft/day

### 1b. Well-stream interaction model (steady state)

Next we will build the well-stream interaction model with a single well located near the stream. We will use a 
steady state model to illustrate the state of the aquifer after the well has been installed and the system has come 
to full equilibrium. 

Well Q = -8000 ft/day<br>
Well location = row 21, column 42, layer 1

We will also examine the total amount of water removed from storage in the time it takes for the system to equilibrate.

### 1c. Well-stream interaction model (transient)

In this case, we will build a transient model where the well draws water from the aquifer and pulls water from the 
stream. We will examine how much water is drawn from the aquifer and how much is pulled from the stream vs time.

Total simulation time: 2000 days<br>
Single stress period with 200 time steps (10 days per time step)<br>
Specific yield = 0.15

We will generated animated gifs showing the evolution of the cone of depression of the well over time. We will also perform a flow budget analysis and plot the rate of storage change and the rate of stream discharge vs. time. 