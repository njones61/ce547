# Exam 3 Study Guide

This exam (and study guide) covers everything from **Particle Tracking** to the end of the semester. While the final exam will be comprehensive, this guide will focus on the main concepts covered in the course after midterm exam #2. For the final exam, it is recommended that you review all three study guides.

## Outline of Main Concepts

### 1. Particle Tracking with MODPATH

* **Introduction to MODPATH**
    * A companion program to MODFLOW, developed by the USGS.
    * Functions as a post-processing tool for MODFLOW solutions.
    * Uses a MODFLOW solution (heads, flow rates) to track hypothetical "particles" forward or backward in time.
    * The trajectory of these particles forms "pathlines."
* **Primary Applications**
    * Particle Tracking: Determining the flow path of groundwater from a starting point (e.g., a landfill leak).
    * Travel Time Analysis: Answering how long it takes for groundwater to travel between two points. This requires defining effective porosity.
    * Capture Zone Delineation: Identifying the area of an aquifer from which water is captured by a well.
* **Setup and Execution Steps**
    1. Run a MODFLOW simulation to generate a solution.
    2. Define effective porosity if travel time is a critical output. GMS defaults to 0.3.
    3. Generate particles at desired starting locations.
    4. Pathlines and capture zones are then automatically computed and updated.
* **Particle Generation Methods**
    * Generate Particles at Wells: Creates a circular ring of particles (default is 20) around selected or all wells. Useful for capture zone analysis.
    * Generate Particles at Selected Cells: Generates particles within a user-selected group of cells. Options for distribution include:
        * On the water table surface (for surface contamination scenarios).
        * On cell faces (a ring on the perimeter).
        * Within the cell (uniformly distributed in 3D).
    * Importing a file: An available but rarely used option.
* **Particle Sets and Tracking Options**
    * Particles are organized into "particle sets."
    * Each set can be configured with a name and tracking options:
        * Direction: Forward or backward in time.
        * Termination: Track to the "beginning" or "end" of the simulation, or for a specific "duration" (e.g., 1000 days).
* **Travel Time and Porosity**
    * To calculate correct travel time, MODPATH requires effective porosity (n or nₑ).
    * The seepage velocity (vₛ) is calculated as vₛ = (K * i) / n, which is distance over time.
    * Porosity can be defined by zones in the map module, edited in a spreadsheet, or assigned to selected cells.
* **Zone Codes**
    * Each grid cell can be assigned an integer zone code (default is 1).
    * Zone codes of starting and ending particle locations can be stored.
    * This allows for color-coding pathlines based on their starting zone, ending zone, or the zone they are passing through, which is useful for visualizing which particles go to a river versus a well.
* **Capture Zone Delineation**
    * Method:
        1. Vertices are created at points along all pathlines.
        2. These vertices are triangulated (Delaunay triangulation).
        3. Long, thin triangles on the perimeter are deleted based on a "thin triangle ratio."
        4. The resulting outer boundary forms the capture zone polygon.
    * Time-Based Capture Zones: By setting a maximum travel duration for backward tracking, one can delineate capture zones for specific timeframes (e.g., 1000-day, 2000-day capture zones).
    * Thin Triangle Ratio: A parameter that controls how tightly the capture zone polygon "shrinks" around the pathlines. A lower ratio (e.g., 0.96) can better represent concave shapes in the capture zone.

### 2. Stochastic Simulations: Basic Theory

* **Core Concept**
    * Instead of a single deterministic model, a set of N equally likely model "instances" or "realizations" is generated.
    * Each instance has slightly different input parameter values.
    * All N models are run, and a target outcome is evaluated across all solutions to determine its probability.
    * This approach is also known as a "Monte Carlo analysis."
* **Purpose and Advantages**
    * Provides a systematic way to deal with uncertainty in parameters, conceptual models, and observations.
    * Avoids the misleading impression of accuracy that a single deterministic solution can give.
    * Presents results in terms of probability (e.g., "80% probability of contamination") rather than a simple yes/no answer.
* **Stochastic Methods**
    * Parameter Randomization (most common): Randomizes the values of model parameters.
        * Random Sampling
        * Latin Hypercube Sampling
        * Gaussian Fields
    * Indicator Simulation (not covered in detail): Creates different interpretations of the spatial distribution of materials (aquifer heterogeneity).
* **Parameter Randomization Process**
    1. For each parameter to be randomized (e.g., hydraulic conductivity K), define a probability distribution function (PDF).
    2. Define the parameters of the distribution:
        * Distribution Type: Uniform/Linear, Normal, or Log-normal (Log-normal is common for hydraulic conductivity).
        * Mean: Typically the optimized value from a model calibration.
        * Standard Deviation: Represents the uncertainty or allowable variation.
        * Min/Max Values: Can be used to prevent extreme outliers and numerical instability.
    3. For each of the N model runs, a random value for each parameter is generated that honors its defined distribution.
* **Latin Hypercube Sampling**
    * A more structured variation of random sampling.
    * Objective: To explore the parameter space more thoroughly with fewer model runs, leading to greater certainty.
    * Process:
        1. The PDF for each parameter is divided into a number of segments (quantiles) with equal area under the curve.
        2. A structured approach is used to ensure that a random value is selected from every possible combination of segments across all parameters.
    * The total number of model runs is the multiplicative product of the number of segments for each parameter (e.g., 4 segments x 4 segments x 5 segments = 80 runs).
* **Gaussian Fields**
    * Randomizes entire arrays (like K or recharge) spatially, rather than randomizing parameter values within zones.
    * An "ensemble" of arrays is generated, each defining a model instance.
    * This method creates spatially distributed heterogeneity, with the size of the "blobs" controlled by a range parameter.

### 3. Stochastic Simulations: GMS Tools

