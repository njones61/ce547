# Case Study #1 - Building the MODFLOW Model

In this exercise we will import a background image, build the conceptual model, and then build and run a preliminary MODFLOW model for the Woburn site.

## Importing a background image

The state of Massachusetts provides a wealth of free digital geographic information on their web site.  The USGS quad map of the Woburn area was downloaded in TIFF format from http://www.state.ma.us/mgis/ftpquad.htm.  A sample of the image is shown in Figure 1 below.  Wells G and H are clearly visible.  The image is actually a composite of 2 USGS quad maps

![mapthumbnail.gif](case_study_1/mapthumbnail.gif)

_Figure 1. Background Image of Aberjona Region._

>>1) Right-click and download the [<u>case1.zip</u>](case_study_1/case1.zip) file. Unzip the file.

>>2) Use the File|Open command to read in the **q233914.tif** file.

Massachusetts also provides a TIFF World File with each TIFF image.  The TIFF World File has the same name as the TIFF file but has a .tfw extension. It contains coordinate system information so that the image can be mapped to real world coordinates. If the .tfw file is in the same folder as the TIFF file (as it is in this case), GMS will find it automatically and use it to locate and scale the image to the correct coordinates.

Next we will set the display projection for our project.

>>3) Select the **Display|Display Projection...** command.

>>4) Select the **Global projection** option and click on the **Set Projection** button.

>>5) Change the projection to **Projected Coordinate Systems|State Plane|NAD 1983 (2011) (US Feet)|NAD 1983 (2011) StatePlane Massachusetts FIPS 2001 (US Feet).**

>>6) Make sure the vertical units are set to **FEET (U.S. SURVEY)** and Click **OK.**

>>7) Check the settings in the **Edit|Units** dialog to make sure the length units are set to **ft.**

>>8) Use the **File|Save As** command to save your project.

Note that the image is busy and contains bright colors. We can make the image more subtle in appearance by adjusting the transparency factor.

>>9) Right-click on the image (q233914) in the **Project Explorer** and select the **Transparency** item.

>>10) Change the transparency to about **50%** and click **OK**.

If you wish, you can now add additional basemaps to the project by selecting the **File|Add Online Maps...** command.

## Creating the Conceptual Model Object

Next we will create a conceptual model object and import a boundary converage.

>>1) Right-click in the **Project Explorer** and create a new conceptual model object.

We will create a boundary coverage that we can use as a template to build other coverages in order to ensure that each coverage has a consistent boundary. The boundary we will be using is shown in Figure 2. The northern and southern boundaries are parallel flow boundaries, and the east and west boundaries are where the aquifer becomes thin. The Aberjona River runs from north to south through the middle of the model, and flow is primarily downhill towards the river.

![boundary.gif](case_study_1/boundary.gif)

_Figure 2. Boundaries Used for Model._

To ensure that each group uses a consistent boundary, we will import the boundary from a shapefile.

>>2) Right-click to download the [<u>boundary_arcs.shp</u>](case_study_1/boundary_arcs.shp) file.

>>3) Use the **File|Open** command to import the file.

Note that the shapefile is imported as a layer in the GIS module. Next we will create a coverage in the map module and convert the shapefile lines into standard GIS feature objects.

>>4) Right-click on the conceptual model object and create a new coverage called **boundary.**

>>5) Select the **boundary_arcs.shp** object in the **GIS Layers** folder in the **Project Explorer.**

>>6) Select the **Shapes -> Feature Objects** command in the **GIS** menu.

>>7) Select Yes at the prompt to confirm that we want to use all of the shapes.

>>8) Click Next on the first page of the wizard.

>>9) Click Next at the second page. We don't need to import any of the attributes. Just the features.

>>10) Click **Finish** to complete the process.

>>11) Use the zoom tool to zoom in on the region surrounding the model boundary.

At this point we no longer need the shapefile so we will remove it from the project.

>>12) Right-click on the **boundary_arcs.shp** item in the Project Explorer and select Delete.

## Rivers

Next we will create a coverage for the river arc.

>>1) Duplicate the **boundary** coverage to create a new coverage called **rivers.** Turn on the **River** attribute.

>>2) Using the blue line in the background as a guide, create an arc corresponding to the Aberjona River as shown in Figure 3.

>>3) Select the arc and change the type to **River**. Also, assign a value of **200** ft^2/day/ft for the **Conductance**. Recall that for arcs we enter conductance per unit length.

>>4) Double click on the northern river node and assign **48.0** ft for the **Head** and **45.0** ft for the **Elev**.

>>5) Double click on the southern river node and assign **40.0** ft for the **Head** and **37.0** ft for the **Elev**.

