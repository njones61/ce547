# Homework #12 - Pilot Point Calibration

_Note: You may work in pairs on this assignment._

Solve the following problem.

In this exercise we will start with the same project we used in the previous assignment:

![easttexsimp2 (1).gif](images/easttexsimp2%20%281%29.gif)

However, this time we will use the pilot point approach to calibrate the model. The pilot points will be associated with the hydraulic conductivity parameter for layer 1. For the other two parameters, we will once again use a simple zonal approach. Before you begin, download the following zip archive:

>>[<u>start.zip</u>](start.zip)

You will need to unzip the files after you download them. Then do the following:

1) Create a new 2D scatter point set called **ppts.**

2) Go to the **Edit|Preferences** dialog, select the **Scatter points** section, and set the default scatter point value to **1.0.**

3) Use the **Create Point** tool to create a set of pilot points. Follow the placement guidelines we discussed in class. 30-50 points should be plenty. NOTE: You are welcome to use the grid-based distribution technique if you like.

4) Go to the **Map Module** and enter key values for the following parameters:

>>Kh in layer 1<br>
>>Kh in layer 2<br>
>>Recharge (big polygon - don't worry about landfill)

>>Be sure to select the **Map -> MODFLOW** command. Also, note the current values of Kh and Recharge before you enter the key values so you can enter them later as starting parameter values.

5) Go to the **Global Options** dialog and change the run mode to **Parameter Estimation.**

6) Go to the **Parameters** dialog in the MODFLOW menu and set up your list of parameters. Mark the **Solve** toggle for each of the three parameters. For the parameter corresponding to Kh in layer 1, turn on the pilot point option, select the **ppts** scatter point set, and turn on log interpolation. Enter a starting value for the other two parameters. Enter a reasonable set of min/max values for the parameters. Turn on the **log transform** option for all parameters.

7) Save and run the model. Read in the solution and view your results. Compare to your manual solution and your first PEST solution.

**NOTE:** If you have trouble getting a good solution, switch your model to forward mode and make sure it runs correctly using the parameter values you have defined.

## Submission

Save the GMS project with the completed solution. Zip up all files associated with the project and upload the zip file to Learning Suite.

!!! note "Do not put your name or NetID in the file"
    Learning Suite records who submitted each file, so your name is not needed
    inside the file itself. This applies to scans and photos too — please
    don't write your name on the page.

## Grading Rubric

**Total: 30 points**

| Criteria                                                                 | Points |
|--------------------------------------------------------------------------|:------:|
| Pilot point scatter set created with reasonable placement (30-50 points) |   8    |
| Key values entered for the three parameters and mapped to MODFLOW        |   5    |
| Run mode set to parameter estimation                                     |   2    |
| Kh in layer 1 tied to the pilot point set with log interpolation         |   6    |
| Reasonable starting values and min/max limits with log transform enabled |   5    |
| Model runs and produces a calibrated solution                            |   4    |
