# MODFLOW Case Study, Part 1 - Solver Problems with a Thin Aquifer

This exercise involves a variation of the [<u>Fremont River</u>](https://byu-ce547.readthedocs.io/en/latest/unit2/03_optional_packages/optional_packages_class/) model. The following changes have been made to the original model:

- The hydraulic conductivity has been increased to 1.5 m/d.
- The two wells have been turned off
- Rather than using a flat bottom, a new set of bottom elevations has been interpolated from a set of scatter points. This results in a surface that slopes up to the west side.

1) Download and unzip the [<u>thinaq.zip</u>](thinaq.zip) file.

2) Save and run the model. Read the solution.<br>
>a) What do the red symbols mean?<br>
>b) Why did this happen?

3) Try fixing the problem by adjusting the starting heads to a larger value. Turn on the **_Starting heads equal grid top elevations_** option in the **Global/Basic** package dialog. Or just change the starting heads to 400.

4) Try fixing the problem by adjusting the acceleration/damping* parameter and/or trying a different solver.

5) Try changing the starting head value to be just above the bottom elevation. You will to turn off the **_Starting heads equal grid top elevations_** option before you can edit the starting heads again.

6) Change the starting heads to a constant value such as 400. Switch to MODFLOW-NWT and turn on the Newton solver.

_*For the PCG2 solver, the acceleration parameter is called the damping parameter._

# MODFLOW Case Study, Part 2 - Dealing with Dry Cells

This exercise involves a variation of the [<u>Fremont River</u>](https://byu-ce547.readthedocs.io/en/latest/unit2/03_optional_packages/optional_packages_class/) model. The model is the same as before, except that the bottom elevations have been changed from 250 m to 280 m.

1) Download and unzip the [<u>drywells.zip</u>](drywells.zip) file.

2) Save and run the model. Read the solution.<br>
>a) What has happened to the wells?<br>
>b) Why did this happen?

3) Try fixing the problem by adjusting the acceleration/damping* parameter in the solver.

4) Try using another solver.

5) Try increasing the K value in the cells containing the wells.<br>
>a) Why did this work?<br>
>b) Is this a legitimate (defensible) approach?<br>
>c) Can you think of any other strategies that may solve the problem?

6) Change the K values in the cells back to the original values and then:<br>
>a) Switch to MODFLOW-NWT and turn on the Newton solver. Run the model.<br>
>b) If it doesn't converge - go into the NWT solver dialog and change the options from SIMPLE to COMPLEX. Note what happens to the **Coefficient to reduce weight applied to head change (DBDTHETA)** value. This is the "acceleration parameter" for this solver. Run the model.<br>
>c) Did the cells go dry?<br>
>d) Look at the flow budget. Notice anything different?

7) Right-click on the two wells and bring up the Sources/Sinks dialog. Change each well from WEL to MNW2 (delete WEL and add MNW2). Enter the pumping rate in the QDES field. Use default values for everything else. Save and run<br>
>a) Did the cells go dry?<br>
>b) Look at the flow budget. Notice anything different?

_*For the PCG2 solver, the acceleration parameter is called the damping parameter._

