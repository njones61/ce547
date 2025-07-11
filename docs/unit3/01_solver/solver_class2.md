# MODFLOW Case Study - Dealing with Dry Cells

This exercise involves a variation of the [<u>Fremont River</u>](https://byu-ce547.readthedocs.io/en/latest/unit2/03_optional_packages/optional_packages_class/) model. The model is the same as before, except that the bottom elevations have been changed from 250 m to 280 m.

1) Download and unzip the [<u>drywells.zip</u>](drywells.zip) file.

2) Save and run the model. Read the solution.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) What has happened to the wells?

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Why did this happen?

3) Try fixing the problem by adjusting the acceleration/damping* parameter in the solver.

4) Try using another solver.

5) Try increasing the K value in the cells containing the wells.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Why did this work?

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Is this a legitimate (defensible) approach?

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c) Can you think of any other strategies that may solve the problem?

6) Change the K values in the cells back to the original values and then:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Switch to MODFLOW-NWT and turn on the Newton solver. Run the model.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) If it doesn't converge - go into the NWT solver dialog and change the options from SIMPLE to COMPLEX. Note what happens to the **Coefficient to reduce weight applied to head change (DBDTHETA)** value. This is the "acceleration parameter" for this solver. Run the model.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c) Did the cells go dry?

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d) Look at the flow budget. Notice anything different?

7) Right-click on the two wells and bring up the Sources/Sinks dialog. Change each well from WEL to MNW2 (delete WEL and add MNW2). Enter the pumping rate in the QDES field. Use default values for everything else. Save and run

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Did the cells go dry?

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Look at the flow budget. Notice anything different?

_*For the PCG2 solver, the acceleration parameter is called the damping parameter._

 

 

 

 