>>6) Delete the arcs on the boundary of the model so that the only arc left in the coverage is the river arc.

Note that the conductance value is an estimate. You may wish to adjust this value during the calibration phase.

![river.gif](case_study_1/river.gif)

Figure 3. The Aberjona River Arc.

## Wells

Next, we will create the wells. In addition to wells G & H there are two industrial wells on the Beatrice property (Riley Tannery).

>>1) Duplicate the **boundary** coverage to create a new coverage called **wells**. Turn on the **Wells** and **Refine points** attribute.

>>2) Right click on the **rivers-wells** coverage and select the **Attribute Table** command.  Make sure that the **Feature** type listed near the top of the dialog is set to **Points**.

>>3) Create four new points by selecting the **Add Point** button four times.

>>4) Toggle on the **Show point coordinates** option and enter the point attributes shown in Table 1.

>>5) Turn on the **Refine** option for all wells, and enter the following options for all four points:

>>>>Base size = **40** ft<br>
>>>>Bias = **1.1**<br>
>>>>Max size = **120** ft

Note that these pumping rates for the industrial wells represent the average annual pumping rates converted to units of [ft^3/day]. The rates for wells G&H were are set to zero because the wells were turned off during the period that the calibration data were collected. We will build the model and calibrate it with the two wells off and then enter a non-zero pumping rate prior to the prediction (particle tracking) phase.

| Name |      	X      |     	Y     |   	Z    |    	Type     |  	Flow Rate  |
|:----:|:------------:|:----------:|:-------:|:------------:|:------------:|
|  G   |  	755879.0   | 	3005310.0 |  	46.5  |    	well     |      	0      |
|  H   |  	755702.0   | 	3005897.0 |  	46.5  |    	well     |      	0      |
| IW1  |  	755442.0   | 	3004227.0 |  	16.0  |    	well     |  	-13406.0   |
| IW2  |  	755845.0   | 	3003893.0 |  	5.0   |    	well     |  	-38304.0   |

_Table 1. Data for Wells G&H and the Two Industrial Wells._

## Recharge

Next, we will create a recharge coverage.

>>1) Duplicate the **boundary** coverage to create a new coverage called **recharge.** Turn on the **Recharge rate** attribute.

>>2) Build polygons.

>>3) Double-click the polygon and enter a recharge rate of **0.004** ft/day.

Once again, this is an estimate that you may wish to adjust during the calibration phase.

## Active Region

Finally, we need a polygon coverage to define the active region of our model.

>>1) Duplicate the boundary coverage to create a new coverage called **active zone**.

>>2) Open the **Coverage Setup** dialog and make sure the **Use to define model boundary (active area)** option is turned on.

>>3) Build polygons.

## Building the Grid

We will now build the computational grid and initialize MODFLOW.

1) Create a grid frame and fit it to your grid. You may wish to rotate the grid to align it with the upper boundary.

2) Double-click on the grid frame and change the **Origin z** value to **-60** and set the **Dimension z** value to **180.**

3) Create a 3D grid.

4) Initialize the MODFLOW simulation.

5) Use the **Activate Cells in Coverage** command to inactivate the cells outside the model boundary.

6) Select the **Map -> MODFLOW** command.

## MODFLOW Properties

Next we will assign starting head and hydraulic conductivity values to the grid cells. We will use a constant value for K for now, but during the calibration phase we will use the pilot point method to interpolate K values.

1) Enter **starting head = 150** for all cells.

2) Enter **K = 15** for all cells.

## Layer Elevations

The final step before running the model is to interpolate a set of top and bottom elevations. To do this, we will download a file containing a scatter point set with both ground surface and bedrock elevations. 

>>1) Download the [<u>elevations.txt</u>](case_study_1/elevations.txt) file (use the **Save Link As...** option in your browser).

>>2) Use the **File|Open** command to open the file and follow the steps in the **Import Wizard.**

Before interpolating we need to change the interpolation option. For some reason the top and bottom elevations from elevations.txt cannot be interpolated using the IDW-Gradient Plane method (the default).

>>3) Open the **Interpolation Options** dialog and change the IDW **Nodal function** sub-option to **Constant (Shepard's Method).**

>>4) Use the **Interpolate to MODFLOW Layers** command to interpolation the elevations to the top and bottom elevations arrays for layer 1.

>>5) Contour your top and bottom elevations arrays to check your results.

## Save and Run MODFLOW

We are now ready to save and run MODFLOW.

>>1) Run the **Check Simulation** command to see if you have any obvious errors.

>>2) Save your project and run MODFLOW.

Note that you may end up with some flooded cells and some dry cells. You can adjust the model inputs and do some manual calibration to get better results if you wish.
