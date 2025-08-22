# Case Study #6 - Transient Analysis

When wells G and H were active, they were only used during the summer months. In the steady state model, we are using a pro-rated pumping rate representing an annual average. In this exercise we will convert our steady state predictive model to a transient model to see if the transient pumping conditions make a difference with our particle tracking results. We will cycle the pumping of wells G and H such that they are on in the summer months and off in the remaining months.

## Loading the Project

Before continuing,

>>1) Launch GMS and open the particle-tracking model you created in [<u>case study #4</u>](fillthisin).

>>2) Save the project to a new name (case4-ss.gpr or something - "ss" for the initial steady state run).

## Setting up the Initial Condition

With all transient models, the initial conditions must be carefully considered. Well G was pumped at about 700 gpm (134,750 ft^3/d) and well H at about 400 gpm (77,000 ft^3/d) during the summer months.  Well G went online in the summer of 1965 and Well H began pumping in 1968.  Since both wells were offline prior to the time we begin modeling this site, we will run a steady state solution with Wells G and H off.  This steady state solution will provide the initial conditions for the transient run.

>>1) Go to the map module and set the pumping rate for wells G and H equal to zero.

>>2) Select the **Map -> MODFLOW** command to convert your changes.

>>3) Save your changes and re-run MODFLOW.

You should see the solution change. Now we will take the heads we just computed and copy them to the starting heads array.

>>4) Open the **Starting Heads** dialog.

>>5) Use the **3D Data Set -> Grid** button to copy the steady state solution to the **Starting Heads** array.

## Setting up the Transient Model

Now we will convert the steady state model to a transient model.

### Stress Periods

First, we will turn on the transient option and define the stress periods.

>>1) Save the project under a new name (**case6-trans.gpr** for example).

>>2) Open the **Global Options** dialog and change the **Model type** to **Transient**.

>>3) Open the **Stress Periods** dialog and turn on the **Use dates/times** toggle.

>>4) Enter a set of dates to define the stress periods used in the simulation. We will start the simulation on 1/1/1965 and end it on 5/1/1979. The wells start pumping each year on 6/1 and stop pumping on 9/1 each year. This results in a total of 29 stress periods. Make your time steps about ten days long. When finished, your dialog should look like the example shown in Figure 1. Note that you do not need to enter the times, just the dates. You may find it easier to enter dates and time steps in Excel (see [<u>stress periods.xlsx</u>](case_study_6/stress%20periods.xlsx)) and paste them to the dialog via the clipboard. Don't worry about setting up the lengths as they are automatically calculated by GMS from the dates.

![stressperiods.png](case_study_6/stressperiods.png)

_Figure 1. Stress Periods Dialog._

Before saving our changes, we delete the head and flow observations in the Map Module. Otherwise, we would get a series of warnings and error messages each time we save the model since we have steady state observations mixed with a transient simulation.

>>5) Delete the coverage containing the observation wells.

>>6) Double-click on the river arc and turn off the observed flow.

>>7) Save your changes to the project.

### Pumping Schedule

Next we will modify the well data in the conceptual model to correspond to the transient pumping schedule. The pumping schedules for the wells are saved in a text file which you’ll import into GMS. 

>>1) Right-click and download the file [<u>wellschedules.txt</u>](case_study_6/wellschedules.txt).

Open up the wellschedules.txt file in a text editor. Note that well H did not go online until 1968. Each record represents a well id, date, time, and pumping rate. The well id (name) in the first column should match the name assigned to the wells in the conceptual model corresponding to wells G and H. Before continuing,

>>2) Open up the attribute table for the coverage containing the wells

>>3) Change the Feature type to Points to display the wells.

>>4) Change the names for wells G and H to exactly match the names used in the wellschedules.txt (case sensitive).

Now we are ready to import the pumping schedule. After importing the file, there will be a time series associated with each well corresponding to the pumping schedule.

>>5) Select the **File|Open** command and change the filter to ***.txt**.

