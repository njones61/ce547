# Exam 2 Study Guide

## Outline of Main Concepts

### 1. 2D Geostatistics - Interpolating Layer Elevations

* **Core Concept:** Using 2D geostatistics to interpolate MODFLOW layer elevations from point data (e.g., boreholes, DEMs).
* **MODFLOW Layer Structure:**
    * Each grid cell has a top and bottom elevation, defined in the discretization file.
    * GMS assumes the bottom of layer i is the top of layer i+1 (bot<sub>i</sub> = top<sub>i+1</sub>).
    * A model with 'n' layers requires 'n+1' elevation arrays.
* **Data Sources & Preparation:**
    * **Ground Surface (Top of Layer 1):** Typically derived from Digital Elevation Model (DEM) data, which can be imported directly from web services in GMS.
    * **Subsurface Layers:** Created from scatter point sets using data from boreholes, cross-sections, etc.
    * **Scatter Point Sets:**
        * Equivalent to a point feature class in ArcGIS.
        * Contains points with XY locations and associated data sets (attributes).
        * Can be imported from .txt or .csv files or pasted from the clipboard.
        * The Text Import Wizard guides the import process.
* **Interpolation Process:**
    * The Interpolate → MODFLOW Layers command interpolates scatter point data directly to the appropriate MODFLOW layer arrays.
    * Interpolation can also be done from scatter points to TINs, meshes, or grids.
* **Interpolation Methods:**
    * **Linear:** Connects points into triangles and interpolates linearly across them. Fast and simple, but not smooth. Good for dense data like DEMs. Does not extrapolate.
    * **Inverse Distance Weighted (IDW):** A common default method giving good results.
        * **Constant:** Simplest form, can create bumps and pits.
        * **Gradient Planes:** Fits a planar surface at each point for a smoother result.
        * **Quadratic:** Uses quadratic nodal functions for even smoother results.
    * **Natural Neighbor:** A popular and effective interpolation method.
    * **Kriging:** The most complicated to set up (requires a variogram) but generally the most accurate, especially with sparse data.
    * **Truncation:** An option to limit interpolated values to a specified min/max range, useful for preventing unrealistic values (e.g., elevations below zero).
* **Error Correction:**
    * Interpolation can cause errors like overlapping layers (e.g., top of layer 3 is above the bottom of layer 1).
    * The Model Checker tool detects these errors.
    * Fixing tools can model complex stratigraphy like Bedrock Truncation and Layer Outcropping.

### 2. MODFLOW Solvers

* **Core Concept:** Solvers are algorithms used to find a solution (a set of head values) that satisfies the governing groundwater flow equation. Most are iterative.
* **Iterative Solution Process:**
    * The user provides an initial guess of head values (starting heads).
    * The solver iteratively "tweaks" or adjusts head values in each cell.
    * The process continues until the maximum head change between iterations is less than the convergence tolerance.
* **Solver Types:**
    * **SIP (Strongly Implicit Procedure):** An original solver; simple but can have speed/stability issues.
    * **SOR (Slice-Successive Over-Relaxation):** An original solver; not recommended as it can be unstable.
    * **PCG2 (Pre-Conditioned Conjugate Gradient):** A good all-around solver; the default in GMS.
    * **PCGN:** A newer, more stable version of PCG2.
    * **NWT (Newton Solver):** Used with MODFLOW-NWT; best for solving wetting and drying problems.
    * **GMG (Geometric Multi-Grid):** A fast USGS multi-grid solver that requires more memory.
    * **DE4 (Direct Solver):** A non-iterative direct matrix solution solver.
    * **LMG (Link-Algebraic Multi-Grid):** A high-performance commercial multi-grid solver.
    * **SMS (Sparse Matrix Solver):** Used with MODFLOW-USG (unstructured grids).
* **Key Solver Parameters:**
    * **Max Number of Iterations:** The solver stops if it reaches this number without converging.
    * **Convergence Tolerance:** The threshold for the maximum head change; if the change is less than this value, the model has converged.
    * **Acceleration/Damping Parameter:** Controls the size of head adjustments per iteration.
        * =1.0: Standard adjustment (Default).
        * <1.0: Reduced adjustment; improves convergence for unstable models but slows the solution.
        * \>1.0: Increased adjustment; faster but may be unstable.
* **Troubleshooting Non-Convergence:**
    * **Diagnosis:** Review command line output, run Model Checker, and examine the MODFLOW output file (.OUT).
    * **Common Causes:**
        * Improper aquifer properties (K is zero, too high, or too low).
        * Unbalanced flow budget (insufficient head-dependent boundaries to act as sources/sinks).
        * Poor starting head estimates.
        * Cells going dry.
* **Wetting and Drying:**
    * A cell goes "dry" if its computed head drops below the cell bottom elevation; it is then turned off.
    * **Causes:** Head overshoot during iteration, incorrect model parameters (high K, low recharge, high pumping), or transient conditions.
    * **Solutions:**
        * Reduce the acceleration/damping parameter to prevent overshoot.
        * Improve starting head estimates to be closer to the final solution.
        * Adjust model parameters.
        * Use the rewetting option (available in flow packages like LPF), which allows dry cells to become wet again but can decrease stability.
        * Use MODFLOW-NWT, which is specifically designed to handle wetting and drying problems robustly.

### 3. Regional Models - The Conceptual Model Approach

* **Modeling Approaches:**
    * **Grid Approach:** Build a grid first, then assign properties directly to cells. Works for simple models.
    * **Conceptual Model Approach:** Build a grid-independent representation of model features using points, lines, and polygons. Properties are assigned to these features, and the grid-based numerical model is automatically derived from it. Best for complex regional models.
