# Pre-Class - The FloPy Python Package

## Overview

FloPy is a Python package designed for creating, running, and post-processing MODFLOW-based groundwater models. It provides a comprehensive Python interface to work with multiple versions of MODFLOW and related groundwater modeling programs. The package enables users to programmatically build, modify, and analyze groundwater flow models while leveraging the power of Python's scientific computing ecosystem.

FloPy supports several MODFLOW versions including:<br>
- MODFLOW 6<br>
- MODFLOW-2005<br>
- MODFLOW-NWT (Newton formulation)<br>
- MODFLOW-USG (Unstructured Grid)

Additionally, FloPy works with related programs such as MT3DMS (solute transport), SEAWAT (variable-density flow), and MODPATH (particle tracking).

For most problems, building MODFLOW models with GMS is the most efficient way to develop and run groundwater models. 
However, FloPy can be useful for automating model runs and post-processing results. For example, you can use FloPy 
to create a series of MODFLOW models with different boundary conditions and run them and plot results in a single 
script. You can also perform sensitivity analyses using FloPy to explore the impact of different model parameters. 
You can import existing MODFLOW models created in GMS into FloPy and analyze them using FloPy's powerful data analysis 
tools.

## When to Use FloPy

FloPy is particularly beneficial in the following scenarios:

1. **Automated Model Development**: When you need to create multiple model scenarios or perform sensitivity analyses that would be tedious using GUI-based tools.

2. **Reproducible Research**: FloPy scripts provide a complete record of model development, making your work transparent and reproducible for scientific publications.

3. **Complex Grid Generation**: When working with irregular boundaries or complex hydrogeological features that require programmatic grid discretization.

4. **Data Integration**: When you need to integrate groundwater models with other data sources (databases, GIS, remote sensing) or couple models with optimization routines.

5. **Post-Processing and Visualization**: FloPy provides powerful tools for analyzing model outputs, creating visualizations, and exporting results to various formats (NetCDF, shapefiles, etc.).

6. **Batch Processing**: When running multiple model simulations with different parameters or boundary conditions.

7. **Version Control**: Python scripts can be managed with version control systems (like Git), allowing you to track changes to your models over time.

## Installation

### Using Conda (Recommended)

The recommended method is to install FloPy using conda from the conda-forge channel:

```bash
conda install -c conda-forge flopy
```

### Using Pip

Alternatively, you can install FloPy using pip:

```bash
pip install flopy
```

### Installing the Latest Development Version

To install the bleeding-edge version directly from GitHub:

```bash
pip install git+https://github.com/modflowpy/flopy.git
```

### Installing MODFLOW Executables

After installing FloPy, you can install MODFLOW and related program executables using:

```bash
get-modflow :flopy
```

This command will download and install the necessary MODFLOW executables for your system.

## Using FloPy with Google Colab

Google Colab is an excellent platform for running FloPy models, especially for students or researchers who want to run models without local installations. Here's how to set up and use FloPy in Google Colab:

### Installation in Colab

At the beginning of your Colab notebook, add the following cells:

```python
# Install FloPy
!pip install flopy

# Install MODFLOW executables
!get-modflow :flopy
```

### Complete Colab Setup Example

Here's a complete setup that you can use at the start of any Colab notebook:

```python
# Install FloPy and MODFLOW executables
!pip install -q flopy
!get-modflow :flopy

# Import necessary libraries
import flopy
import numpy as np
import matplotlib.pyplot as plt
import os

# Verify installation
print(f"FloPy version: {flopy.__version__}")

# Check MODFLOW executables
import flopy.utils
exe_name = 'mf6'
exe_path = flopy.which(exe_name)
if exe_path:
    print(f"MODFLOW 6 executable found at: {exe_path}")
else:
    print("Warning: MODFLOW executable not found!")
```

### Working with Files in Colab

When working with FloPy in Colab, keep these points in mind:

1. **Workspace Directories**: Use relative paths for your model workspace. Files will be saved in your Colab session's filesystem.

```python
# Create a workspace directory
model_ws = './my_model'
os.makedirs(model_ws, exist_ok=True)
```

2. **Persistence**: Files in Colab are temporary. To save your work:
   - Mount Google Drive to save models and results
   - Download files to your local machine

```python
# Mount Google Drive (optional, for persistent storage)
from google.colab import drive
drive.mount('/content/drive')

# Use a Drive folder for your model
model_ws = '/content/drive/MyDrive/groundwater_models/model1'
os.makedirs(model_ws, exist_ok=True)
```

3. **Downloading Results**: Download output files from Colab to your computer:

```python
from google.colab import files

# Download a specific file
files.download('./model_output/gwf_model.hds')

# Or zip multiple files
!zip -r model_results.zip ./model_output
files.download('model_results.zip')
```

### Tips for Using FloPy in Colab

- **Runtime Type**: Standard CPU runtime is sufficient for most FloPy models. You don't need GPU for MODFLOW simulations.

- **Session Timeout**: Colab sessions timeout after periods of inactivity. For long-running models, periodically interact with the notebook.

