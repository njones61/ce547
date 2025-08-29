# MODFLOW Simulation Analysis with FloPy

This code provides a comprehensive workflow for loading, analyzing, and visualizing MODFLOW groundwater flow simulations using FloPy.

## Features

- **Model Loading**: Automatically loads existing MODFLOW simulations or creates model structure from individual files
- **Result Analysis**: Loads and analyzes head distributions, budget files, and other outputs
- **Visualization**: Creates comprehensive plots including head distributions, contours, histograms, and budget information
- **Performance Analysis**: Analyzes model convergence and performance metrics

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. **Basic Analysis**: Run the script to analyze existing simulation results:
   ```bash
   python main_flopy.py
   ```

2. **Run New Simulation**: Uncomment the simulation line in the main function to run a new MODFLOW simulation:
   ```python
   run_modflow_simulation(mf, str(model_path))
   ```

## Output

The script will:
- Load the MODFLOW model from `bbottoms_MODFLOW/`
- Display model information and available packages
- Load existing simulation results
- Analyze model performance
- Create visualizations saved as `bbottoms_results.png`

## Model Structure

The code is designed to work with MODFLOW-2000 models and automatically detects:
- Model discretization (layers, rows, columns)
- Hydraulic properties
- Boundary conditions (recharge, rivers, wells, drains)
- Output control settings

## Troubleshooting

- **Missing .nam file**: The code will automatically create a model structure from individual files
- **Binary file errors**: Some MODFLOW output files are binary and require FloPy utilities to read
- **HDF5 files**: Requires h5py package for reading HDF5 format arrays

## Customization

Modify the visualization functions to create custom plots or add additional analysis capabilities specific to your needs.