* **Steps in the Conceptual Model Approach:**
    1. **Establish a Base Map:** Provides geographic reference. Can be loaded from web services (ESRI) and can be exported as a local, tiled copy for faster refreshing.
    2. **Define a Projection:** Sets the coordinate system for the project. Imported data with a defined projection is automatically located correctly.
    3. **Select Units:** Ensures consistency. Length unit must match the projection.
    4. **Build a Conceptual Model:** Create a grid-independent representation of model features.
    5. **Convert to Numerical Model:** Generate the grid and automatically assign properties from the conceptual model.
* **Building the Conceptual Model:**
    * **Feature Objects:**
        * **Points:** Used for features like wells.
        * **Arcs (Polylines):** Composed of nodes (endpoints) and vertices (midpoints). Properties can be assigned to nodes and vary linearly along the arc. Used for rivers, drains, etc.
        * **Polygons:** Formed by closed loops of arcs. Used for defining zones of K, recharge, or general head boundaries.
    * **Coverages:** Collections of related feature objects used to organize data. A conceptual model consists of one or more coverages.
* **Conductance Calculation:**
    * A critical parameter for source/sink packages (River, Drain, GHB).
    * **For Arcs (e.g., River):** Assign conductance on a per length basis. C = K × W / M, where K is riverbed conductivity, W is width, and M is riverbed thickness. GMS calculates the length of overlap in each cell and multiplies it by this value.
    * **For Polygons (e.g., Lake/GHB):** Assign conductance on a per area basis. C = K / M, where K is sediment conductivity and M is sediment thickness. GMS calculates the area of overlap in each cell and multiplies it by this value.
* **Converting to a Numerical Model:**
    1. **Create Grid Frame:** Defines the location, size, and rotation of the grid relative to the conceptual model.
    2. **Map → 3D Grid:** Creates a 3D grid that fills the grid frame.
    3. **New MODFLOW Simulation:** Initializes the numerical model.
    4. **Activate Cells in Coverage(s):** Inactivates all grid cells outside the conceptual model boundary polygon.
    5. **Map → MODFLOW:** The final step that discretizes all conceptual model inputs (properties, sources/sinks, conductances) and populates the MODFLOW packages with cell-by-cell values.

### 4. Model Calibration Basics

* **Core Concept:** The process of adjusting model input parameters (K, recharge, etc.) until the model's simulated outputs (heads and flows) match field-observed values.
* **Observation Data:**
    * **Head Observations:** Water table elevations measured in monitoring wells or piezometers. Care must be taken with data from production wells due to cones of depression.
    * **Flow Observations:** Measurements of streamflow, typically used to determine gains or losses to baseflow between two points on a stream.
* **Calibration Methods:**
    * **Trial and Error (Manual):** Manually tweaking inputs and re-running the model.
    * **Automated Parameter Estimation:** Using an optimization utility (like PEST) to systematically adjust input parameters to minimize error.
* **Measuring Calibration Success:**
    * A perfect fit is not expected due to measurement error, simplifying assumptions, and uncertainty in inputs.
    * The goal is to get simulated values within a "window" or calibration target of the observed values.
    * **Residual:** The difference between an observed value and a computed value (Observed - Computed).
* **Error Norms (Global Measures):**
    * **Mean Error (ME):** The average of the residuals. Indicates overall bias (if heads are consistently too high or too low).
    * **Mean Absolute Error (MAE):** The average of the absolute values of the residuals. Indicates the average magnitude of error.
    * **Root Mean Squared Error (RMSE):** The square root of the average of the squared residuals. Magnifies the effect of large outlier errors.
    * **Sum of Squared Weighted Residuals (SSWR):** A single error norm used by optimization software (PEST) that combines both head and flow residuals, applying weights to each observation.
* **The Problem of Non-Uniqueness:**
    * It is possible to achieve a good calibration with multiple, different combinations of input parameters.
    * **Example:** Calibrating to heads only can be achieved with either (Low K and Low Recharge) or (High K and High Recharge), as both can produce a similar water table shape.
    * This is a problem because while the heads may match, the flow velocities and fluxes could be completely wrong, making the model a poor predictive tool.
* **Achieving a Unique Solution:**
    * Including flow observations is crucial. A flow observation (like baseflow discharge to a stream) pins down the water budget, effectively fixing one of the unknowns (e.g., recharge).
    * By constraining the total flux through the system, the remaining parameters (like K) can be solved for with much greater confidence, drastically reducing the number of possible solutions and leading to a more unique model.

### 5. Calibration Tools in GMS

* **Observation Points:**
    * Primarily used for head observations from monitoring wells.
    * Organized in a special Observation Coverage in the Map Module.
    * Data can be imported from text files or pasted from a spreadsheet.
    * The attribute table includes name, XY coordinates, observed head, layer number, and the interval and confidence used to define the calibration target and observation weight.
* **Calibration Targets:**
    * A visual representation of the residual at each observation point.
    * The size of the target "whisker" is based on the user-defined interval.
    * **Color-coded for quick assessment:**
        * **Green:** Computed value is within the target interval.
        * **Yellow:** Computed value is outside the target (error > 100% of interval).
        * **Red:** Computed value is far outside the target (error > 200% of interval).
* **Calibration Statistic Plots:**
    * Accessed via the Create Plot macro.
    * The Computed vs. Observed plot is an industry-standard 45-degree line plot.
    * A well-calibrated model will have points tightly clustered around the 45-degree line.
* **Flow Observations:**
    * Assigned to arcs (for streams) or polygons (for lakes) in a source/sink coverage.
    * **Arc Groups:** If a flow observation spans multiple stream arcs, the arcs must be combined into an Arc Group to assign the single observation to the collection.
