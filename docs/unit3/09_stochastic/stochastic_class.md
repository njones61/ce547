# Stochastic Simulations - Big Valley

For this exercise we will revisit the Big Valley model and perform a stochastic simulation.

Do the following:

1. Download and unzip stochastic.zip if necessary.  Open start.gpr
2. Change the MODFLOW Run Option in the Global/Basic Package dialog to Stochastic Simulation
3. Check the settings in the Stochastic Options dialog.
4. Parameter Randomization
Go to Parameters dialog
Randomize both the K fields and the recharge fields.
Make sure that Log Xform is turned ON for K, but OFF for recharge.
Change the standard deviation for K fields to 0.3 log cycles.
Change the standard deviation for recharge fields to 0.00001.
Change to random sampling
50 instances
Save and run as montecarlo-1
Browse through the folder of solutions. Click on individual solution folders to update contours.
Right-click on folder of solutions and select Statistical Analysis.  View mean head, etc.
Review Latin Hypercube distributions/options in the Parameters dialog.  No need to run another model.
5. Gaussian Simulation
Create a dummy, empty scatter point set. Rename it to gauss points.
Select the Interpolation|Gaussian Simulation Options command.
Log interpolation
50 realizations (this number is extremely low - for demo purposes only)
Truncate 0.001 to 200
Mean = 0.4
Variogram
Range = 700-1000
Contribution = 0.3
Nugget = 0
Select the Run Gaussian Simulation command.
Turn on log contouring
Contouring Options.
Use the Populate Values button and turn on the Log Scale option.
Run MODFLOW
Change all K polygons to -100 key value
Map -> MODFLOW
Delete all of the HK_XXX parameters except for HK_100
Turn on Use multiplier arrays option.
Change Multiplier option for HK_100 to Mult. Arrays. Make sure you have NOT selected Latin Hypercube or you won't be able to see this option.
Use the Data Set(s) button to select gaussian folder. Note run configuration at bottom.
Save and run as montecarlo-2.gpr.
Reset contour options and browse through folder of solutions.
Probabilistic Capture Zone Analysis
Right-click on one of the stochastic solutions and select Risk Analysis.
Probabilitistic capture zone analysis.
Next.
Stop in cells with weak sinks.
Review placement options. One particle per cell is faster, but more particles can give you a cleaner capture zone.
Weight results based on residual error.
Finish.
Select each of the three data sets generated to view. Each one represents probability of capture for a particular well.
Change contour options
Contour specified range.
Change lower limit to 0.1 and turn off the Fill below option.
Note: If you get an error message when running the gaussian simulator, it could be a permissions problem when running the gaussian simulator on CAEDM. It tries to write a temp scratch file and it can't. To solve the problem, copy the FIELDGEN.EXE file to a local drive and change the path to the file using the Edit|Preferences dialog. You can see the current location of FIELDGEN.EXE using the Edit|Preferences dialog.

 

 
 