>>6) Follow the steps in the wizard to import the file. In step 2, be sure to change the **GMS data type:** option to **Pumping data**. Click Yes when asked if you want to import the times series as a step function.

Now we will check to make sure the schedule was properly imported.

>>7) Double-click on one of the wells.

>>8) Click on the small "..." button on the right side of the **Flow rate** field (it should say "<span style="color:blue"><transient\></span>").

You should see the pumping schedule represented as a time series. Note that some of the dates are repeated in order to set up the time series as a step function (pumping rates change instantaneously).

>>9) Select the **Map -> MODFLOW** command to transfer the pumping data to the Well package stress period format.

### Storage Coefficients

Now that the model is transient, we need to specify storage coefficients. We will need both specific storage and specific yield.  The tables below list some common values for specific yield and specific storage. Select one value from each table.

| Material                |   	Specific storage (Ss) (m-1)    |
|:------------------------|:---------------------------------:|
| Plastic Clay            | 	2.0E-02 &emsp;	to &emsp;	2.6E-03 |
| Stiff Clay              | 	2.6E-03 &emsp;	to &emsp;	1.3E-03 |
| Medium-hard clay        | 	1.3E-03 &emsp;	to &emsp;	9.2E-04 |
| Loose sand	             | 1.0E-03 &emsp;	to &emsp;	4.9E-04  |
| Dense sand	             | 2.0E-04 &emsp;	to &emsp;	1.3E-04  |
| Dense sandy gravel	     | 1.0E-04 &emsp;	to &emsp;	4.9E-05  |
| Rock, fissure, jointed	 | 6.9E-05 &emsp;	to &emsp;	3.3E-06  |
| Rock, sound             |         	Less than 3.3E-6         |

_Table 1. Specific Storage (Anderson & Woessner, 1992)._

| Material   |	Specific Yield (Sy)<br/>Min| 	Specific Yield (Sy)<br/>Max | 	Specific Yield (Sy)<br/>Ave |
|:-----------|:--------------------------:|:----------------------------:|:----------------------------:|
| Clay       |           	.00	            |            	.05	             |             	.02             |
| Sandy clay |            .03             |             .12              |              .07             |
| Silt       |            .03             |             .19              |             .18              |
| Fine sand  |            .10             |             .28              |             .21              |
| Medium sand|            .15             |             .32              |             .26              |
| Coarse sand|            .20             |             .35              |             .27              |
| Gravelly sand|            .20             |             .35              |             .25              |
| Fine gravel|            .21             |             .35              |             .25              |
| Medium gravel|            .13             |             .26              |             .23              |
| Coarse gravel|            .12             |             .26              |             .22              |

_Table 2. Specific Yield (Fetter, 1994)._

Since we will be using one set of values for the entire grid, we will enter the values directly into the arrays in the LPF package rather than using polygons in the Map Module.

>>1) Open the SY array dialog and enter your selected value for specific yield.

>>2) Open the SS array dialog and enter your selected value for specific storage.

## Running the Model

We are now ready to run the model.

>>1) If you still have particle sets in the project, make sure they are turned off in the Project Explorer. Otherwise the display refresh will be slow when you import the solution.

>>2) Save the project and run MODFLOW. It should take a few minutes to complete. 

>>3) Close the model wrapper dialog and view the solution. Since you have over 500 time steps, it may take a few minutes to read the solution.

>>4) Click on the solution folder in the **Project Explorer**. You should see the **Time Step Window** appear at the bottom of the **Project Explorer**. You can scroll through the time steps and click on them to view how the solution varies over time.

Depending on the K values used in your model, you may get some cell drying for the top cell associated with well G. If so, you may want to try adjusting K in the vicinity of the well to see if you can eliminate the drying. I was able to make this cell stop drying by setting K=200 right at well G and K=50 for the eight cells surrounding well G (in layer one only).

## Particle Tracking

At this point you may want to consider doing a forward particle tracking analysis considering the following information from the jury instructions in the Woburn trial.