* **Viewing Results:**
    * Clicking on an observation point or arc in the main window displays its specific computed vs. observed values and residual at the bottom of the screen.
    * Global error norms (ME, MAE, RMSE, SSWR) for the entire solution can be viewed by right-clicking the solution folder in the Project Explorer and selecting Properties.

### 6. Automated Parameter Estimation with PEST

* **PEST (Parameter ESTimation):** An optimization utility developed by John Doherty that minimizes residual error (specifically, the SSWR) by iteratively adjusting selected input parameters. It is fully integrated into GMS.
* **Parameterization:** The process of identifying the model input values to be optimized by PEST.
    * The number of parameters must generally be less than the number of observations (unless using pilot points with regularization).
    * **Methods:**
        * **Zonation:** Dividing an array (like K or Recharge) into zones of constant value. Each zone is a single parameter. This is the most common method.
        * **Multiplier Arrays:** Using a single parameter to scale an entire array up or down.
        * **Pilot Points:** A method for simulating heterogeneity, covered in the next section.
    * **Key Values:** Using unique negative numbers (e.g., -700, -800) in the input arrays to mark the location and extent of parameter zones. PEST uses these to build the parameter list.
* **PEST Workflow in GMS:**
    1. Build a stable, working MODFLOW model with good starting values.
    2. Enter all head and flow observation data.
    3. Parameterize the model using zonation or another method with key values.
    4. Initialize the parameter list from the model (GMS finds the key values). Edit the list to set min/max bounds and starting values.
    5. Run the model in Inverse Run mode (parameter estimation).
    6. Monitor the PEST console as it runs, showing the error reduction per iteration.
    7. View the output results (updated calibration targets, plots, and global error norms).
    8. Import the final optimal parameter values back into the parameter list.
* **Important Considerations:**
    * **Stability:** The MODFLOW solver must converge for every PEST run. It may be necessary to increase max iterations or decrease the acceleration parameter to ensure stability.
    * **Uniqueness:** After a PEST run, check the *.MTT file. If the ratio of the maximum to minimum eigenvalue is greater than ~10⁸, the model is likely non-unique.
    * **Parameter Sensitivity:** The *.SEN file (or a sensitivity plot in GMS) shows which parameters have the largest impact on the model error. Hydraulic conductivity and recharge are typically the most sensitive.

### 7. The Pilot Point Method

* **Core Concept:** A parameterization method that simulates spatial heterogeneity without requiring discrete zones. It is particularly effective for hydraulic conductivity (K).
* **How It Works:**
    1. The user creates a set of 2D scatter points, called pilot points.
    2. Each pilot point is assigned a starting K value (a parameter).
    3. The K values are spatially interpolated from the pilot points to the MODFLOW grid cells, creating a smooth, heterogeneous K field.
    4. PEST treats each pilot point's K value as a handle, "warping" the interpolated surface by adjusting the point values to minimize the difference between simulated and observed heads.
* **Advantages & Disadvantages:**
    * **Advantages:** Can produce calibrated models with very low error; does not require arbitrary zonation decisions.
    * **Disadvantages:** Can have long run times, as each pilot point adds a parameter. This can be mitigated with SVD-Assist or Parallel PEST.
* **Regularization:**
    * A technique used by PEST that adds "stiffness" to the objective function, allowing the use of more parameters than observations, which is common with pilot points.
    * **Preferred Homogeneous Regularization (Default):** In the absence of influence from observations, pilot points near each other are encouraged to have similar values.
    * **Preferred Value Regularization:** In the absence of influence, pilot points are encouraged to stay close to their starting value.
* **Pilot Point Placement Strategies:**
    * **Uniform Placement:** Points are distributed on a regular grid. Simple and can work well.
    * **Adaptive Placement:** Points are manually and strategically placed based on model features:
        * Between observation wells.
        * Between observation wells and boundaries.
        * In areas of high hydraulic gradient.
        * With higher density where observation wells are denser.
    * **Fixed Pilot Points:** If K has been measured from a pump test, a pilot point can be placed at that location and marked as "fixed." Its value will not be changed by PEST.


---

## Review Questions

### True/False Questions

1. A MODFLOW model with 3 layers requires 3 elevation arrays to be defined.

    **False.** A 3-layer model requires 4 elevation arrays (Top<sub>1</sub>, Bot<sub>1</sub>/Top<sub>2</sub>, Bot<sub>2</sub>/Top<sub>3</sub>, Bot<sub>3</sub>).

2. The Slice-Successive Over-Relaxation (SOR) solver is not recommended because it can result in incorrect solutions.

    **True.** The source states it can result in incorrect solutions and is not recommended.

3. In the conceptual model approach, conductance for a river arc should be assigned on a conductance per area basis.

    **False.** Conductance for an arc is assigned on a per length basis.

4. The Root Mean Squared Error (RMSE) is more sensitive to large outlier errors than the Mean Absolute Error (MAE).

    **True.** RMSE squares the residuals, which gives greater weight to larger values (outliers).

5. Calibration targets shown in green in GMS indicate that the computed value is far outside the user-defined interval.

    **False.** Green indicates the value is within the target interval. Red indicates it is far outside.

6. PEST is an acronym for Parameter ESTimation.

    **True.** The P is from Parameter and the EST is from ESTimation.

7. Using the pilot point method requires that the number of pilot points (parameters) be less than the number of observations.

    **False.** Due to regularization, the pilot point method allows for more parameters than observations.