- **Memory Limits**: Free Colab accounts have memory limitations (~12 GB RAM). Very large models may require Colab Pro or local execution.

- **Visualization**: Matplotlib works perfectly in Colab for plotting heads, budgets, and model grids. Plots display inline automatically.

## Example Scripts

### Example 1: Creating a Simple MODFLOW 6 Groundwater Flow Model

```python
import flopy
import numpy as np

# Create a new MODFLOW 6 simulation
sim_name = 'simple_model'
sim = flopy.mf6.MFSimulation(sim_name=sim_name,
                              exe_name='mf6',
                              version='mf6',
                              sim_ws='./model_output')

# Create the temporal discretization package
tdis = flopy.mf6.ModflowTdis(sim,
                              nper=1,
                              perioddata=[(1.0, 1, 1.0)])

# Create the groundwater flow model
model_name = 'gwf_model'
gwf = flopy.mf6.ModflowGwf(sim, modelname=model_name)

# Create the Iterative Model Solution (IMS) package
ims = flopy.mf6.ModflowIms(sim,
                           print_option='ALL',
                           outer_dvclose=1e-5,
                           inner_dvclose=1e-6)

# Create the discretization package
nlay, nrow, ncol = 3, 10, 10
delr = delc = 100.0  # cell size in meters
top = 100.0
botm = [95.0, 90.0, 85.0]

dis = flopy.mf6.ModflowGwfdis(gwf,
                               nlay=nlay,
                               nrow=nrow,
                               ncol=ncol,
                               delr=delr,
                               delc=delc,
                               top=top,
                               botm=botm)

# Create the initial conditions package
start_head = 95.0
ic = flopy.mf6.ModflowGwfic(gwf, strt=start_head)

# Create the node property flow package
k = 10.0  # hydraulic conductivity in m/day
npf = flopy.mf6.ModflowGwfnpf(gwf, k=k)

# Create constant head boundary on left side
chd_rec = []
for layer in range(nlay):
    for row in range(nrow):
        chd_rec.append(((layer, row, 0), 100.0))  # (cellid, head)

chd = flopy.mf6.ModflowGwfchd(gwf,
                               stress_period_data=chd_rec)

# Create well package (pumping well in center)
wel_rec = [((1, 5, 5), -1000.0)]  # (cellid, pumping rate in m3/day)
wel = flopy.mf6.ModflowGwfwel(gwf,
                               stress_period_data=wel_rec)

# Create the output control package
oc = flopy.mf6.ModflowGwfoc(gwf,
                             head_filerecord=f'{model_name}.hds',
                             saverecord=[('HEAD', 'ALL')],
                             printrecord=[('BUDGET', 'ALL')])

# Write the simulation files
sim.write_simulation()

# Run the simulation
success, buff = sim.run_simulation()
if success:
    print('Model ran successfully!')
else:
    print('Model failed to run.')
```

### Example 2: Loading and Analyzing an Existing MODFLOW Model

```python
import flopy
import numpy as np
import matplotlib.pyplot as plt

# Load an existing MODFLOW-2005 model
model_ws = './existing_model'  # workspace directory
model_name = 'mymodel'

# Load the model
ml = flopy.modflow.Modflow.load(f'{model_name}.nam',
                                 model_ws=model_ws,
                                 check=False)

print(f'Model name: {ml.name}')
print(f'Number of layers: {ml.nlay}')
print(f'Number of rows: {ml.nrow}')
print(f'Number of columns: {ml.ncol}')

# Access model packages
dis = ml.get_package('DIS')
bas = ml.get_package('BAS6')
lpf = ml.get_package('LPF')

# Get hydraulic conductivity array
k_array = lpf.hk.array
print(f'K array shape: {k_array.shape}')

# Modify the model (e.g., change hydraulic conductivity)
new_k = k_array * 1.5
lpf.hk = new_k

# Write modified model to a new workspace
new_ws = './modified_model'
ml.change_model_ws(new_ws)
ml.write_input()

# Run the modified model
success, buff = ml.run_model()

if success:
    # Read the head file
    import flopy.utils.binaryfile as bf

    hds = bf.HeadFile(f'{new_ws}/{model_name}.hds')
    head = hds.get_data()  # Get head for last time step

    # Create a simple plot of heads for layer 0
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create model map
    modelmap = flopy.plot.PlotMapView(model=ml, layer=0, ax=ax)

    # Plot head contours
    contours = modelmap.contour_array(head, levels=10)
    plt.colorbar(contours, ax=ax, label='Head (m)')

    # Plot grid
    modelmap.plot_grid()

    plt.title('Simulated Hydraulic Head - Layer 1')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.savefig(f'{new_ws}/head_map.png', dpi=300, bbox_inches='tight')
    plt.show()

    print('Post-processing complete!')
else:
    print('Model run failed.')
```

These examples demonstrate FloPy's capabilities for both creating new models from scratch and working with existing models. The first example shows how to build a simple three-layer MODFLOW 6 model with constant head boundaries and a pumping well. The second example demonstrates loading an existing model, modifying parameters, running the simulation, and visualizing the results. 