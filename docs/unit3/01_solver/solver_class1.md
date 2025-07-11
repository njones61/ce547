# MODFLOW Case Study - Solver Problems with a Thin Aquifer

This exercise involves a variation of the [<u>Fremont River</u>](https://byu-ce547.readthedocs.io/en/latest/unit2/03_optional_packages/optional_packages_class/) model. The following changes have been made to the original model:

- The hydraulic conductivity has been increased to 1.5 m/d.
- The two wells have been turned off
- Rather than using a flat bottom, a new set of bottom elevations has been interpolated from a set of scatter points. This results in a surface that slopes up to the west side.

1) Download and unzip the [<u>thinaq.zip</u>](thinaq.zip) file.

2) Save and run the model. Read the solution.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) What do the red symbols mean?

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Why did this happen?

3) Try fixing the problem by adjusting the starting heads to a larger value. Turn on the **_Starting heads equal grid top elevations_** option in the **Global/Basic** package dialog. Or just change the starting heads to 400.

4) Try fixing the problem by adjusting the acceleration/damping* parameter and/or trying a different solver.

5) Try changing the starting head value to be just above the bottom elevation. You will to turn off the **_Starting heads equal grid top elevations_** option before you can edit the starting heads again.

6) Change the starting heads to a constant value such as 400. Switch to MODFLOW-NWT and turn on the Newton solver.

_*For the PCG2 solver, the acceleration parameter is called the damping parameter._

 