8. The top elevation of layer 1 typically corresponds to the ground surface.

    **True.** DEM data is typically used to define the ground surface, which is the top of layer 1.

9. Setting the solver's acceleration/damping parameter to a value greater than 1.0 is a common strategy to improve model stability.

    **False.** Values > 1.0 may make the model unstable. A value < 1.0 is used to improve stability.

10. The Map → MODFLOW command is used to create the 3D grid from a grid frame.

    **False.** The Map → 3D Grid command creates the grid. Map → MODFLOW populates it with data.

11. A model calibrated only to head observations might be non-unique.

    **True.** This is the core concept of non-uniqueness; different parameter sets can produce the same heads.

12. An Arc Group is used to assign a single flow observation to a collection of multiple stream segments.

    **True.** This allows a single flow value to be compared against the summed computed flow from multiple arcs.

13. In PEST, a "forward run" computes optimal parameter values that minimize residuals.

    **False.** An "inverse run" computes optimal parameter values. A "forward run" is a normal model run using a specified set of parameter values.

14. Regularization is a technique that adds stiffness to the PEST objective function, allowing for more parameters than observations.

    **True.** This is the definition of regularization in this context.

15. A fixed pilot point is a point whose location is fixed, but its hydraulic conductivity value can be changed by PEST.

    **False.** A fixed pilot point's hydraulic conductivity value is fixed and is NOT changed by PEST.

### Multiple Choice Questions

1. Which interpolation method is generally considered the most accurate for sparse data but requires setting up a variogram?

    > A) Inverse Distance Weighted (IDW)<br>
    > B) Linear<br>
    > **C) Kriging**<br>
    > D) Natural Neighbor

2. What is the best solver to use for models with significant wetting and drying problems?

    > A) PCG2<br>
    > B) SIP<br>
    > **C) NWT** (MODFLOW-NWT is specifically designed for this).<br>
    > D) GMG

3. If a model is having trouble converging due to oscillation, a good first step is to:

    > A) Increase the convergence tolerance.<br>
    > **B) Decrease the acceleration/damping parameter to a value less than 1.0.**<br>
    > C) Switch to the DE4 direct solver.<br>
    > D) Increase the maximum number of iterations.

4. In the GMS conceptual model approach, what feature object is composed of nodes and vertices?

    > A) Point<br>
    > B) Polygon<br>
    > C) Coverage<br>
    > **D) Arc**

5. What is the primary purpose of including flow observations in model calibration?

    > A) To decrease the model run time.<br>
    > **B) To achieve a more unique and defensible solution.**<br>
    > C) To calculate the Mean Absolute Error.<br>
    > D) To ensure the solver converges.

6. The industry-standard plot for visualizing calibration results, which shows points clustered around a 45-degree line, is called:

    > A) A calibration target plot.<br>
    > B) A parameter sensitivity plot.<br>
    > **C) A computed vs. observed plot.**<br>
    > D) An error norm summary plot.

7. Which of the following is NOT a primary method for parameterizing a model for PEST?

    > A) Zonation<br>
    > **B) Solver Selection** (This is part of the model setup, not parameterization for PEST).<br>
    > C) Multiplier Arrays<br>
    > D) Pilot Points

8. What does a ratio of the max/min eigenvalue greater than ~10⁸ in the *.MTT file indicate?

    > A) The model is highly sensitive to recharge.<br>
    > **B) The model calibration is likely non-unique.**<br>
    > C) The model has converged successfully.<br>
    > D) The model is using too many pilot points.

9. When creating pilot points, the "adaptive placement" strategy involves:

    > A) Placing points on a uniform grid.<br>
    > B) Allowing PEST to create points automatically.<br>
    > **C) Manually placing points strategically based on observation wells and boundaries.**<br>
    > D) Using only points where K has been measured from a pump test.

10. Which two parameters are typically the most sensitive during model calibration?

    > A) Riverbed Conductance and Specific Storage<br>
    > **B) Hydraulic Conductivity and Recharge**<br>
    > C) Pumping Rate and Drain Conductance<br>
    > D) Specific Yield and Evapotranspiration

11. To create a local, tiled copy of a web-based base map for faster refreshing, you should:

    > A) Use the File → Import from Web command.<br>
    > **B) Right-click on the map in the Project Explorer and select Export.**<br>
    > C) Go to Edit → Units and link the map.<br>
    > D) Create a new conceptual model.

12. A cell becomes "dry" in MODFLOW when:

    > A) The recharge rate is zero.<br>
    > **B) The head in the cell drops below the cell bottom elevation.**<br>
    > C) The head in the cell rises above the cell top elevation.<br>
    > D) The hydraulic conductivity is too low.

13. What is a "residual" in the context of model calibration?

    > A) The total number of model iterations.<br>
    > **B) The difference between an observed value and a computed value.**<br>
    > C) The hydraulic conductivity value assigned to a zone.<br>
    > D) A parameter with very low sensitivity.

14. What are key values (e.g., -900, -800) used for when setting up a PEST run?

    > A) They are the starting values for the parameters.<br>
    > B) They are error codes indicating non-convergence.<br>
    > **C) They are placeholders that mark the locations of parameter zones in input arrays.**<br>
    > D) They define the min/max bounds for parameters.

15. What is the default regularization method used by PEST with pilot points?

    > A) Preferred Value Regularization<br>
    > B) Single Value Decomposition<br>
    > C) Inverse Model Regularization<br>
    > **D) Preferred Homogeneous Regularization**

16. Which of the following is NOT an error norm used to measure overall model calibration?

    > A) Mean Error<br>
    > B) Sum of Squared Weighted Residuals<br>
    > **C) Parameter Sensitivity** (This is a result of a PEST analysis, not a direct measure of calibration error).<br>
    > D) Root Mean Squared Error

