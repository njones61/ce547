# MODFLOW Case Study - Agricultural Drains

Drains are sometimes used in agricultual regions with high water tables. Drains are thought to create a healthier environment for plant growth and to dry the soil so that it can be accessed by farm equipment throughout the crop production cycle. Drainage can also reduce saline-alkiline problems.

One type of agricultural drain is a simple trench as shown below. The drain acts as a fixed head boundary.

![drainfig.gif](images/drainfig.gif)

The objective of this exercise is to build a MODFLOW model to simulate the lowering of the water table at a farm as a result of two parallel agricultural drains constructed as trenches. The problem details are shown in the following figure. We will assume that the fields and drain continue to the north and south and we will assume parallel flow boundaries at the north and south ends.

![planview.gif](images/planview.gif)

**Main Steps**

1) Build the grid

3) Initialize MODFLOW and turn on the Recharge package

4) Assign K value to all cells

5) Assign recharge value to all cells

6) Make specified head boundaries on two sides

7) Save project

8) Run MODFLOW

9) View Solution


# MODFLOW Case Study - Agricultural Drain Model, Part 2

In this exercise, we will revisit the agricultural drain model we built for our previous in-class task.

![planview.gif](images/planview.gif)

Click [here](agdrains1.zip) to download a completed version of the previous model. Unzip the model and load it into GMS. Then do the following:

1) Add a well in the interior.

&nbsp;&nbsp;&nbsp;&nbsp;a) Use Q = -2000 ft^3/day

&nbsp;&nbsp;&nbsp;&nbsp;b) Use Q = -5000 ft^3/day

2) Analyze the flow budget

&nbsp;&nbsp;&nbsp;&nbsp;a) Select the cells on each side and change the zone budget id's. Use 2 on the left and 3 on the right.

&nbsp;&nbsp;&nbsp;&nbsp;b) Look at the flow budget. What percentage of the water goes to the left drain vs. the right drain?

&nbsp;&nbsp;&nbsp;&nbsp;c) Remove the well and re-run the model to get the original solution. Look at the flow budget again.

3) Determine impact of using a 2D model

&nbsp;&nbsp;&nbsp;&nbsp;a) Set the head contours to a fixed interval (1.0) and save a copy of the contours to a CAD layer.

&nbsp;&nbsp;&nbsp;&nbsp;b) Rebuild the model using a multi-layer grid (six layers). Assign head bc to top layer only and re-enter the inputs in the same order used in the first exercise. Let Kv=Kh for now.

&nbsp;&nbsp;&nbsp;&nbsp;c) Compare the contours. Is there a significant difference?

&nbsp;&nbsp;&nbsp;&nbsp;d) Has the flow budget changed?

4) Determine impact of vertical anisotropy

&nbsp;&nbsp;&nbsp;&nbsp;a) Save another copy of head contours.

&nbsp;&nbsp;&nbsp;&nbsp;b) Change Kv=Kh/5=0.8.

&nbsp;&nbsp;&nbsp;&nbsp;c) Save and run the model. Compare the solution.

5) Determine impact of using drains vs. constant head bc for ag drains.

&nbsp;&nbsp;&nbsp;&nbsp;a) Save another copy of head contours. Note the flow budget.

&nbsp;&nbsp;&nbsp;&nbsp;b) Remove fixed head BC and add drains to left and right side. Use a large value for conductance (1e6).

&nbsp;&nbsp;&nbsp;&nbsp;c) Save and run. Compare results.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note: You may need to reduce the acceleration (relaxation) parameter to get the PCG solver to converge. Try reducing from 1.0 to 0.2 in the PCG Package dialog.

&nbsp;&nbsp;&nbsp;&nbsp;d) Compute a drain conductance value assuming K=0.5, L=50, width=6, thickness=3. Enter CD, save and run again. Compare results.

 

 
 

 
