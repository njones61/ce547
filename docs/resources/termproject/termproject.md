# Term Project

The term project will involve building a groundwater model of the Woburn site described in the book A Civil Action. We will divide the class into eight groups. Each group will build a MODFLOW model of the site and perform a particle tracking analysis. Two groups will represent Beatrice, two groups will represent the plaintiffs against Beatrice, two groups will represent W.R. Grace, and the final two groups will represent the plaintiffs against W.R. Grace. We will focus on one primary issue: flow paths and travel times. Using MODFLOW and MODPATH each group will attempt to prove or disprove that the hydraulic conditions were such that any TCE dumped at the sites could have reached the municipal water wells within the target time frame. At the end of the semester, each group will submit a written report and we will spend three days making presentations and debating the merits of each model.

## Time Issues

The main focus of this project is to address the travel time issue. Using your model, you should be answering the question of whether or not TCE could have traveled from the W.R. Grace or Beatrice facility to wells G&H within the time frame addressed by the court trial. Consider the following comment regarding the jury instructions from Judge Skinner:

>>_"First: Had the plaintiffs established by a preponderance of the evidence that any of the following chemicals - TCE, perc, adn 1,2 transdichloroethylene - were disposed on the Beatrice land after August 27, 1968 (in the case of W.R. Grace, after October 1, 1964, and the date Well G had opened), and had these chemicals substantially contributed to the contamination of the wells before May 22, 1979? If the answer should be yes for one or more of the chemicals, then the second question: What, according to a preponderance of the evidence, was the earliest date - both month and year - at which each of these chemicals had substantially contributed to the contamination of the wells? And then: Had this happened because of the defendants' failure to fulfill any duty of care to the plaintiffs? Finally, if the jurors answered yes to that question, then this puzzler: What, according to a preponderance of the evidence, was the earliest time (again, both the month and year) at which the substantial contribution referred to in question 3 was caused by the negligent conduct of this defendant?" (Harr, 1995)_

Note that there is a specific time range mentioned by the judge. Refer to this time range as you discuss the results of your particle tracking analysis. The max travel time for the W.R. Grace case is about 14.5 years. For Beatrice it would be about 10.5 years. You may argue for applying a shorter time frame that this depending on your point of view. For example, these numbers represent the worst case scenario (the TCE was released at the earliest possible date).

## Web Site

