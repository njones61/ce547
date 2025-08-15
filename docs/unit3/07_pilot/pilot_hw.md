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

Save the GMS project with the completed solution. Zip up all files associated with the project.

Name your zip folder `pilot_hw.zip` and upload it on Learning Suite after we grade it together in class.

## Grading Rubric

Self-grade your assignment using the following rubric. Enter your points in the "Submission notes" section for the assignment on Learning Suite when you upload your file. You can use fractional points if you like (e.g. 2.5).

| Criteria                                    | Points |
|---------------------------------------------|:------:|
| Completed on time and all or mostly correct |   3    |
| Completed more than half of assignment      |   2    |
| Made an effort                              |   1    |
| Did nothing                                 |   0    |