* **Workflow in GMS**
    1. Select Run Option: In MODFLOW global options, choose "Stochastic" run type.
    2. Parameterize Inputs: Define parameters using zones in the conceptual model (same as for calibration).
    3. Select Parameter Values: In the parameters dialog, define the mean (starting value), min/max, and standard deviation for each parameter to be randomized. Toggle log transform for log-normal distributions.
    4. Select Randomization Options:
        * Choose the method (Random Sampling or Latin Hypercube).
        * For Random Sampling, enter the number of instances.
        * For Latin Hypercube, enter the number of segments for each parameter.
        * The table of runs is automatically populated.
    5. Save and Run MODFLOW: GMS executes one run for each model instance and tracks convergence.
    6. Read Solution: GMS reads in all converged solutions.
    7. Analyze Results: Analyze the ensemble of solutions.
* **Managing Solutions**
    * Solutions are organized in the Project Explorer under a main folder, with a sub-folder for each instance.
    * Clicking an individual solution folder displays its results.
    * Right-clicking a folder can show a summary of residuals.
* **Probabilistic Capture Zone Analysis**
    * An automated analysis tool in GMS available by right-clicking the top-level solution folder.
    * Result: A dataset where the value in each cell represents the probability that particles originating from that cell will be captured by a specific well.
    * Algorithm:
        1. For each model instance, one or more particles are generated at the center of each grid cell.
        2. Particles are tracked forward in time.
        3. The number of particles from each cell that are captured by a well is counted across all instances.
        4. Probability = (Number of particles captured) / (Total number of particles generated).
* **Application to Other Outcomes**
    * Stochastic analysis can be applied to any model outcome by stepping through each solution and tallying the results. Examples include:
        * Travel time from a spill to a receptor (river, lake, well).
        * Probability of springs going dry.
        * Probability of drawdown exceeding a threshold.
        * Determining if sustainable conditions are met.

### 4. Governing Equations: Transient Term

* **Derivation Foundation**
    * Starts with the mass balance equation: inflow - outflow = Δstorage / Δt.
    * For steady-state, Δstorage is zero. For transient, it is non-zero.
    * The change in mass stored (Δstorage) in a representative element (dx dy dz) is due to a change in the product of density (ρ) and porosity (n) over time.
    * The governing equation becomes: -[∂(ρvₓ)/∂x + ∂(ρvᵧ)/∂y + ∂(ρv₂)/∂z] = ∂(ρn)/∂t.
* **Simplification to Head**
    * Assuming constant density (ρ), it can be removed.
    * Inserting Darcy's Law for the velocity terms (v) expresses the left side in terms of head (h).
    * The right side, ∂n/∂t, represents the change in porosity over time. In a saturated aquifer, a change in storage can only happen if the void space changes.
    * This change in porosity is related to the change in head via the specific storage coefficient (Sₛ): ∂n/∂t = Sₛ * ∂h/∂t.
* **Final Transient Equation (Diffusion Equation)**
    * ∂/∂x(Kₓ ∂h/∂x) + ∂/∂y(Kᵧ ∂h/∂y) + ∂/∂z(K₂ ∂h/∂z) + R = Sₛ * ∂h/∂t
    * This equation relates head (h) to both position (x, y, z) and time (t).
