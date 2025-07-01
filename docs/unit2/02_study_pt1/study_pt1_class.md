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

 

 
