# Homework - MODFLOW Grid Approach, Part 1

*Note: You may work in pairs on this assignment.*

Solve the following problems. 

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

9\.At this point, you may wish to experiment with the model by
>a) changing the pumping rates, <br>
b) changing the K values (change the global value or try setting up zones of differing K)


## Submission

Save your work in a file named `_hw.xlsx` and upload it on Learning Suite after we grade it together in class.

## Grading Rubric

Self-grade your assignment using the following rubric. Enter your points in the "Submission notes" section for the assignment on Learning Suite when you upload your file. You can use fractional points if you like (e.g. 2.5).

| Criteria                                    | Points |
|---------------------------------------------|:------:|
| Completed on time and all or mostly correct |   3    |
| Completed more than half of assignment      |   2    |
| Made an effort                              |   1    |
| Did nothing                                 |   0    |