* **Specific Storage (Sₛ)**
    * Definition: The volume of water released from a unit volume of the aquifer per unit decline in head.
    * Physical Mechanisms: A decrease in head leads to a decrease in pore pressure (u), which in turn:
        1. Increases effective stress (σ'): This compresses the aquifer matrix, squeezing water out. This is controlled by aquifer compressibility (α).
        2. Decreases pore pressure (u): This allows the water itself to expand slightly, releasing a small amount of water. This is controlled by fluid compressibility (β).
    * Derived Formula: Sₛ = γw(α + nβ)
        * γw = unit weight of water
        * α = aquifer compressibility (1/Modulus of Elasticity)
        * n = porosity
        * β = fluid compressibility (a constant for water, 4.4 x 10⁻¹⁰ m²/N)

### 5. Governing Equations: Areal Flow (Transient)

* **Confined Aquifers**
    * Assumes primarily horizontal flow in an aquifer of thickness b.
    * The 3D transient equation is multiplied by the aquifer thickness b.
    * This leads to new lumped parameters:
        * Transmissivity (T): T = K * b
        * Storativity (S): S = Sₛ * b
    * Storativity (S) Definition: The volume of water released from the aquifer per unit area due to a unit decline in head.
    * Governing Equation: ∂/∂x(Tₓ ∂h/∂x) + ∂/∂y(Tᵧ ∂h/∂y) = S * ∂h/∂t
* **Unconfined Aquifers**
    * The upper boundary is the free surface (water table).
    * The primary storage mechanism is different from confined aquifers.
    * Specific Yield (Sᵧ): The storage coefficient for unconfined aquifers.
    * Specific Yield (Sᵧ) Definition: The volume of water released from the unconfined aquifer per unit area per unit decline in head.
    * Physical Mechanism: When the water table drops, water in the pore space of the dewatered zone drains out due to gravity ("gravity drainage"). This releases a much larger volume of water than the compression/expansion mechanism of specific storage.
    * Sᵧ is approximately equal to the saturated moisture content minus the residual moisture content, and is generally a fraction of the total porosity (e.g., Sᵧ ≈ 0.15-0.2 for a porosity of 0.25-0.3).
    * Specific yield is also called "unconfined storativity" and is much larger than storativity (S) for a confined aquifer.
    * Governing Equation: ∂/∂x(Kₓh ∂h/∂x) + ∂/∂y(Kᵧh ∂h/∂y) = Sᵧ * ∂h/∂t

### 6. MODFLOW Transient Simulations

* **Storage Coefficients in MODFLOW**
    * The LPF package requires storage coefficients based on the layer type.
    * Confined Layer: Assumed to remain fully saturated. Requires only Specific Storage (Sₛ).
    * Convertible Layer: Can start saturated and become unsaturated (head drops below the cell top). Requires both Specific Storage (Sₛ) and Specific Yield (Sᵧ). MODFLOW uses Sₛ when the cell is saturated and switches to Sᵧ when it becomes unconfined.
* **Initial Conditions**
    * Critical Importance: For a transient model, initial conditions represent the state of the aquifer at time zero. They are not just a "guess" like in steady-state models.
    * Requirement: Starting heads must be consistent with the boundary conditions and stresses at the beginning of the simulation.
    * Incorrect Methods: Using arbitrary values (e.g., flat water table) or heads interpolated from observation wells is wrong. This causes the model to spend early time steps adjusting to the inconsistency, leading to errors.
    * Correct Method: Use model-generated heads from a preliminary steady-state run that uses the same boundary conditions as the start of the transient simulation.
    * MODFLOW Feature: Recent versions can automatically run the first time step as steady-state, which handles this requirement.
* **Time Discretization**
    * Stress Periods: Periods of time during which all model inputs (pumping rates, recharge, etc.) are constant. Inputs can only change at the beginning of a new stress period.
    * Time Steps: Computational intervals within a stress period. The model computes a solution for each time step.
    * Distribution:
        * Fewer stress periods with many time steps are used when inputs are constant for long periods but the aquifer response needs to be captured (e.g., cone of depression development).
        * Many stress periods with fewer time steps are used when inputs change frequently (e.g., modeling daily river stage changes).
* **Changing Head (CHD) Package**
    * The standard method for specified heads (IBOUND array) is for static (steady-state) conditions only.
    * The CHD package is required for specified head boundary conditions that change over time.
    * Unique Feature: For each stress period, the CHD package allows for specifying a beginning and ending head value. The head then varies linearly over the stress period, unlike most other packages which use a constant (step-function) value.

### 7. Boundary Condition Analysis: Types

* **Three Main Categories**
    1. Head Boundaries:
        * Constant Head (Specified Head): Represents a large water body with a strong connection to the aquifer (minimal head loss). Simulated with the IBOUND array (steady-state) or CHD package (transient).
        * Head-Dependent: Represents features like rivers, drains, or lakes where there is a low-K layer (e.g., riverbed) causing head loss between the feature and the aquifer. Simulated with packages like RIV, DRN, GHB.
    2. Specified Flow Boundaries:
        * Represents a known quantity of water entering the model boundary.
        * Commonly used for lateral inflow or mountain front recharge in alluvial aquifers adjacent to mountains.
        * Can be simulated with a series of injection wells or focused recharge along the model edge.
    3. No-Flow Boundaries:
        * Represents a boundary across which there is no groundwater flow. This is the default condition in MODFLOW.
        * Physical Barrier: An impermeable feature like a bedrock outcropping or a low-permeability fault.
        * Groundwater Divide: The high point in the water table where flow diverges. Can be used as a no-flow boundary, but care must be taken as its location can shift if stresses (e.g., new wells) are added nearby.
        * Parallel Flow Boundary: A line drawn parallel to groundwater flow direction (perpendicular to head contours). No flow crosses this line. Subject to the same cautions as a groundwater divide.

### 8. Boundary Condition Analysis: Improper Conditions & Solutions

* **The Problem of Over-Constrained Models**
    * It is critical to select boundary conditions that are appropriate for the site and do not lead to artificial calibration or a non-unique model.
    * A common error is to create a local-scale model by placing specified head boundaries on both the upstream and downstream ends, based on interpolated head contours.
    * Consequence: In this setup, the distribution of heads between the two boundaries is fixed. The model will produce the same head solution regardless of the hydraulic conductivity (K) value used. The only thing that changes is the calculated flow rate (Q). This is a non-unique model and is not useful for prediction.
* **Solutions to Avoid Non-Uniqueness**
    1. Use a Flow Observation: If a flow rate can be measured or estimated (e.g., stream gage gain/loss, tracer test, estimated lateral inflow), this provides an additional constraint. Calibrating to both heads and a flow target can lead to a unique value for K.
    2. Improve Boundary Conditions: Instead of a specified head upstream, extend the model boundary back to a true no-flow boundary (like a groundwater divide or bedrock). In this case, flow is driven by recharge, and heads will rise or fall based on the K value, making the model sensitive and calibration possible.
    3. Regional-to-Local Model Conversion (Telescopic Grid Refinement):
        * Strategy: When good local boundaries or flow observations are unavailable.
        1. Build a larger, regional model that extends to well-defined, natural boundaries (e.g., rivers, mountain fronts).
        2. Calibrate the regional model to find reasonable values for K, recharge, etc.
        3. Create a smaller, local model within the bounds of the regional model.
        4. Use the computed heads and/or flows from the calibrated regional model to define the boundary conditions for the local model.
        * Benefit: Even though the local model may use specified heads derived from the regional model's contours, it is more reliable because the underlying K and recharge values have been constrained by the calibration of the larger, more physically-based regional model.

### 9. Boundary Condition Analysis: Case Studies

* **Steptoe Valley, Nevada**
    * Context: Model for an environmental impact statement for a proposed power plant in a basin surrounded by mountains.
    * Boundary Conditions:
        * Lateral Boundaries (East/West): Lateral inflow (a type of specified flow) was used to represent subsurface flow from the adjacent mountain ranges into the valley fill. The amount of inflow was estimated using a separate hydrology model based on precipitation.
        * Northern/Southern Boundaries: Fixed head boundaries were used, placed far from the areas of interest to minimize their impact.
* **Sacramento, California**
    * Context: A large regional model for the City of Roseville and other stakeholders.
    * Boundary Conditions:
        * North, West, South: Major rivers (Bear, Feather, Sacramento, Mokelumne) were used as head-dependent boundaries.
        * East: The boundary was the edge of the Sierra Nevada mountains. This was represented as a combination of no-flow (bedrock) and specified flow (mountain front recharge). The recharge amount was calculated using the GSSHA surface water model for adjacent ungaged watersheds.
    * Application: The calibrated regional model was then used for regional-to-local model conversion to create smaller, focused models for specific analyses (e.g., aquifer storage and recovery systems).

### 10. Groundwater Sustainability: Definition & Consequences

* **Definition of Sustainability**
    * "Development and use of ground water in a manner that can be maintained for an indefinite time without causing unacceptable environmental, economic, or social consequences."
* **Perennial Yield (Safe Yield, Sustainable Yield)**
    * The maximum amount of water that can be withdrawn and consumed economically each year for an indefinite period.
    * Cannot exceed natural recharge indefinitely and is limited to the amount of natural discharge that can be salvaged for beneficial use.
* **Negative Consequences of Unsustainable Use**
    1. Aquifer Subsidence:
        * Mechanism: Over-pumping lowers the water table, which decreases pore pressure (u). This increases the effective stress (σ') on the aquifer matrix, causing it to compress like a sponge.
        * Result: The ground surface elevation drops.
        * Non-Elasticity: In aquifers with significant clay or silt, this compression is often permanent (non-elastic). The lost void space and storage capacity are not recovered even if the aquifer is refilled.
        * Impacts: Damage to infrastructure (roads, buildings, pipes), creation of earth fissures.
    2. Saltwater Intrusion:
        * Mechanism: In coastal areas, freshwater naturally floats on top of denser saltwater, forming a "freshwater lens." Over-pumping can lower the freshwater table, reversing the natural seaward gradient.
        * Result: Saltwater migrates inland and can be captured by pumping wells, contaminating the freshwater supply.
    3. Loss of Drought Mitigation Capacity:
        * Groundwater acts as a massive underground reservoir, providing a critical buffer during droughts when surface water is scarce.
        * If groundwater reserves are depleted during normal times, this crucial backup is unavailable during a drought, which can have catastrophic consequences.

### 11. Groundwater Sustainability: Equilibrium Dynamics

* **Natural Equilibrium**
    * Before development, aquifers are in a state of approximate dynamic equilibrium where inflows (recharge from precipitation, losing streams) equal outflows (discharge to streams, springs, evapotranspiration).
* **Theis's Principle (1940)**
    * Pumping is a new discharge superimposed on the system. It must be balanced by one or more of the following:
        1. An increase in recharge.
        2. A decrease in natural discharge.
        3. A loss of water from storage.
* **Capture**
    * The sum of increased recharge and decreased natural discharge is called capture. For pumping to be sustainable, it must eventually be balanced entirely by capture.
    * Water is "captured" by the wells before it can discharge to a stream or be lost to evapotranspiration.
* **Transitional Storage**
    * When pumping begins, water is initially removed from storage, causing the water table to drop (a cone of depression).
    * Definition: Transitional storage is the water lost from storage as the system evolves from its pre-pumping equilibrium state to a new equilibrium state (where Pumping = Capture).
* **Groundwater Mining**
    * If a new equilibrium is never achieved (or would take centuries/millennia), and the water table continues to decline indefinitely, the aquifer is in a state of groundwater mining. This is unsustainable use.
* **The Importance of Well Location**
    * The time it takes to reach a new equilibrium and the amount of transitional storage lost depend critically on the location of wells relative to natural discharge zones.
    * Wells placed far from discharge zones may take an extremely long time to "capture" the discharge, leading to prolonged periods of groundwater mining and potentially dewatering large portions of the aquifer.
    * Wells placed close to discharge zones can capture water more quickly and reach equilibrium sooner.
* **The Water Budget Myth**
    * The Myth: The common misconception that the sustainable yield of an aquifer is simply equal to its rate of natural recharge.
    * The Reality: This is incorrect because it ignores the dynamics of capture. Sustainable yield is limited to the amount of natural discharge that can be captured. Pumping an amount equal to recharge without considering where the water is coming from can lead to the depletion of streams, wetlands, and prolonged groundwater mining.

---

## Review Questions

### True/False Questions

1. MODPATH can calculate particle travel times without any information about aquifer porosity.

    **False.** MODPATH requires effective porosity to calculate correct travel times.

2. In MODPATH, "forward tracking" is used to delineate the capture zone for a pumping well.

    **False.** "Backward tracking" is used to delineate capture zones.

3. A Monte Carlo analysis is another name for a deterministic groundwater model.

    **False.** A Monte Carlo analysis is a stochastic modeling approach, the opposite of a single deterministic model.

4. Latin Hypercube sampling is a method designed to explore the parameter space more thoroughly with fewer model runs compared to simple random sampling.

    **True.**

5. In a transient groundwater model, the initial head values are just a starting guess and have little impact on the final solution.

    **False.** Initial conditions for a transient model are critical and must be consistent with the state of the aquifer at time zero.

6. The primary physical mechanism behind specific yield (Sᵧ) is the compression of the aquifer matrix.

    **False.** The primary mechanism for specific yield is gravity drainage from the dewatering of pore spaces. Aquifer compression is the mechanism for specific storage.

7. A "convertible" layer in MODFLOW requires both a specific storage and a specific yield value.

    **True.**

8. Storativity (S) is a dimensionless coefficient.

    **False.** Storativity (S) is dimensionless (L³/L²)/L = L/L.

9. A groundwater divide can be safely used as a no-flow boundary even if a new high-capacity well is installed right next to it.

    **False.** Major changes in stress, like a new well, can shift the flow paths and invalidate the assumption of a parallel flow or groundwater divide boundary.

10. A local-scale model with specified head boundaries on both the upstream and downstream sides will produce a unique, reliable calibration for hydraulic conductivity.

    **False.** This setup creates a non-unique, over-constrained model where the head solution is independent of the hydraulic conductivity.

11. Aquifer subsidence is a fully elastic process, meaning the ground surface will return to its original elevation if the aquifer is recharged.

    **False.** Subsidence is often non-elastic, especially in formations with clay and silt, leading to a permanent loss of storage capacity.

12. According to Theis, pumping must ultimately be balanced by an increase in recharge and/or a decrease in natural discharge.

    **True.**

13. The "water budget myth" refers to the correct idea that sustainable pumping is limited to the amount of natural discharge that can be captured.

    **False.** The "water budget myth" is the misconception itself, not the correct idea. The myth is that sustainable yield equals recharge.

14. In coastal aquifers, over-pumping can reverse the natural hydraulic gradient, causing saltwater intrusion.

    **True.**

15. For the MODFLOW CHD package, head values are assumed to vary linearly within a single stress period.

    **True.**

### Multiple Choice Questions

1. Which of the following is NOT a primary application of MODPATH?

    > A) Delineating well capture zones.<br>
    > **B) Calibrating hydraulic conductivity values.**<br>
    > C) Analyzing groundwater travel times.<br>
    > D) Tracking the path of a contaminant plume.
