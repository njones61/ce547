# Boundary Condition Analysis

This exercise involves experimenting with a model similar to the local scale industrial plant model highlighted in the lecture notes.

Do the following:

1) Download and unzip the following file. Open the project in GMS.

>[<u>bcanalysis.zip</u>](bcanalysis.zip)

2) Look at the conceptual model.

>a) Note the boundary conditions that have been applied on the two ends of the model.<br>
>b) Note the total model error for the current solution.<br>
>c) Note the flow budget values.<br>
>d) Note the travel time for the particles/pathlines.

## Model Uniqueness

3) Decrease the hydraulic conductivity by a factor of **10** (set K=1). Save the model as **plant2_K1.gpr** and re-run the model.

4) After reading in the solution, examine the head contours and the total residual error. Is it substantially different? Why not?

5) If the heads are the same, what is the difference between the two solutions?

6) What could you do to determine which model (or what value of K) would be most appropriate?

## Head/Flow Boundary Conditions

7) Change the K back to the original value (K=10) and save the model as **plant2_HF.gpr** and re-run the model.

8) Bring up the flow budget dialog and determine how much water is going out the right side (-5538).

9) Double-click on the main coverage in the map module and add **Specified Flow** as an attribute. This creates a set of pseudo-wells along the boundary to force a specified discharge of water along the boundary. 

10) Double-click on the arc on the right boundary of the model and change it to specified flow at the rate you determined.

11) Run the **Map -> MODFLOW** command and save and run the model.

12) Read the solution and look at the flow budget and travel times. Has the model changed?

**NOTE:** The pathline travel times become random with this solution. To fix this, select **MODPATH|General Options** and select the Stop in cells with weak sinks option. Then you should notice the same travel times as before.

13) Decrease the hydraulic conductivity by a factor of **10** (set K=1). Save the model as **plant2_HFK1.gpr** and re-run the model.

14) Now look at the heads, observation wells, and model error. What has changed?

**Note**: If you somehow knew (or estimated) the discharge on the boundary, you could now iteratively change the K in the model until the heads matched the observations. In this case that would happen when K=10. 

## Solution

GMS project file with solution: [<u>bcanalysis-key.zip</u>](bcanalysis-key.zip)

Step-by-step instructions: [<u>bcanalysis-script.pptx</u>](bcanalysis-script.pptx)

Video: [<u>www.youtube.com/watch?v=yLbIhwaMQgg</u>](https://www.youtube.com/watch?v=yLbIhwaMQgg)

 