The [Woburn Hydrogeology Data](https://ce547.groups.et.byu.net/woburn/) web site has been established to provide you with data related to the Woburn site.  The data on this site are copies of actual investigations at Woburn. There may be more detail here than you end up using, but it is a good resource that you should explore carefully.

## Teams

The teams will be divided as shown in the following table. The group ids are shown in parentheses.

| W.R. Grace (1)   | 	Plaintiffs vs. Grace (2)        |
|:-----------------|:---------------------------------|
|                  |                                  |
|                  |                                  |
|                  |                                  |
| **Beatrice (3)** | 	**Plaintiffs vs. Beatrice (4)** |
|                  |                                  |
|                  |                                  |
|                  |                                  |

In terms of team management, I expect you to do the following:

1. Elect a team leader
2. Collectively draft a team contract that outlines who will do what. Each team member review and agree to the contract. You should upload your team contract to Learning Suite by the deadline shown in the table below.
3. Try to address participation problems within your group. Use the instructor as a last resort to arbitrate differences.

## Model

To support your viewpoint, you should first build a MODFLOW model. While the USGS model has been provided on the web site for informational purposes, you are not allowed to simply use the USGS model for your model. You need to build a model from scratch. Once you have your initial MODFLOW model built and running, you should then calibrate the model. Once you have calibrated the model and converted it to a predictive model, you can then proceed to the particle tracking analysis.

## Case Study Exercises

I have prepared a series of case study exercises that lead you through the process of building your model of the Woburn site. The purpose of these exercises is to show you how the model could be built. You are under no obligation to follow these steps exactly as you build your model. Feel free to improvise.

| Case Study	                                    | Notes                                                                                                                                            | 	Submission                                                                                                                                                                        |
|------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Case Study #1 - Building the MODFLOW Model]() | 	Covers setting up the initial version of the model,<br> including the background image and conceptual<br> model.                                | 	Upload a *screenshot of the completed model<br> showing head contours.                                                                                                            |
| [Case Study #2 - Calibration]()                | 	Importing the head and flow observations and setting<br> up the calibration process.                                                            | 	Zip and upload a *screenshot of the calibrated<br> model showing the targets and a second<br> screenshot of the error norm summary.                                               |
| [Case Study #3 - Predictive Model]()           | 	Converting the model from calibration mode to forward<br> mode and splitting the model into three layers that<br> match the well screen elevtions. | 	Zip and upload 2-3 *screenshots of the multi-layer<br> model in oblique view with the cell faces turned<br> on. Include a screenshot showing the head<br> contours in plan view.  |
| [Case Study #4 - Particle Tracking]()          | 	Preparing the MODPATH options, importing property<br> boundary polygons and creating particle sets to<br> analyze travel times.                 | 	Zip and upload 2-3 *screenshots of your pathlines.                                                                                                                                |
| [Case Study #5 - Stochastic Analysis]()        | 	Illustrates how to convert your particle tracking<br> model to stochastic mode in order to compute<br> probabilistic capture zones.             | 	(optional - no upload required)                                                                                                                                                   |
| [Case Study #6 - Transient Analysis]()         | 	Describes how to convert your steady state model to<br> a transient model to simulate the seasonal variations<br> in pumping for wells G and H. | 	(optional - no upload required)                                                                                                                                                   |

_*Do not put the screenshots in a word document. Just zip up the image files (JPG, GIF, PNG)._

### Case Study #1 - Building the MODFLOW Model

In this exercise we will import a background image, build the conceptual model, and then build and run a preliminary MODFLOW model for the Woburn site.

#### Importing a background image

The state of Massachusetts provides a wealth of free digital geographic information on their web site.  The USGS quad map of the Woburn area was downloaded in TIFF format from http://www.state.ma.us/mgis/ftpquad.htm.  A sample of the image is shown in Figure 1 below.  Wells G and H are clearly visible.  The image is actually a composite of 2 USGS quad maps



_Figure 1. Background Image of Aberjona Region._

>>1) Right-click and download the case1.zip file. Unzip the file.

>>2) Use the File|Open command to read in the **q233914.tif** file.

Massachusetts also provides a TIFF World File with each TIFF image.  The TIFF World File has the same name as the TIFF file but has a .tfw extension. It contains coordinate system information so that the image can be mapped to real world coordinates. If the .tfw file is in the same folder as the TIFF file (as it is in this case), GMS will find it automatically and use it to locate and scale the image to the correct coordinates.

Next we will set the display projection for our project.

3) Select the Display|Display Projection... command.

4) Select the Global projection option and click on the Set Projection button.

5) Change the projection to Projected Coordinate Systems|State Plane|NAD 1983 (2011) (US Feet)|NAD 1983 (2011) StatePlane Massachusetts FIPS 2001 (US Feet).

6) Make sure the vertical units are set to FEET (U.S. SURVEY) and Click OK.

7) Check the settings in the Edit|Units dialog to make sure the length units are set to ft.

8) Use the File|Save As command to save your project.

Note that the image is busy and contains bright colors. We can make the image more subtle in appearance by adjusting the transparency factor.

9) Right-click on the image (q233914) in the Project Exlorer and select the Transparency item.

10) Change the transparency to about 50% and click OK.

If you wish, you can now add additional basemaps to the project by selecting the File|Add Online Maps... command.

Creating the Conceptual Model Object
Next we will create a conceptual model object and import a boundary converage.

1) Right-click in the Project Explorer and create a new conceptual model object.

We will create a boundary coverage that we can use as a template to build other coverages in order to ensure that each coverage has a consistent boundary. The boundary we will be using is shown in Figure 2. The northern and southern boundaries are parallel flow boundaries, and the east and west boundaries are where the aquifer becomes thin. The Aberjona River runs from north to south through the middle of the model, and flow is primarily downhill towards the river.



Figure 2. Boundaries Used for Model.

To ensure that each group uses a consistent boundary, we will import the boundary from a shapefile.

2) Right-click to download the boundary_arcs.shp file.

3) Use the File|Open command to import the file.

Note that the shapefile is imported as a layer in the GIS module. Next we will create a coverage in the map module and convert the shapefile lines into standard GIS feature objects.