2. To calculate seepage velocity and travel time, MODPATH uses Darcy velocity (Ki) divided by what parameter?

    > A) Storativity<br>
    > B) Specific Yield<br>
    > C) Transmissivity<br>
    > **D) Effective Porosity**
3. A stochastic simulation is primarily used to:

    > A) Find the single best-fit value for a parameter.<br>
    > **B) Systematically analyze the effects of uncertainty.**<br>
    > C) Speed up a MODFLOW run time.<br>
    > D) Simplify the governing differential equations.
4. Which probability distribution is most commonly used for hydraulic conductivity in stochastic groundwater modeling?

    > A) Uniform<br>
    > B) Linear<br>
    > C) Normal<br>
    > **D) Log-normal**
5. The total number of runs in a Latin Hypercube simulation is determined by:

    > A) The user directly entering the desired number of runs.<br>
    > B) The number of observation wells in the model.<br>
    > **C) The multiplicative product of the number of segments for each randomized parameter.**<br>
    > D) The standard deviation of the parameters.

6. The automated probabilistic capture zone analysis in GMS calculates:

    > A) The time it takes for a particle to reach a well.<br>
    > **B) The probability that a particle starting in a given cell will be captured by a well.**<br>
    > C) The total volume of water captured by a well over time.<br>
    > D) The single, definitive boundary of the capture zone.

