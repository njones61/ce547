# MODFLOW Case Study - Fremont River Model

For this case study, we will be solving the problem shown in the following figure using a one layer MODFLOW model.  Since the model domain is rectangular and the source/sink objects are simple, we can set up this model quickly using the “grid approach”.  The site is 1800 m wide from east to west and 2000 m wide from north to south.  The west boundary corresponds to a ground water divide and the north and south boundaries correspond to parallel flow boundaries.  Thus, these three boundaries will be simulated as no-flow boundaries.  The east side of the model corresponds to a river that will be modeled with a constant head boundary.  Two production wells and an agricultural drain are located within the model domain.

![fremont.gif](images/fremont.gif)

**Background Image**

Before building the model, first download and unzip the following file: [<u>startfiles.zip</u>](zip%20folders/startfiles.zip)

Then launch GMS and read in the project file (map.gpr) using the **File|Open** command.

**Steps**

Build your MODFLOW model using the following basic steps:

1) Select the appropriate units (length = m, and time = d).

2) Create a one layer grid of the proper X and Y dimensions and use 45 cells in the X direction and 50 cells in Y direction.

3) Save your project to a new file name (use the Save As command) and save the model frequently during the exercise.

4) Initialize your MODFLOW simulation.
>a) Select the packages you wish to use.<br>
>b) Enter a top elevation of 400 m and a bottom elevation of 250 m.  For simplicity, we will assume that the top and bottom of the aquifer are relatively flat.

5) Create a constant head boundary on the right side of the model = 317 m.

6) In the LPF package, use a convertible layer.  Enter a value of K = 0.1 m/d for the entire grid.

7) Enter a recharge value of 0.00055 m/d for the entire grid.

8) Create a set of drains in the location of the agricultural drain.  Enter a conductance of 200 m^2/d and use a drain elevation = 317m.<br>
>_Note: To help you select the correct cells, change the cell edge style from solid to dashed._

9) Create two wells at the location shown.
>a) For well SR-3, enter a pumping rate of –300 m^3/d.<br>
>b) For well SR-4, enter a pumping rate of –450 m^3/d.

10) Check your model for errors and then save and run the simulation.

**Analysis**

If your solution is successful, you may wish to try modifying your model as follows:

1) Change the conductance on the drains and see if it makes a significant difference in the solution.

2) Try increasing the pumping rate for the wells to see what happens to the drawdown.  At some point the wells will go dry.

3) Change the hydraulic conductivity and the recharge and notice how sensitive the model is to these two parameters.

## Solution

Step-by-step instructions with screen shots: [<u>fremont river, part 1.pptx</u>](fremont%20river%2C%20part%201.pptx)

GMS project file with final version of model: [<u>fremont1.zip</u>](zip%20folders/fremont1.zip)

Video: [<u>www.youtube.com/watch?v=1AaLIQfzQ6U</u>](https://www.youtube.com/watch?v=1AaLIQfzQ6U)

# MODFLOW Case Study - Fremont River Model, Part 2

For this case study, we will be revisiting the Fremont River model. We will add a lake and a flow barrier simulating a low permeability fault.

1) Download and unzip the [<u>start.zip</u>](zip%20folders/start.zip) file. Open the **fremont2.gpr** file in GMS.

2) Apply general head conditions to the cells in the vicinity of the lake polygon.
>a) Select the cells using a polygon<br>
>b) Create GHB cells.<br>
>c) Compute and assign an appropriate conductance. Assume:<br>
>>H = 360<br>
>>Thickness of sediment = 2 m<br>
>>K of sediment = 0.2 m/d<br>
>>Cell size = 40 m x 40 m

3) Save and run

4) Apply HFB conditions to simulate fault
>a) Select pairs of cells and toggle barrier (one pair at a time)<br>
>b) HC = 0.00001

5) Save and run

Experiment with parameter values.
 
## Solution

Step-by-step instructions with screen shots: [<u>fremont river, part 2.pptx</u>](Fremont%20River%2C%20Part%202.pptx)

GMS project file with final version of model: [<u>fremont2.zip</u>](zip%20folders/fremont2.zip)

Video: [<u>www.youtube.com/watch?v=OwDWJ-IAb5Q</u>](https://www.youtube.com/watch?v=OwDWJ-IAb5Q)

 

 

 
 

 