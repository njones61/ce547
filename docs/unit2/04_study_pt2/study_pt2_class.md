# MODFLOW Case Study - Agricultural Drain Model, Part 3

In this exercise, we will revisit the agricultural drain model we built for our previous in-class task.

![planview.gif](planview.gif)

Click [<u>here</u>](agdrains2.zip) to download a completed version of the previous model. Unzip the model and load it into GMS. Then do the following:

## Part 1 - General Head Boundary (GHB) Package

For this part of the exercise, we will add a pond to the model using the GHB package. The pond will be located in the middle of the model domain and will represent an irrigation pond that is used to store water for irrigation. The pond will be represented as a GHB with a specified head and conductance.

1) Turn off the display of the CAD objects (or delete them)..

2) Select some cells in the middle and add an irrigation pond using the GHB package. Let the elevation = 3830 and use a large value for conductance (2000 ft^2/day). Note: using a larger value of conductance such as 1e6 leads to a model that will converge but it has mass balance errors.

3) Save and run. Look at heads and flow budget.

4) Compute a conductance assuming pond is lined with a K=0.01 ft/day material with thickness= 1 ft. Save and run. What is the impact on heads and flow budget?

## Part 2 - Evapotranspiration (EVT) Package

This site has a high water table that is close to the ground surface. For this part of the exercise, we will add evapotranspiration to the model using the EVT package. The evapotranspiration will be applied to the top layer of the model and will represent the loss of water due to evaporation and transpiration.

1) Note that the top elevation is 3832 ft. Move your cursor around the model domain and note the depth to water table. 

2) Add the EVT package to the model. Use a maximum ET rate of 0.005 ft/day and a depth of extinction of 5 ft. Apply the EVT to the entire top layer.

3) Save and run. Look at heads and flow budget. What is the impact of adding EVT to the model?

4) Change the depth of extinction to 2 ft. Save and run. What is the impact on heads and flow budget?

## Solution

Step-by-step instructions with screen shots: [<u>Agricultural Drains, Part 3.pptx</u>](Agricultural%20Drains%2C%20Part%203.pptx)

GMS project file with final version of model: [<u>agdrains3.zip</u>](agdrains3.zip)

Video: [<u>www.youtube.com/watch?v=EFG0KVHS2q8</u>](https://www.youtube.com/watch?v=EFG0KVHS2q8)