7. Specific Storage (Sₛ) is defined as the volume of water released per unit decline in head from a:

    > A) Unit area of a confined aquifer.<br>
    > B) Unit area of an unconfined aquifer.<br>
    > **C) Unit volume of an aquifer.**<br>
    > D) Unit length of a stream.

8. The term Sₛ * ∂h/∂t in the transient governing equation is equivalent to:

    > A) ∂K/∂t<br>
    > **B) ∂n/∂t**<br>
    > C) ∂T/∂x<br>
    > D) ∂Q/∂t

9. Which storage coefficient is typically the largest in value?

    > A) Aquifer Compressibility (α)<br>
    > B) Specific Storage (Sₛ)<br>
    > C) Storativity (S)<br>
    > **D) Specific Yield (Sᵧ)**

10. In MODFLOW, the inputs for pumping rates and recharge can only be changed:

    > A) At the beginning of each time step.<br>
    > **B) At the beginning of each stress period.**<br>
    > C) At any point during the simulation.<br>
    > D) Only once, at the start of the model run.
11. Why must the initial conditions for a transient model be a model-generated steady-state solution?

    > A) To make the model run faster.<br>
    > **B) To ensure the starting heads are consistent with the boundary conditions and parameters at time zero.**<br>
    > C) To satisfy the requirements of the CHD package.<br>
    > D) Because arbitrary heads cause the model to fail to converge.

12. A boundary representing a river where there is significant head loss through the riverbed sediment is best modeled as a:

    > A) Constant head boundary.<br>
    > **B) Head-dependent boundary.**<br>
    > C) No-flow boundary.<br>
    > D) Specified flow boundary.

13. "Mountain front recharge" is an example of which boundary condition type?

    > A) Parallel Flow<br>
    > B) Groundwater Divide<br>
    > **C) Specified Flow**<br>
    > D) Constant Head

14. Building a large, calibrated regional model to define the boundary conditions for a smaller, focused model is known as:

    > A) Stochastic simulation.<br>
    > B) Artificial calibration.<br>
    > C) A Monte Carlo analysis.<br>
    > **D) Regional-to-local model conversion.**

15. The primary cause of aquifer subsidence is:

    > A) The expansion of water as pore pressure decreases.<br>
    > B) The dissolution of the aquifer matrix by groundwater.<br>
    > **C) An increase in effective stress causing the aquifer matrix to compress.**<br>
    > D) The weight of new buildings constructed on the surface.

16. Water lost from storage as an aquifer system evolves from a pre-pumping equilibrium to a new, post-pumping equilibrium is called:

    > A) Specific Yield<br>
    > B) Perennial Yield<br>
    > **C) Transitional Storage**<br>
    > D) Capture

17. If an aquifer's water table continues to drop for decades or centuries without reaching a new equilibrium, it is said to be in a state of:

    > A) Sustainable development.<br>
    > **B) Groundwater mining.**<br>
    > C) Capture.<br>
    > D) Dynamic equilibrium.

18. The "water budget myth" is the erroneous belief that sustainable yield is equal to:

    > A) The total amount of water in storage.<br>
    > B) The total amount of natural discharge.<br>
    > **C) The rate of natural recharge.**<br>
    > D) The pumping rate of the largest well.

19. For pumping to be sustainable in the long term, it must be balanced by:

    > A) Transitional storage.<br>
    > B) Water removed from storage.<br>
    > **C) Capture (increased recharge + decreased discharge).**<br>
    > D) Perennial yield.

20. Which case study used the GSSHA surface water model to estimate lateral inflow from ungaged watersheds for its boundary conditions?

    > A) San Joaquin Valley<br>
    > B) Steptoe Valley, Nevada<br>
    > C) Cedar Valley, Utah<br>
    > **D) Sacramento, California**

### Short Answer Questions

1. What are the two main physical mechanisms that contribute to specific storage (Sₛ)?

    **Answer:** The two mechanisms are (1) the compression of the aquifer matrix due to an increase in effective stress, and (2) the expansion of the pore water itself due to a decrease in pore pressure.

2. What is the fundamental difference between how specific storage and specific yield release water from an aquifer?

    **Answer:** Specific storage releases water through the slight compression of the aquifer matrix and expansion of water under pressure. Specific yield releases a much larger volume of water through the actual gravity drainage of water from the pore spaces as the water table falls.

3. Why is a log-normal distribution often used for hydraulic conductivity in stochastic simulations?

    **Answer:** Hydraulic conductivity (K) values often span several orders of magnitude in a single geologic setting. A log-normal distribution is appropriate because the logarithms of the K values are normally distributed, which better represents this wide range.

4. Briefly describe the purpose of using zone codes with MODPATH.

    **Answer:** Zone codes allow for the color-coding of pathlines based on their starting location, ending location, or the zones they pass through. This is a powerful visualization tool to distinguish, for example, which particles flow to a river versus which flow to a well.