17. In the GMS conceptual model approach, a collection of related feature objects (points, arcs, polygons) is called a:

    > **A) Coverage**<br>
    > B) Grid Frame<br>
    > C) Data Set<br>
    > D) Layer

18. What is the function of a "Grid Frame"?

    > A) It defines the hydraulic properties of the grid cells.<br>
    > B) It organizes the observation points for calibration.<br>
    > **C) It defines the location, size, and rotation of the numerical grid.**<br>
    > D) It displays the final solution contours.

19. The Sum of Squared Weighted Residuals (SSWR) is the single objective function that PEST seeks to:

    > A) Maximize<br>
    > **B) Minimize**<br>
    > C) Keep constant<br>
    > D) Log transform

20. A scatter point set in GMS is analogous to what type of object in ArcGIS?

    > A) A raster dataset<br>
    > **B) A point feature class**<br>
    > C) A TIN<br>
    > D) A polygon feature class

### Short Answer Questions

1. What is the difference between a node and a vertex on a GMS arc?

    **Answer:** A node is an endpoint of an arc where properties (like river stage) can be assigned. A vertex is a midpoint along an arc that only defines its shape or geometry.

2. What is head overshoot and what is a simple way to fix it?

    **Answer:** Head overshoot is when an iterative solver adjusts a head value too far in one iteration, causing it to drop below the cell bottom and go dry unnecessarily. A simple fix is to reduce the acceleration/damping parameter to less than 1.0.

3. Why must conductance for a polygon be specified on a "per area" basis in the conceptual model?

    **Answer:** Conductance for a polygon must be specified per area because GMS automatically calculates the area of overlap between the polygon and each grid cell. GMS then multiplies the per-area conductance by the cell-specific overlap area to get the final cell conductance.

4. Briefly explain why a perfect fit between simulated and observed values should not be expected during calibration.

    **Answer:** A perfect fit is not expected due to inherent measurement error in field data, simplifying assumptions made in the model structure, and uncertainty in model inputs like pumping rates or boundary conditions.

5. What information does a red calibration target convey to the user in GMS?

    **Answer:** A red calibration target indicates a large error, specifically that the difference between the computed and observed value is more than 200% of the user-defined interval.

6. What is the purpose of copying computed heads to the starting heads array before running PEST?

    **Answer:** This ensures the starting heads are very close to the final solution, which reduces the number of solver iterations required for each model run and improves model stability, saving significant time during a PEST run that involves hundreds of model executions.

7. Define zonation as a parameterization method.

    **Answer:** Zonation is a parameterization method where a model input array (like hydraulic conductivity) is divided into a smaller number of discrete zones. All cells within a single zone are assigned the same value, and that single value becomes one parameter for PEST to optimize.

8. What is the primary advantage of the pilot point method over the zonation method?

    **Answer:** The primary advantage of the pilot point method is that it simulates spatial heterogeneity and does not require making arbitrary zonation decisions, which can be difficult and subjective in complex aquifers.

9. What are the two main types of observation data used for groundwater model calibration?

    **Answer:** The two main types of observation data are head observations (water levels from wells) and flow observations (gains/losses in streams or lakes).

10. What does the rewetting option do in MODFLOW, and what are its potential downsides?

    **Answer:** The rewetting option allows a cell that has gone dry to become wet again if conditions change. Its downsides are that it can increase solution time and may cause the solution to be less stable.

11. What is the final step in the conceptual model workflow that transfers all the defined properties to the numerical grid?

    **Answer:** The final step is the Map → MODFLOW command, which discretizes all conceptual model features and populates the MODFLOW packages.

12. What is the difference between a forward run and an inverse run when using a parameterized model?

    **Answer:** A forward run is a standard MODFLOW simulation that computes heads and flows based on a given set of parameter values. An inverse run uses PEST to start with observed heads/flows and solve for the optimal set of input parameters that minimizes the error.

### Essay Questions

1. Describe the complete workflow of the Conceptual Model Approach in GMS, starting from establishing a base map and ending with a ready-to-run numerical model. What are the key advantages of this approach over the Grid Approach?
2. Explain the problem of non-uniqueness in groundwater model calibration. Use the example of calibrating with only head observations to illustrate how different combinations of K and recharge can yield similar results. How does the inclusion of flow observations help to resolve this issue and lead to a more unique solution?
3. Compare and contrast the zonation method and the pilot point method for model parameterization. Discuss the core concept, advantages, disadvantages, and typical use case for each.
4. A MODFLOW simulation fails to converge. Describe the systematic process you would follow to troubleshoot the problem. What are the three main diagnostic tools you would use, and what are the common causes of non-convergence you would investigate?
5. Explain the concept of "wetting and drying" in MODFLOW. What causes cells to go dry, and what are the three primary solutions available to address this problem, including the most robust solution?
6. Describe the five different interpolation methods available in GMS for creating layer elevations (Linear, IDW, Natural Neighbor, Kriging, and Cleft-Koehler/Linear-like). Briefly explain how each works and discuss their relative accuracy, ease of use, and suitability for different types of data (sparse vs. dense).
7. What is PEST and what is its role in model calibration? Outline the major steps involved in setting up and running PEST within GMS, from parameterizing the model to importing the final optimal values.
8. Define the three primary error norms used to evaluate model calibration: Mean Error (ME), Mean Absolute Error (MAE), and Root Mean Squared Error (RMSE). Explain what each one measures and how they are used together to provide a comprehensive picture of calibration performance.
9. Explain the concept of regularization as it is used by PEST with the pilot point method. Why is it necessary, and what are the two main types of regularization discussed?
10. Describe the calibration tools available in GMS for visualizing and assessing model error. Include descriptions of observation points, calibration targets, the computed vs. observed plot, and how to view global error statistics.

