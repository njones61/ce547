# Case Study #2 - Calibration

In this exercise we will input the field observations and calibrate the model.

## Loading the Project

Before continuing,

>>1) Launch GMS open the GMS project you created in [<u>Case Study #1</u>](https://byu-ce547.readthedocs.io/en/latest/termproject/casestudy1/case_study_1/).

>>2) Select **File|Save As** to save the project under a new name.

Be sure to save your changes often as you work through the case study.

## Observation Data

To calibrate the model, we need field observed values. We’ll use head observations at monitoring wells, and a flux observation on the Aberjona river.

### Head

The head observations were collected in April, 1985.

>>1) Right-click to download the [<u>4-3-85_observe.txt</u>](4-3-85_observe.txt) file to your local drive.

>>2) Right-click on your conceptual model object and create a new coverage.

>>3) Change the name to **obs heads** and turn on the **Head** option in the **Observation Points** section of the dialog.  Make sure that the **3D grid layer options for obs. pts.** is set to **By z** location.

>>4) Open the **4-3-85_observe.txt** file.  Follow the appropriate steps in the text import wizard.

There is another set of head observations ([<u>12-1-85_observe.txt</u>](12-1-85_observe.txt)) collected at the beginning of December 1985, prior to the 30-day pump test. You are welcome to use these observations as well. Just make sure you don't use both the April and the December observations at the same time.

### Flow

The net gain or loss of water between the Aberjona river and the aquifer varies. You need to choose the flow observation on the Aberjona river that you want to use.  The following information from the USGS report might be helpful:

_“During low-flow conditions when most measurements were made, the Aberjona River reach flowing through the study area gained between 0.1 and 0.62 ft3/s.  With the exception of the September 20, 1985, discharge measurement, all measurements of stream discharge during the 3 months prior to the 30-day aquifer test indicated a net streamflow gain between the inflow and outflow measuring sites.” (Myette and others, 1987)_

>>1) Double click on the coverage containing your river arc.  Turn on the **Observed Flow** option in the **Sources/Sinks/BCs** section of the dialog.

>>2) Enter a flow observation value into the river arc.  You’ll probably need to do a units conversion so your units are consistent.

## Parameterization

You can use either polygonal zones or pilot points or both as you calibrate the model with PEST.  Since we don’t have much information on where to create polygonal zones, you might want to use pilot points for both recharge and hydraulic conductivity.  In the interest of time, however, I recommend that you use pilot points only for the hydraulic conductivity and polygonal zones for recharge.

To parameterize the input:

>>1) Enter a key value (-100 for example) for all cells in the HK array in the LPF package.

>>2) Create a set of pilot points

>>>>a) Create a new 2D scatter point set.

>>>>b) Set the default data set value to **15** in the **Scatter Point Settings** dialog because 15 is the starting hydraulic conductivity we want to use.

>>>>c) Create a set of scatter points. Don’t create more than 30 to 35 points to begin with (you can add more later). Concentrate your points mainly in-between your observations, and also between observations and the edge of the model.

>>3) You need to decide how you want to handle recharge. There are two options:

>>>>a) You could use a single constant value of recharge for the entire model domain. In this case you will use a single recharge polygon. This approach is simple and conservative.

>>>>b) You could subdivide the recharge coverage into a set of polygonal zones based on soil type, slope, and land use. If you choose this option, you need to be careful that you do not allow the recharge in each zone to vary drastically from the mean. You can control this using the min/max bounds in the parameter dialog. One option would be to have one recharge zone by the river and then the areas on the left and right of the river as a single zone. You probably would not get much recharge by the river because the ground is likely to be saturated. This would justify having more water coming from the edges which might help or hurt your case depending on which side you represent.

>>>>Regardless of which approach you use, you can calculate ahead of time almost exactly what your total recharge should be. You have a closed system: water enters via recharge and exits via discharge to the river and pumping from the two industrial wells. Using a spreadsheet you can calculate exactly how much water is leaving the system and that represents how much water has to come in via recharge. This is a volumetric flow rate (ft^3/day). If you take this value and divide it by the area of the model you will have your recharge rate in ft/day. This is what you would apply in option (a) above with a single polygon. If you use option (b), the total volumetric recharge would have to match this value. You can still calibrate recharge as a parameter, but the total recharge is fixed.

>>4) Parameterize the recharge coverage by replacing the recharge rate for each polygon with a negative integer number.

>>>>a) Keep track of which recharge rate goes with which parameter value – you’ll need this to enter starting values in the next step.

>>>>b) When you’re done, be sure to select **Map -> MODFLOW.**

>>>>**Note:** Given that recharge is the only source of water and the sinks are fixed (river discharge, two wells), you can use a spreadsheet to calculate the recharge rate(s) required for flow calibration using a water budget.

>>5) In the MODFLOW **Parameters** dialog, select **Initialize from Model** to create the parameters.  Enter the correct starting values. Turn on pilot points for the hydraulic conductivity parameter.

## Forward Run/Manual Calibration

It is a good idea to run your model in forward mode with the parameters before you attempt automated parameter estimation.

>>1) Save your project as **forward.gpr** and run MODFLOW.

Hopefully your model ran fine. If not, troubleshoot the parameters and make sure the input values are correct. After your model has successfully run you may want to look at the observed heads and the flux observation and adjust the parameter values manually until you start to see a decent fit.

## Automated Calibration

To set up the model for automated calibration with PEST.

>>1) Save your project under a new name so you can distinguish the forward run from the inverse runs (**inverse-01.gpr** for example).

>>2) From the MODFLOW **Global Options** dialog, change the run type to **Parameter Estimation**. 

>>3) In the **Parameters** dialog, turn on the solve toggle for each of the parameters.

>>4) Enter the correct min and max values (don’t use 0.0 for the min for any of these as PEST has problems with 0.0). Turn on the log transform option for all parameters.

>>5) Save your project and run MODFLOW. If all goes well, PEST will run MODFLOW many times as it calibrates the model. This will likely take over an hour. When the process completes, close the dialog.

Now you should be looking at the solution from a calibrated model.  Most of the observation targets should be green.  If you right-click on the solution in the **Project Explorer** and select **Properties**, you can see a summary of the error.

At this point, you will need to iterate to improve the calibration. You can typically get the RMS error for head to be less than 1-2 ft. You may wish to try the following:

>>a) Change the number and distribution of your pilot points.

>>b) Use manual calibration to tweak your inputs to give you a better, more stable starting point.

>>c) Change the convergence options to avoid problems with dry cells.

>>d) Change the distribution of your recharge polygons (if applicable)

>>e) Change the interpolation option used with the pilot points.

>>f) Change the PEST options.

>>g) Adjust the stream discharge rate assigned to the observed flow field for the river. If you are having trouble getting the heads high enough, increase the observed discharge within the allowable range to get more recharge (or vice versa).

>>etc.