5. What is the key difference between a "stress period" and a "time step" in a MODFLOW transient simulation?

    **Answer:** A stress period is a time interval during which all model stresses (like pumping) are constant. A time step is a smaller computational interval within a stress period at which the model calculates a head solution.

6. What is an "over-constrained" model, and what kind of boundary condition setup typically causes it?

    **Answer:** An "over-constrained" model is one where the boundary conditions so rigidly define the solution that the model is no longer sensitive to parameters like hydraulic conductivity. It is typically caused by placing specified-head boundaries on both the upstream and downstream ends of a model domain.

7. Define "perennial yield" in the context of groundwater sustainability.

    **Answer:** Perennial yield is the maximum amount of water that can be withdrawn from an aquifer indefinitely without causing unacceptable environmental, economic, or social consequences. It is limited by the amount of natural discharge that can be captured.

8. What is the relationship between storativity (S), specific storage (Sₛ), and aquifer thickness (b)?

    **Answer:** Storativity is the specific storage integrated over the aquifer thickness: S = Sₛ * b.

9. Explain why a parallel flow boundary is considered a type of no-flow boundary.

    **Answer:** Groundwater flows perpendicular to head contours. A parallel flow boundary is a line drawn parallel to the direction of flow. By definition, no groundwater can flow across this line, making it a no-flow boundary.

10. What is "capture" in the context of groundwater pumping and equilibrium?

    **Answer:** "Capture" refers to the process where pumping intercepts groundwater that would have otherwise discharged naturally (e.g., to a stream or phreatophytes) or induces additional recharge into the aquifer (e.g., from a losing stream).

11. What two pieces of information are needed for each parameter when setting up parameter randomization (e.g., random sampling)?

    **Answer:** For each parameter, you need to define its probability distribution function, which requires a mean and a standard deviation.

12. Why is groundwater a critical resource for drought mitigation?

    **Answer:** Groundwater is stored in vast underground aquifers, which act as natural reservoirs. During a drought, when surface water sources like rivers and reservoirs are depleted, this stored groundwater can be pumped to alleviate critical water shortages, acting as a buffer.

### Essay Questions

1. Describe the process of delineating a time-based capture zone for a well using MODPATH. Explain the roles of backward tracking, particle duration, and the triangulation method used to create the final polygon.
2. Compare and contrast the standard random sampling method with Latin Hypercube sampling for a stochastic simulation. What is the primary objective of using the Latin Hypercube method, and how does it achieve this?
3. Explain in detail why using arbitrary or field-measured heads as initial conditions for a transient MODFLOW simulation is an incorrect practice. What is the correct procedure, and why does it lead to a more accurate solution?
4. Derive the concept of Specific Storage (Sₛ). Start by explaining the two physical phenomena that occur when head declines in a saturated aquifer and combine them to arrive at the final expression Sₛ = γw(α + nβ). Define each term in the equation.
5. You are tasked with building a local-scale groundwater model around an industrial plant, but there are no clear physical boundaries (like rivers or bedrock) nearby. Describe the problem with simply applying fixed-head boundaries based on regional water level contours. Then, detail the strategy of "regional-to-local model conversion" as a superior alternative.
6. Define groundwater sustainability. Then, describe three major negative consequences of unsustainable groundwater use, explaining the physical process behind each one.
7. Explain the concept of equilibrium in a groundwater system, both before and after the introduction of pumping wells. Define "transitional storage" and describe the process by which a pumped aquifer reaches a new state of equilibrium.
8. What is the "water budget myth"? Explain why simply limiting total pumping to the total natural recharge of a basin is not sufficient to ensure sustainability. What other critical factor, as illustrated by the Theis and Bredehoeft examples, must be considered?
9. Describe the three main categories of groundwater model boundary conditions (Head, Specified Flow, No-Flow). For each category, provide two distinct examples and explain the physical situation they represent.
10. Imagine you are running a stochastic simulation to determine the probability that a landfill leak will contaminate a municipal well within 10 years. Outline the entire process, from setting up the parameter distributions to performing the final probabilistic analysis.

---

## Essay Question Answers