---

## Essay Question Guidelines

!!!NOTE
    The following guidelines show very detailed answers. It may be possible to answer these questions with less detail depending on the context.

**1. (Conceptual Model Workflow):** The answer should detail the five main steps:

* **1. Establish Base Map:** Load a georeferenced map (e.g., from ESRI web services) to provide context. Exporting a local copy improves performance.
* **2. Define Projection & 3. Select Units:** Set up the coordinate system and consistent units for the model (e.g., feet, days). This is often done implicitly when setting up the base map.
* **4. Build Conceptual Model:** This is the core step.
    * Create a Conceptual Model object.
    * Create Coverages to organize data (e.g., one for boundaries/sources, one for K zones, one for recharge).
    * Use feature object tools to create points (wells), arcs (rivers), and polygons (model boundary, K zones).
    * Assign properties to these features, including conductances (per length for arcs, per area for polygons).
* **5. Convert to Numerical Model:**
    * Create a Grid Frame to define the grid extent.
    * Use Map → 3D Grid to generate the grid.
    * Use Activate Cells in Coverage to define the active model area.
    * Use Map → MODFLOW to automatically discretize and assign all properties from the conceptual model to the grid cells.
* **Advantages:** It is grid-independent, making it easy to change grid resolution. It automates the tedious task of assigning cell-by-cell values, which is highly efficient for complex regional models.

**2. (Non-Uniqueness):** The answer should explain:

* **Definition:** Non-uniqueness means that multiple, distinct sets of input parameters can produce a calibrated model where simulated values match observed values reasonably well.
* **Heads-Only Example:** A high water table can be simulated by either high recharge (more water in) or low hydraulic conductivity (water can't get out, so it mounds up). Conversely, a low water table can be simulated by low recharge or high K. Without knowing the total flow through the system, there's no way to distinguish between these scenarios. An infinite number of K/recharge combinations could theoretically produce the same head distribution.
* **Role of Flow Observations:** A flow observation, such as the baseflow discharge to a stream, measures the total flux exiting a portion of the system. This provides a hard constraint on the water budget. Since recharge is often the main input, the model's recharge value must be adjusted until the simulated discharge matches the observed flow. This "pins down" the recharge, removing one degree of freedom. With the flux fixed, PEST can then solve for K with much greater confidence, leading to a unique, or at least a much more constrained and defensible, solution.

**3. (Zonation vs. Pilot Points):** The answer should compare the two on these points:

* **Zonation:**
    * **Concept:** Divides the model into discrete polygons (zones), with each zone having one constant parameter value (e.g., a single K for the entire zone).
    * **Advantages:** Conceptually simple, intuitive, and computationally faster as it uses fewer parameters.
    * **Disadvantages:** Requires making arbitrary decisions about zone boundaries, which may not reflect the true, gradual changes in aquifer properties (heterogeneity). The result is a "stair-step" distribution of properties.
    * **Use Case:** Good for aquifers with clearly defined geological units or when a simpler parameterization is desired.
* **Pilot Points:**
    * **Concept:** Defines parameter values at discrete points. A smooth, heterogeneous field of properties is created by spatially interpolating between these points. Each pilot point is a parameter.
    * **Advantages:** Simulates heterogeneity without arbitrary zones, often resulting in a lower calibration error (better fit).
    * **Disadvantages:** Computationally intensive due to a large number of parameters, leading to long run times. Can potentially "over-fit" the data.
    * **Use Case:** Best for complex, heterogeneous aquifers where zone boundaries are unknown and a more realistic spatial distribution of properties is desired.

**4. (Troubleshooting Non-Convergence):** The answer should outline this process:

* **1. Diagnosis:**
    * **Command Line Output:** First place to look. It will explicitly state "MODFLOW failed to converge."
    * **Model Checker:** Run this GMS tool to find obvious input errors like K=0 or overlapping layers.
    * **MODFLOW Output File (*.OUT):** This text file provides detailed diagnostics, often identifying the specific cell with the largest head change, which can point to the problem area.
* **2. Common Causes & Investigation:**
    * **Improper Aquifer Properties:** Check for K values that are zero, too low (causing extreme head mounding), or too high (causing areas to go dry).
    * **Unbalanced Flow Budget:** Ensure the model has sufficient head-dependent boundaries (rivers, drains, GHBs) to act as flexible sources/sinks. A model with only fixed fluxes (recharge, wells) may not be able to reach equilibrium.
    * **Poor Starting Heads:** If starting heads are too far from the final solution, the model may not converge. Try using the solution from a previous stable run as the starting heads.
    * **Cells Going Dry:** This is a major cause of instability. Investigate using the methods from the next essay question.

**5. (Wetting and Drying):** The essay should cover:

* **Concept:** A cell goes "dry" when the solver calculates a head value below the cell's bottom elevation. MODFLOW then deactivates the cell. This can happen at any iteration, not just at the end of a time step.
* **Causes:**
    * **Head Overshoot:** The solver makes too large of an adjustment during an iteration.
    * **Model Parameters:** High K can create a flat water table that intersects the grid bottom; low recharge or high pumping can dewater the aquifer.
    * **Transient Conditions:** Fluctuating stresses can cause the water table to drop below cell bottoms.
* **Solutions:**
    * **1. Reduce Acceleration/Damping Parameter:** Setting the value to <1.0 forces smaller iterative steps, preventing overshoot. This is often the first and easiest thing to try.
    * **2. Improve Starting Head Estimates:** If the starting head is closer to the final solution, the solver doesn't have to make large adjustments, reducing the chance of overshoot.
    * **3. Use MODFLOW-NWT:** This is the most robust solution. MODFLOW-NWT and its associated Newton (NWT) solver are specifically designed to handle the non-linearities caused by cells rewetting and drying, leading to a much more stable solution in these cases. The standard "rewetting" option in packages like LPF is a last resort as it can be unstable.

**6. (Interpolation Methods):** The essay should describe:

* **Linear:** Creates a Triangulated Irregular Network (TIN) and interpolates linearly across flat triangular faces. Fast and predictable, but creates a faceted, non-smooth surface. Best for very dense data like a DEM.
* **Inverse Distance Weighted (IDW):** Estimates values based on a weighted average of surrounding points, where closer points have more influence. A good default method. Can have different "flavors" like Constant, Gradient Planes, or Quadratic for increasing smoothness.
* **Natural Neighbor:** A robust method that produces good results. The details of its algorithm are complex but it's a popular choice.
* **Kriging:** A geostatistical method that considers the spatial autocorrelation of the data. It is the most complex to set up (requires defining a variogram) but is generally considered the most accurate, especially when data is sparse.
* **Clough-Tocher/Linear-like:** Similar to Linear in that it uses triangulation, but applies some blending to create a slightly smoother result than pure linear interpolation.<br>

>For sparse borehole data, Kriging is superior, while for dense DEM data, Linear is often sufficient and very fast. IDW is a good all-around choice.

**7. (PEST Overview):** The essay should cover:

* **What is PEST:** PEST (Parameter ESTimation) is an external optimization software that automates model calibration. It functions as an "inverse model" by taking observed heads and flows as input and systematically adjusting user-defined model parameters (like K and recharge) to find the set of values that minimizes an objective function (the Sum of Squared Weighted Residuals).
* **Workflow:**
    1. **Build Stable Model:** Start with a working MODFLOW model.
    2. **Enter Observations:** Input all head and flow observation data with appropriate intervals/weights.
    3. **Parameterize Model:** Define which inputs PEST can change, using methods like zonation (with key values) or pilot points.
    4. **Initialize Parameter List:** Have GMS create the parameter list from the key values. Set starting values and min/max bounds for each parameter.
    5. **Run PEST:** Change the run mode to "Inverse" (Parameter Estimation) and execute the model. PEST takes over, running MODFLOW hundreds or thousands of times.
    6. **Analyze Results:** After PEST finishes, review the updated calibration statistics, plots, and targets in GMS. Check for uniqueness (*.MTT) and sensitivity (*.SEN).
    7. **Import Optimal Values:** Once satisfied, import the final optimized values from PEST back into the GMS parameter list to finalize the calibrated model.

**8. (Error Norms):** The essay should define and explain:

* **Mean Error (ME):** The average of all residuals (Observed - Computed). Its sign indicates the overall model bias. A large positive ME means computed heads are, on average, too low. A value near zero indicates positive and negative errors are balanced, but doesn't mean the errors are small.
* **Mean Absolute Error (MAE):** The average of the absolute values of the residuals. This measures the average magnitude of the error, regardless of direction. It provides a good sense of the typical error at any given point.
* **Root Mean Squared Error (RMSE):** The square root of the average of the squared residuals. Like MAE, it measures the magnitude of error. However, by squaring the residuals, it gives much more weight to large errors (outliers). If the RMSE is significantly larger than the MAE, it indicates the presence of a few points with very large errors that may need investigation.
* **Combined Use:** They should be used together. The goal is an ME near zero (no bias) and the lowest possible MAE and RMSE (small error magnitudes).

**9. (Regularization):** The essay should explain:

* **Why it's necessary:** Normally, an optimization problem is unstable if there are more unknown parameters than there are observations (constraints). The pilot point method often creates this exact situation. Regularization is a mathematical technique that adds extra information or constraints to the problem to make it stable and solvable. It adds "stiffness" to the objective function.
* **Preferred Homogeneous Regularization:** This is the default method. It adds a constraint that says, "in the absence of strong information from nearby observation wells, the values of adjacent pilot points should be similar." This encourages a smoother, more plausible interpolated surface and prevents unreasonable values in areas with no data.
* **Preferred Value Regularization:** This method adds a different constraint: "in the absence of strong information from nearby observation wells, the value of a pilot point should remain close to its initial starting value." This biases the solution towards the user's initial guess in data-poor areas.

**10. (GMS Calibration Tools):** The essay should describe:

* **Observation Points/Coverage:** A dedicated coverage type for entering monitoring well data, including location, observed head, and the interval/confidence used for weighting and target visualization.
* **Calibration Targets:** A graphical overlay on the model view. At each observation point, it displays a symbol (whisker plot) showing the residual (difference between computed and observed head). The symbol is color-coded (green/yellow/red) to give an immediate, spatial sense of calibration quality.
* **Computed vs. Observed Plot:** An industry-standard scatter plot that graphs the computed head against the observed head for all observation points. A perfect calibration would have all points on a 45-degree line. It provides a global summary of the calibration fit.
* **Global Error Statistics:** The overall error norms (ME, MAE, RMSE, SSWR) for both heads and flows can be accessed by right-clicking on the solution folder in the Project Explorer and viewing its properties. This provides the quantitative summary of the model's performance.

## Glossary of Key Terms

| Term | Definition |
|:-----|:-----------|
| **2D Geostatistics** | A set of tools in the 2D Scatter Point Module in GMS used to interpolate data, such as layer elevations, to grids or other objects. |
| **Acceleration Parameter** | A solver parameter that controls the amount of adjustment made to heads at each iteration. A value less than 1.0 reduces the head change, which can improve convergence stability. |
| **Arc Group** | A feature object created by grouping multiple arcs together so that a single, combined flow observation can be assigned to the entire group. |
| **Arcs** | Feature objects representing polylines. They consist of nodes at the endpoints, where properties can be assigned, and vertices that define the geometry. |
| **Automated Parameter Estimation** | A calibration method that uses an optimization utility, such as PEST, to systematically adjust input parameters to find a set of values that minimizes the error between model outputs and field observations. |
| **Calibration** | The process of adjusting model input parameters (e.g., hydraulic conductivity, recharge) until the model's simulated outputs (heads and flows) match field-observed values within an acceptable margin of error. |
| **Calibration Target** | A user-defined interval around an observed value. In GMS, visual indicators show whether the computed value falls within (green), just outside (yellow), or far outside (red) this target range. |
| **Conceptual Model** | A grid-independent representation of the major model features, including aquifer properties, boundary conditions, and sources/sinks, defined using GIS objects like points, arcs, and polygons. |
| **Conductance per unit area** | The value assigned to a polygon in a conceptual model (e.g., for a General Head Boundary), calculated as K/M (hydraulic conductivity / vertical thickness of sediments). |
| **Conductance per unit length** | The value assigned to an arc in a conceptual model (e.g., for a River), calculated as K×W/M (hydraulic conductivity × width / thickness of riverbed material). |
| **Convergence Tolerance** | A solver parameter representing a small head value. The iterative solution process is considered converged and stops when the maximum head change across all cells in an iteration is less than this value. |
| **Coverage** | A collection of related GIS feature objects (points, arcs, polygons) that serves as a layer of information within a conceptual model. |
| **DEM (Digital Elevation Model)** | A dataset representing ground surface elevations, which can be imported into GMS and interpolated to define the top elevation of layer 1 in a MODFLOW grid. |
| **Grid Frame** | An object in GMS that defines the location, dimensions, and rotation of the 3D numerical grid relative to the conceptual model. |
| **Head Overshoot** | A common cause of model non-convergence where the solver makes too large an adjustment to a cell's head, causing it to fall below the cell bottom elevation and incorrectly become "dry." |
| **Inverse Distance Weighted (IDW)** | An interpolation method where the influence of a data point is inversely related to its distance from the interpolation location. It is the default interpolation method in GMS. |
| **Inverse Run** | A model simulation mode where an optimization utility like PEST is used to solve for the input parameters (e.g., K, recharge) that best match observed outputs (heads, flows). |
| **Iterative Solution Algorithm** | The method used by most MODFLOW solvers, which starts with an initial guess of head values and repeatedly "tweaks" them until the head differences satisfy the governing groundwater flow equation. |
| **Key Values** | Unique numerical values (typically negative, like -700, -800) entered into model arrays to mark the locations of different parameter zones for use with PEST. |
| **Kriging** | A geostatistical interpolation method that is often the most accurate for sparse data but requires the user to set up a variogram. |
| **Map to MODFLOW** | The GMS command that automatically discretizes all input from the conceptual model (features, properties, boundary conditions) and assigns the appropriate values to the cells of the numerical grid. |
| **Mean Absolute Error (MAE)** | A calibration error norm calculated as the average of the absolute values of the residuals. It indicates the average magnitude of error. |
| **Mean Error (ME)** | A calibration error norm calculated as the average of the residuals (observed value - computed value). It indicates the overall bias of the model (whether heads are consistently too high or too low). |
| **MODFLOW-NWT** | A version of MODFLOW that uses the Newton (NWT) solver, specifically designed to be more robust and stable for models with significant wetting and drying problems. |
| **Non-uniqueness** | A critical issue in calibration where different combinations of input parameters can result in similarly well-calibrated models, making the solution uncertain. |
| **Observation Points** | Points contained within a special "Observation Coverage" in the Map module that represent locations (e.g., monitoring wells) with field-observed head values used for calibration. |
| **Parameterization** | The process of identifying the set of input values to be optimized by an inverse model and simplifying them into a manageable number of parameters, using methods like zonation or pilot points. |
| **PCG2 (Pre-Conditioned Conjugate Gradient)** | A robust, all-around iterative solver package that is the default solver selected in GMS for new MODFLOW simulations. |
| **PEST** | An acronym for Parameter ESTimation; an optimization utility integrated with GMS that automatically adjusts specified model parameters to minimize the difference between simulated and observed values. |
| **Pilot Point Method** | A parameterization technique where aquifer properties (like K) are spatially interpolated from a set of user-created scatter points. The value at each pilot point becomes a parameter for PEST to optimize. |
| **Regularization** | A numerical technique used by PEST, particularly with the pilot point method, to add "stiffness" to the objective function, which allows a stable solution even when the number of parameters exceeds the number of observations. |
| **Residual** | The difference between a field-observed value and a model-computed value at the same location (e.g., observed head - computed head). |
| **Root Mean Squared (RMS) Error** | A calibration error norm calculated as the square root of the average of the squared residuals. It is sensitive to large outlier errors. |
| **Scatter Point Sets** | A fundamental GMS object type, analogous to a point feature class, that contains a list of points with XY locations and one or more associated data sets. |
| **Sum of Squared Weighted Residuals (SSWR)** | The single error norm, or objective function, that PEST seeks to minimize. It combines both head and flow residuals into a single value. |
| **Zonation** | A parameterization method where a model array is divided into discrete zones, with all cells within a single zone being assigned the same parameter value. |