# Homework #5 - MODFLOW Grid Approach, Part 1

_Note: You may work in pairs on this assignment._

Solve the following problem. 

Set up the groundwater model shown below. The problem is a simple single layer model with a single injection well and a single extraction well. The problem is as follows:

![mfgrid.gif](images%2Fmfgrid.gif)

Set up and perform a steady state simulation using the values shown.

1\. Generate a grid using the Create Grid dialog and initialize the MODFLOW simulation.

2\. Use the Global Options dialog to:
>a) select the packages you will be using, <br>
b) set up the starting heads (or confirm that starting heads = top of grid option is selected). <br>
c) set the top and bottom elevation (if necessary - this can be done with create grid dialog). <br>

3\. Use the LPF Package dialog to assign the hydraulic conductivity.

4\. Use the Point Source/Sink command to define the wells.

5\. Run the Model Checker and fix any errors you find.

6\. Save the simulation.

7\. Run MODFLOW.

8\. Examine the solution. Note the shape of the water table as depicted by the head contours.

9\. At this point, you may wish to experiment with the model by
>a) changing the pumping rates, <br>
b) changing the K values (change the global value or try setting up zones of differing K)

## Submission

Save the GMS project with the completed solution. Zip up all files associated with the project and upload the zip file to Learning Suite.

!!! note "Do not put your name or NetID in the file"
    Learning Suite records who submitted each file, so your name is not needed
    inside the file itself. This applies to scans and photos too — please
    don't write your name on the page.

## Grading Rubric

**Total: 30 points**

| Criteria                                                                  | Points |
|---------------------------------------------------------------------------|:------:|
| Grid created with the correct dimensions and MODFLOW initialized          |   5    |
| Global options: packages, starting heads, top and bottom elevations       |   5    |
| Hydraulic conductivity assigned in the LPF package                        |   5    |
| Injection and extraction wells defined at the correct locations and rates |   6    |
| Model checker run and all errors resolved                                 |   5    |
| Simulation saved with a converged solution and reasonable head contours   |   4    |