**1. (Time-Based Capture Zones):** To delineate a time-based capture zone (e.g., a 5-year zone), one would use MODPATH by first creating a set of particles in a ring around the screen of the pumping well. The particle tracking option would be set to "backward" in time. The termination criterion would be set to a specific "duration," corresponding to the desired timeframe (5 years, converted to the model's time units, e.g., 1826 days). When the simulation is run, MODPATH tracks the particles backward from the well for a maximum of 1826 days. The resulting pathlines show all the locations from which water could reach the well within 5 years. To create the final polygon, GMS takes all the points (vertices) along these pathlines, performs a Delaunay triangulation on them, and then deletes long, thin triangles from the perimeter to create a smooth outer boundary representing the 5-year capture zone.

**2. (Random Sampling vs Latin Hypercube):** Both methods are forms of parameter randomization. Standard random sampling generates a value for each parameter for each model run by independently drawing from each parameter's probability distribution. Over many runs, the distribution of sampled values will match the defined PDF. Latin Hypercube sampling is a more structured approach with the objective of exploring the parameter space more thoroughly and efficiently, achieving greater certainty with fewer runs. It achieves this by first dividing each parameter's PDF into an equal number of "segments" of equal probability. It then systematically generates runs by sampling one value from every possible combination of segments across all parameters, ensuring that the full range of each parameter's distribution is sampled in combination with the full range of all other parameters.

**3. (Transient Initial Conditions):** Using arbitrary or field-measured heads as initial conditions is incorrect because a transient simulation's initial state must be in equilibrium with the model's boundary conditions and parameters (K, recharge, etc.) at time zero. If arbitrary heads are used, they are inconsistent with the model physics. Consequently, the model will spend the initial time steps trying to adjust the heads to a consistent state. This adjustment is an artifact of the incorrect starting point, not a response to the transient stresses being studied, and it introduces significant error into the early-time results. The correct procedure is to perform a steady-state simulation using the exact boundary conditions and stresses that exist at the beginning (time zero) of the transient simulation. The resulting head solution from this steady-state run is then used as the starting heads array for the transient model. This ensures consistency and that any subsequent changes in head are a true response to the transient stresses applied in the model.

**4. (Specific Storage Derivation):** The concept of Specific Storage (Sₛ) describes the water released from a unit volume of a saturated aquifer when the hydraulic head declines by one unit. This release is due to two physical phenomena caused by the decrease in pore pressure (u):

* **Aquifer Compression:** The decrease in pore pressure increases the effective stress (σ') on the solid aquifer skeleton. This causes the matrix to compress, reducing the void volume and squeezing water out. The volume of water released is proportional to the aquifer compressibility (α) and the unit weight of water (γw). For a unit decline in head, this component is α * γw.
* **Water Expansion:** The decrease in pore pressure allows the water itself, which is slightly compressible, to expand. This expansion forces a small volume of water out of the pores. The volume released is proportional to the fluid compressibility (β), the volume of water present (porosity n), and the unit weight of water (γw). For a unit decline in head, this component is n * β * γw.

Combining these two terms gives the total specific storage: Sₛ = α*γw + n*β*γw, which simplifies to Sₛ = γw(α + nβ).

**5. (Regional-to-Local Model Conversion):** Applying fixed-head boundaries based on regional water level contours for a local model is problematic because it creates an over-constrained, non-unique system. The head gradient is fixed by the boundaries, meaning the model will produce the same head distribution regardless of the hydraulic conductivity (K) used. This makes it impossible to calibrate K uniquely, rendering the model useless for predictive simulations. A superior alternative is "regional-to-local model conversion." The strategy involves:

* First, building a larger regional model whose boundaries extend to actual, well-defined physical features like major rivers (head-dependent boundaries) and mountain fronts/bedrock (no-flow or specified-flow boundaries).
* This regional model is then calibrated against observed heads and, ideally, flow data (like stream baseflow). This process yields calibrated, physically plausible values for parameters like K and recharge over the entire region.
* A new, smaller, local-scale grid is then created for the area of interest.
* The boundary conditions for this local model are derived directly from the results of the calibrated regional model. The head values along the local model's boundary are interpolated from the regional model's solution.

This approach is more reliable because even though the local model uses "contour" head boundaries, those contours and the internal parameters (K, recharge) are consistent and have been validated through the calibration of the larger, physically-based regional model.

**6. (Groundwater Sustainability):** Groundwater sustainability is the development and use of groundwater in a manner that can be maintained indefinitely without causing unacceptable environmental, economic, or social consequences. Three major negative consequences are:

* **Aquifer Subsidence:** Over-pumping lowers the water table and pore pressure, which increases the effective stress on the aquifer's solid matrix. This causes the matrix (especially clays and silts) to compress permanently, leading to a drop in the ground surface elevation. This can damage infrastructure and permanently reduces the aquifer's storage capacity.
* **Saltwater Intrusion:** In coastal areas, excessive pumping can lower the freshwater table to the point that the natural seaward hydraulic gradient is reversed. This allows denser saltwater from the ocean to migrate inland, contaminating wells and rendering the freshwater resource unusable.
* **Loss of Drought Mitigation Capacity:** Aquifers act as massive natural reservoirs. Unsustainable pumping depletes this stored water. During a severe drought when surface water is unavailable, this critical backup supply will have been diminished or exhausted, potentially leading to catastrophic water shortages.

**7. (Equilibrium and Transitional Storage):** Before pumping, a natural groundwater system is in a state of dynamic equilibrium where long-term inflows (recharge) are balanced by long-term outflows (natural discharge to streams, springs, etc.). When a new stress, pumping, is introduced, this equilibrium is disturbed. Initially, the pumped water comes from water removed from storage, causing the water table to decline in a cone of depression. This volume of water removed to lower the heads is called "transitional storage." This head decline has two effects: it can reduce the amount of natural discharge (e.g., less water flows into a stream) and potentially increase recharge (e.g., a gaining stream becomes a losing stream). The system evolves until the head decline is sufficient to create enough "capture" (the sum of reduced discharge and increased recharge) to fully balance the pumping rate. At this point, no more water is taken from storage, and a new state of equilibrium is reached.

**8. (Water Budget Myth):** The "water budget myth" is the common and dangerous misconception that the sustainable pumping rate (or perennial yield) of a basin is simply equal to its average rate of natural recharge. This is a myth because it ignores the dynamics of the water budget and where the pumped water actually comes from. In a system in equilibrium, recharge is balanced by natural discharge. When you pump, the water must come from a reduction in storage, a reduction in discharge, or an increase in recharge. For pumping to be sustainable, it must eventually be balanced by "capture" (reduced discharge + increased recharge). Therefore, the true sustainable yield is limited by the amount of natural discharge that can be captured. Simply pumping an amount equal to recharge without capturing discharge will lead to the depletion of the resource that discharge was supporting (e.g., drying up streams and wetlands) and can result in perpetual groundwater mining if wells are too far from the discharge zones to effectively capture water.

**9. (Boundary Condition Categories):** The three main boundary condition categories are:

* **Head Boundaries:** These specify the hydraulic head value.
    * **Example 1 - Constant Head:** Represents a large lake or river with a very permeable connection to the aquifer, where the water level dictates the aquifer head at the boundary.
    * **Example 2 - Head-Dependent:** Represents a river with a semi-permeable riverbed. The flow into or out of the aquifer depends on the head difference between the river stage and the aquifer head, and the conductance of the riverbed.
* **Specified Flow Boundaries:** These specify a rate of flow into or out of the model.
    * **Example 1 - Lateral Inflow/Mountain Front Recharge:** Represents subsurface flow entering an alluvial basin from an adjacent mountain block, often estimated from a hydrologic analysis.
    * **Example 2 - Injection Well:** A well used to inject water into the aquifer at a known, constant rate can be simulated as a specified flow boundary condition at a single cell.
* **No-Flow Boundaries:** These specify that there is zero flow across the boundary.
    * **Example 1 - Physical Barrier:** Represents an impermeable geologic feature, such as a bedrock valley wall or a very low-permeability fault, that physically blocks groundwater flow.
    * **Example 2 - Groundwater Divide:** A line along the crest of the water table from which groundwater flows away in opposite directions. No flow occurs across this line, so it can be used as a no-flow boundary.

**10. (Stochastic Simulation Process):** The process would be as follows:

* **Setup the Stochastic Model:** Identify key uncertain parameters, such as the hydraulic conductivity (K) of different zones and the recharge rate. For each, define a probability distribution (e.g., log-normal for K, normal for recharge) with a mean and standard deviation based on calibration results and professional judgment.
* **Generate Model Instances:** Using a method like Random Sampling or Latin Hypercube, generate a large number (N, e.g., 500) of model "instances" or runs. Each run will have a unique combination of K and recharge values drawn from their respective distributions.
* **Run All Models:** Execute all 500 MODFLOW simulations. These will be transient runs with a duration of at least 10 years.
* **Perform Particle Tracking for Each Run:** For each of the 500 converged solutions, run a MODPATH simulation. In each MODPATH run, place particles at the landfill location. Track the particles forward in time.
* **Tally the Outcome:** For each of the 500 MODPATH runs, determine if any particle from the landfill reaches the municipal well within the 10-year (3652 days) simulation time. Keep a count of the number of "yes" outcomes.
* **Calculate Probability:** The final probability is the number of instances where contamination occurred divided by the total number of runs. For example, if the well was contaminated in 400 out of the 500 runs, the conclusion would be that there is an 80% probability of contamination within 10 years.

---

## Glossary of Key Terms

| Term | Definition |
|:-----|:-----------|
| **Aquifer Compressibility (α)** | The property of an aquifer matrix that describes its change in volume in response to a change in effective stress. It is the inverse of the modulus of elasticity. |
| **Aquifer Subsidence** | The lowering of the ground surface elevation caused by the compression of an aquifer matrix, typically due to excessive groundwater withdrawal increasing effective stress. This process is often non-elastic, resulting in a permanent loss of storage capacity. |
| **Capture** | The process by which pumping wells intercept groundwater that would have otherwise discharged naturally to features like streams, springs, or phreatophytes, or by inducing additional recharge into the aquifer. For pumping to be sustainable, it must eventually be balanced by capture. |
| **Capture Zone** | The three-dimensional region of an aquifer from which groundwater flows to a pumping well. |
| **Changing Head (CHD) Package** | A MODFLOW package used to simulate specified head boundary conditions that change over time. It allows head to vary linearly within a stress period. |
| **Convertible Layer** | A MODFLOW layer type that can switch between confined and unconfined conditions during a simulation. It requires both specific storage and specific yield as input. |
| **Groundwater Divide** | An underground feature, analogous to a watershed divide on the surface, that represents the high point in the water table. Groundwater on opposite sides of the divide flows in different directions. It can be used as a no-flow boundary. |
| **Groundwater Mining** | A state where groundwater is extracted at a rate that exceeds the natural rate of replenishment over a long period, causing a continuous and long-term decline in the water table without reaching a new state of equilibrium. |
| **Latin Hypercube Sampling** | A structured statistical method for generating parameter sets for stochastic simulations. It divides the probability distribution of each parameter into segments and ensures that samples are drawn from every combination of segments, providing a more thorough exploration of the parameter space with fewer model runs than simple random sampling. |
| **MODPATH** | A companion post-processing program for MODFLOW that uses the velocity fields from a MODFLOW solution to track the movement of hypothetical particles through an aquifer over time. |
| **Monte Carlo Analysis** | A type of stochastic modeling that uses repeated random sampling to obtain numerical results, often to understand the impact of uncertainty. In groundwater modeling, it involves running a model many times with different, randomly generated parameter values. |
| **Parallel Flow Boundary** | A type of no-flow boundary condition represented by a line drawn parallel to the direction of groundwater flow (and perpendicular to head contours). |
| **Particle Set** | In MODPATH, a group of particles with a common set of tracking options, such as tracking direction (forward/backward) and duration. |
| **Pathline** | The trajectory or flow path of a single hypothetical particle of water as computed by MODPATH. |
| **Perennial Yield** | The maximum amount of groundwater that can be withdrawn from an aquifer annually for an indefinite period without causing unacceptable consequences. Also known as safe yield or sustainable yield. |
| **Probabilistic Capture Zone** | A result from a stochastic simulation where each cell in the model grid is assigned a probability value representing the likelihood that groundwater originating from that cell will be captured by a well. |
| **Regional-to-Local Model Conversion** | A modeling strategy where a large, regional-scale model with well-defined physical boundaries is built and calibrated first. The results of this model are then used to define the boundary conditions and parameters for a smaller, more detailed local-scale model. Also known as telescopic grid refinement. |
| **Specific Storage (Sₛ)** | The volume of water that a unit volume of a saturated aquifer releases from storage per unit decline in hydraulic head. It is due to the combined effects of aquifer matrix compression and pore water expansion. |
| **Specific Yield (Sᵧ)** | The volume of water that a unit area of an unconfined aquifer releases from storage per unit decline in the water table. It is primarily due to the gravity drainage of water from the de-saturated pores and is much larger than storativity. Also called unconfined storativity. |
| **Stochastic Simulation** | A modeling approach that generates many possible outcomes ("realizations" or "instances") by allowing for randomness in inputs, thereby representing uncertainty. The results are analyzed statistically to determine probabilities of different outcomes. |
| **Storativity (S)** | The volume of water that a unit area of a confined aquifer releases from storage per unit decline in hydraulic head. It is a dimensionless parameter equal to specific storage multiplied by the aquifer thickness (S = Sₛ * b). |
| **Stress Period** | In a transient MODFLOW simulation, a period of time during which all model inputs (stresses), such as pumping rates and recharge, are held constant. |
| **Time Step** | A computational interval within a stress period for which MODFLOW calculates a solution. A stress period can be divided into multiple time steps. |
| **Transitional Storage** | The volume of water that is removed from storage in an aquifer as it evolves from an initial state of equilibrium to a new state of equilibrium after a new stress (like pumping) is introduced. |
| **Water Budget Myth** | The common misconception that the amount of groundwater that can be sustainably pumped from a basin is equal to the average rate of natural recharge. This is a myth because it ignores the dynamics of capture and the fact that pumping is ultimately balanced by a reduction in natural discharge. |
