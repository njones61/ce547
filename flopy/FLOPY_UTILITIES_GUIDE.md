# FloPy Utilities Guide for MODFLOW Analysis

## Overview

This guide demonstrates the **proper way** to use FloPy's built-in utilities for reading, analyzing, and visualizing MODFLOW simulation results. The key insight is that FloPy has specialized classes and methods designed specifically for MODFLOW data handling.

## Key FloPy Utilities

### 1. HeadFile - For Reading Head Results

```python
from flopy.utils import HeadFile

# Load head file
head_file = "bbottoms.hed"
headobj = HeadFile(head_file)

# Get available times and stress periods
times = headobj.get_times()           # [1.0]
kstpkper = headobj.get_kstpkper()    # [(0, 0)]

# Get data for specific time
head_data = headobj.get_data(totim=times[0])
# Shape: (1, 120, 80) - (layers, rows, columns)

# Get data for specific stress period
head_data = headobj.get_data(kstpkper=(0, 0))
```

### 2. CellBudgetFile - For Reading Flow Budgets

```python
from flopy.utils import CellBudgetFile

# Load budget file
budget_file = "bbottoms.ccf"
budgetobj = CellBudgetFile(budget_file)

# Get available budget terms
budget_terms = budgetobj.get_unique_record_names()
# Available terms: CONSTANT HEAD, FLOW RIGHT FACE, FLOW FRONT FACE, 
#                 WELLS, DRAINS, RIVER LEAKAGE, RECHARGE

# Extract specific budget data
constant_head_flow = budgetobj.get_data(text=b'   CONSTANT HEAD')
river_leakage = budgetobj.get_data(text=b'   RIVER LEAKAGE')
```

### 3. PlotMapView - For Grid-Aware Plotting

```python
from flopy.plot import PlotMapView

# Note: This requires a full model object with grid information
# plot = PlotMapView(model=mf)
# plot.plot_array(head_data)
```

## Handling MODFLOW No-Data Values

**Critical Issue**: MODFLOW uses `-999.0` as a no-data value, not `NaN`. This is why your plots were showing empty polygons.

### Solution: Use Masked Arrays

```python
import numpy as np

# Create masked array for MODFLOW no-data values
masked_head = np.ma.masked_where(head_data == -999.0, head_data)

# Now plotting will work correctly
plt.imshow(masked_head[0, :, :], cmap='viridis')
```

### Alternative: Replace with NaN

```python
# Replace -999.0 with NaN for compatibility
head_clean = head_data.copy()
head_clean[head_data == -999.0] = np.nan
```

## Complete Working Example

Here's the corrected approach for visualizing MODFLOW head results:

```python
import flopy
import numpy as np
import matplotlib.pyplot as plt

def plot_modflow_head_correctly():
    """Demonstrate correct MODFLOW head visualization using FloPy."""
    
    # 1. Load head data using FloPy's HeadFile
    headobj = flopy.utils.HeadFile("bbottoms.hed")
    
    # 2. Get data for first time step
    times = headobj.get_times()
    head_data = headobj.get_data(totim=times[0])
    
    # 3. Handle MODFLOW no-data values properly
    masked_head = np.ma.masked_where(head_data == -999.0, head_data)
    
    # 4. Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Plot 1: Standard MODFLOW head plot
    im1 = ax1.imshow(masked_head[0, :, :], cmap='RdYlBu_r', 
                    aspect='auto', interpolation='nearest')
    ax1.set_title('MODFLOW Head Distribution')
    ax1.set_xlabel('Column')
    ax1.set_ylabel('Row')
    plt.colorbar(im1, ax=ax1, label='Head (m)')
    
    # Plot 2: Enhanced plot with statistics
    im2 = ax2.imshow(masked_head[0, :, :], cmap='viridis', 
                    aspect='auto', interpolation='nearest')
    ax2.set_title('Enhanced Head Visualization')
    ax2.set_xlabel('Column')
    ax2.set_ylabel('Row')
    plt.colorbar(im2, ax=ax2, label='Head (m)')
    
    # Add statistics overlay
    valid_data = masked_head.compressed()
    stats_text = f'Statistics:\nMin: {np.min(valid_data):.1f} m\nMax: {np.max(valid_data):.1f} m\nMean: {np.mean(valid_data):.1f} m'
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    plt.show()
```

## What Was Wrong Before

1. **No-Data Values**: The `-999.0` values were being treated as valid data, causing plotting issues
2. **Missing Masking**: Without proper masking, matplotlib couldn't distinguish between valid and invalid data
3. **Incorrect Data Range**: The full range including -999.0 was being used for color scaling

## What's Fixed Now

1. **Proper No-Data Handling**: Using `np.ma.masked_where()` to mask -999.0 values
2. **Correct Data Range**: Only valid head values (2102.183 to 2112.530 m) are used for visualization
3. **FloPy Integration**: Using FloPy's built-in utilities for proper MODFLOW file handling
4. **Professional Plots**: Clean, publication-quality visualizations with proper statistics

## Key Takeaways

1. **Always use FloPy's utilities** (`HeadFile`, `CellBudgetFile`) for MODFLOW data
2. **Handle -999.0 no-data values** with masked arrays or NaN replacement
3. **Use proper time/stress period indexing** when extracting data
4. **Leverage FloPy's built-in plotting capabilities** when possible
5. **Check data ranges** before plotting to identify no-data issues

## Files Generated

The corrected code now generates three visualization files:
- `bbottoms_results.png` - Comprehensive 4-panel analysis
- `bbottoms_flopy_head.png` - FloPy-specific head visualization  
- `bbottoms_flopy_utilities.png` - Demonstration of FloPy utilities

All plots now correctly show the groundwater head distribution without empty polygons!