4) Right-click on the conceptual model object and create a new coverage called boundary.

5) Select the boundary_arcs.shp object in the GIS Layers folder in the Project Explorer.

6) Select the Shapes -> Feature Objects command in the GIS menu.

7) Select Yes at the prompt to confirm that we want to use all of the shapes.

8) Click Next on the first page of the wizard.

9) Click Next at the second page. We don't need to import any of the attributes. Just the features.

10) Click Finish to complete the process.

11) Use the zoom tool to zoom in on the region surrounding the model boundary.

At this point we no longer need the shapefile so we will remove it from the project.

11) Right-click on the boundary_arcs.shp item in the Project Explorer and select Delete.

Rivers
Next we will create a coverage for the river arc.

1) Duplicate the boundary coverage to create a new coverage called rivers. Turn on the River attribute.

2) Using the blue line in the background as a guide, create an arc corresponding to the Aberjona River as shown in Figure 3.

3) Select the arc and change the type to River. Also, assign a value of 200 ft^2/day/ft for the Conductance. Recall that for arcs we enter conductance per unit length.

4) Double click on the northern river node and assign 48.0 ft for the Head and 45.0 ft for the Elev.

5) Double click on the southern river node and assign 40.0 ft for the Head and 37.0 ft for the Elev.

6) Delete the arcs on the boundary of the model so that the only arc left in the coverage is the river arc.

Note that the conductance value is an estimate. You may wish to adjust this value during the calibration phase.



Figure 3. The Aberjona River Arc.

Wells
Next, we will create the wells. In addition to wells G & H there are two industrial wells on the Beatrice property (Riley Tannery).

1) Duplicate the boundary coverage to create a new coverage called wells. Turn on the Wells and Refine points attribute.

2) Right click on the rivers-wells coverage and select the Attribute Table command.  Make sure that the Feature type listed near the top of the dialog is set to Points.

3) Create four new points by selecting the Add Point button four times.

4) Toggle on the Show point coordinates option and enter the point attributes shown in Table 1.

5) Turn on the Refine option for all wells, and enter the following options for all four points:

Base size = 40 ft
Bias = 1.1
Max size = 120 ft

Note that these pumping rates for the industrial wells represent the average annual pumping rates converted to units of [ft^3/day]. The rates for wells G&H were are set to zero because the wells were turned off during the period that the calibration data were collected. We will build the model and calibrate it with the two wells off and then enter a non-zero pumping rate prior to the prediction (particle tracking) phase.

Name	X	Y	Z	Type	Flow Rate
G	755879.0	3005310.0	46.5	well	0
H	755702.0	3005897.0	46.5	well	0
IW1	755442.0	3004227.0	16.0	well	-13406.0
IW2	755845.0	3003893.0	5.0	well	-38304.0
Table 1. Data for Wells G&H and the Two Industrial Wells.

Recharge
Next, we will create a recharge coverage.

1) Duplicate the boundary coverage to create a new coverage called recharge. Turn on the Recharge rate attribute.

2) Build polygons.

3) Double-click the polygon and enter a recharge rate of 0.004 ft/day.

Once again, this is an estimate that you may wish to adjust during the calibration phase.

Active Region
Finally, we need a polygon coverage to define the active region of our model.

1) Duplicate the boundary coverage to create a new coverage called active zone.

2) Open the Coverage Setup dialog and make sure the Use to define model boundary (active area) option is turned on.

3) Build polygons.

Building the Grid
We will now build the computational grid and initialize MODFLOW.

1) Create a grid frame and fit it to your grid. You may wish to rotate the grid to align it with the upper boundary.

2) Double-click on the grid frame and change the Origin z value to -60 and set the Dimension z value to 180.

2) Create a 3D grid.

3) Initialize the MODFLOW simulation.

4) Use the Activate Cells in Coverage command to inactivate the cells outside the model boundary.

5) Select the Map -> MODFLOW command.

MODFLOW Properties
Next we will assign starting head and hydraulic conductivity values to the grid cells. We will use a constant value for K for now, but during the calibration phase we will use the pilot point method to interpolate K values.

1) Enter starting head = 150 for all cells.

2) Enter K = 15 for all cells.

Layer Elevations
The final step before running the model is to interpolate a set of top and bottom elevations. To do this, we will download a file containing a scatter point set with both ground surface and bedrock elevations. 

