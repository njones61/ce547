# Homework #11 - Automated Parameter Estimation

_Note: You may work in pairs on this assignment._

Solve the following problems.

In this exercise we will first read in a MODFLOW model corresponding to the previous homework assignment (manual calibration). However, in this case the head and flow observations are already assigned to the model. We will then calibrate the model using PEST.

![easttexsimp2.gif](easttexsimp2.gif)

Before you begin, download the following zip archive:

>>[<u>start.zip</u>](start.zip)

You will need to unzip the files after you download them. Then do the following:

1) Go into the MODFLOW Global Options and set the run option to **parameter estimation** mode.

2) Go to the Map Module and enter key values for the following parameters:

>>Kh in layer 1<br>
>>Kh in layer 2<br>
>>Recharge (big polygon - don't worry about landfill)

3) Select the **Map->MODFLOW** command to map your key values to the grid

4) Go to the Parameters dialog in the MODFLOW menu and set up your list of parameters. Enter a starting value and mark the Solve toggle for each of the three parameters. Turn on the log transform option.

5) Save and run the model. Read in the solution and view your results. Compare to your manual solution. Did the PEST solution do better or worse than your manual solution?

6) Open up the *.MTT file and compare the max to min Eigenvalues. Do you think you have a unique solution?

Create a Word document named results.doc to discuss your results for items 5-6.

## Submission

Save the GMS project with the completed solution. Zip up all files associated with the project, **including the Word document,** and upload the zip file to Learning Suite.

!!! note "Do not put your name or NetID in the file"
    Learning Suite records who submitted each file, so your name is not needed
    inside the file itself. This applies to scans and photos too — please
    don't write your name on the page.

## Grading Rubric

**Total: 30 points**

| Criteria                                                                        | Points |
|---------------------------------------------------------------------------------|:------:|
| Run option set to parameter estimation mode                                     |   3    |
| Key values entered for the three parameters and mapped to the grid              |   6    |
| Parameters dialog set up with starting values, Solve toggles, and log transform |   6    |
| Model run and PEST solution read in successfully                                |   5    |
| Discussion comparing the PEST solution to the manual calibration                |   5    |
| Eigenvalue ratio from the *.MTT file with a discussion of uniqueness            |   5    |