1) Download the elevations.txt file (use the Save Link As.. option in your browser).

2) Use the File|Open command to open the file and follow the steps in the Import Wizard.

Before interpolating we need to change the interpolation option. For some reason the top and bottom elevations from elevations.txt cannot be interpolated using the IDW-Gradient Plane method (the default).

3) Open the Interpolation Options dialog and change the IDW Nodal function sub-option to Constant (Shepard's Method).

3) Use the Interpolate to MODFLOW Layers command to interpolation the elevations to the top and bottom elevations arrays for layer 1.

4) Contour your top and bottom elevations arrays to check your results.

Save and Run MODFLOW
We are now ready to save and run MODFLOW.

1) Run the Check Simulation command to see if you have any obvious errors.

2) Save your project and run MODFLOW.

Note that you may end up with some flooded cells and some dry cells. You can adjust the model inputs and do some manual calibration to get better results if you wish.

## Report

Each team will be required to submit a written report on the modeling project. I expect each report to be at least twenty pages long. At a minimum, you should describe the assumptions you made and the procedures you modeled in developing your model, you should describe the calibration process, the particle tracking results, and the conclusions you made. Be sure to present your results in relation to the [travel time question](https://byu-ce547.readthedocs.io/en/latest/resources/termproject/#time-issues).

You will be given freedom to organize and format the report any way you wish. Your report should be as professional as possible. The report should be prepared and uploaded in **MS Word** format.

Please write your report in **first person narrative.** For example, instead of saying "the model was then calibrated", you should say "we then calibrated the model".

## Presentation

Each group will be given part of a class period to make an oral presentation of the results. This will take two periods.

For the presentation, I would like you to prepare a PowerPoint presentation. Upload your Powerpoint by the deadline so that I can make sure it is set up properly.

Make your presentation last 15 minutes. This will leave a few minutes for Q/A.

## Grading

The term project is worth 22% of your grade. I will assign a grade to each team based on my evaluation of the written report and the oral presentations. The term project score is broken down as follows:

### 1) Model development milestones (15%)

Please keep in mind the following milestones. For each item, the completed item (document, spreadsheet, etc.) should be uploaded into Learning Suite. See the schedule for due dates.

| Part  |      	Value       | 	Item Due                                      |
|:-----:|:-----------------:|:-----------------------------------------------|
|  a.   |      	3 pts       | 	Team contract                                 |
|  b.   |      	3 pts       | 	Working flow model (case study #1)            |
|  c.   |      	3 pts       | 	Calibrated flow model (case study #2)         |
|  d.   |      	3 pts       | 	Predictive model (case study #3)              |
|  e.   |      	3 pts       | 	Particle tracking analysis (case study #4)    |
|  f.   |      	73 pts      | 	Written project report                        |
|  g.   |      	12 pts      | 	Oral report                                   |

All items should be uploaded by due date shown using Learning Suite.

### 2) Oral report (12%)

Presentations should be professional, informative, and cover the basic features of your project. Keep your introductions brief since we are all quite familiar with the background information on the Woburn case. Make sure you cover all of the primary assumptions you made when building the model. Explain your calibration results and the results of your particle tracking analysis. Describe any special types of analysis that you considered.

### 3) Written report (73%)

a) Quality of writing, graphics, and organization (23 pts)

Be sure to proof several times to remove spelling and grammar errors. Assume your audience is familiar with groundwater modeling but don't assume that they are experts on the GMS interface. In other words, don't spend time explaining details unique to GMS such as what coverages you used, what menu commands you selected, etc.

b) Completion of basic modeling steps required (18 pts)

Be sure to fully document what you did and the assumptions you made. Include a full set of error norms for your final calibrated model. Also be sure to list/graph your final optimal values for recharge and K.

c) Thoroughness and rigor with respect to exploration and analysis of model results (32 pts)

In this case I am looking to see what you did to explore your model once it was constructed. How thoroughly did you investigate the particle tracking results? This includes (but is certainly not limited to) how you dealt with modeling assumptions such as recharge, the manner in which you analyzed your calibration results, how you selected your ranges and starting values for parameters, sensitivity analyses, risk assessment (stochastic analyses), transient factors, etc.


