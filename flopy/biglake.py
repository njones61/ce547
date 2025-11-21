# In this script we will import a previously constructed flow model of the Big Valley site
# and illustrate how to visualize and run the model using flopy.

# Import necessary libraries
import flopy
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import flopy.plot as fp

def plot_inputs(model):
    """
    Plot model inputs including grid and boundary conditions.

    Parameters:
    -----------
    model : flopy.modflow.Modflow
        The MODFLOW model object
    """
    # Create a figure with specified size
    fig = plt.figure(figsize=(10, 6))

    # Create the plotmapview object
    pmap = fp.PlotMapView(model=model, layer=0)

    # Plot the grid
    pmap.plot_grid(lw=0.5, color="0.5")
    pmap.plot_inactive(color_noflow='gray')

    # Plot boundary conditions
    # Specified head cells (ibound = -1)
    ibound = model.bas6.ibound.array[0]
    if np.any(ibound == -1):
        pmap.plot_ibound(color_ch='blue', alpha=0.3)

    # Plot wells
    if hasattr(model, 'wel') and model.wel is not None:
        wel_data = model.wel.stress_period_data[0]
        for well in wel_data:
            k, i, j = int(well[0]), int(well[1]), int(well[2])
            # Get cell center coordinates
            x = model.modelgrid.xcellcenters[i, j]
            y = model.modelgrid.ycellcenters[i, j]
            plt.plot(x, y, 'ro', markersize=10, label='Wells' if well is wel_data[0] else '')

    # Plot rivers
    if hasattr(model, 'riv') and model.riv is not None:
        riv_data = model.riv.stress_period_data[0]
        for idx, riv in enumerate(riv_data):
            k, i, j = int(riv[0]), int(riv[1]), int(riv[2])
            x = model.modelgrid.xcellcenters[i, j]
            y = model.modelgrid.ycellcenters[i, j]
            plt.plot(x, y, 'cs', markersize=6, alpha=0.6, label='River' if idx == 0 else '')

    # Plot GHB (general head boundaries)
    if hasattr(model, 'ghb') and model.ghb is not None:
        ghb_data = model.ghb.stress_period_data[0]
        for idx, ghb in enumerate(ghb_data):
            k, i, j = int(ghb[0]), int(ghb[1]), int(ghb[2])
            x = model.modelgrid.xcellcenters[i, j]
            y = model.modelgrid.ycellcenters[i, j]
            plt.plot(x, y, 'g^', markersize=5, alpha=0.5, label='GHB' if idx == 0 else '')

    # Create custom legend entry for specified heads
    if np.any(ibound == -1):
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='blue', alpha=0.3, label='Specified Head')]

        # Add other BC elements
        if hasattr(model, 'wel') and model.wel is not None:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w',
                                             markerfacecolor='r', markersize=10, label='Wells'))
        if hasattr(model, 'riv') and model.riv is not None:
            legend_elements.append(plt.Line2D([0], [0], marker='s', color='w',
                                             markerfacecolor='c', markersize=6, label='River'))
        if hasattr(model, 'ghb') and model.ghb is not None:
            legend_elements.append(plt.Line2D([0], [0], marker='^', color='w',
                                             markerfacecolor='g', markersize=5, label='GHB'))

        plt.legend(handles=legend_elements, loc='best', fontsize=10)

    # Add title and labels
    plt.title(f'Model Inputs and Boundary Conditions - {model.name}')
    plt.xlabel('X-coordinate [m]')
    plt.ylabel('Y-coordinate [m]')

    plt.show()

def plot_solution(model, head, pathlines=None, max_time=None):
    """
    Plot head distribution with contours and optionally pathlines.

    Parameters:
    -----------
    model : flopy.modflow.Modflow
        The MODFLOW model object
    head : numpy array
        Head array with shape (nlay, nrow, ncol)
    pathlines : list of numpy recarrays or None, optional
        Pathline data from PathlineFile.get_alldata()
    max_time : float or None, optional
        Maximum time (in days) to display pathlines. If None, show all.
    """
    # Create a figure with specified size (width, height in inches)
    fig = plt.figure(figsize=(10, 6))
    
    # Create the plotmapview object
    pmap = fp.PlotMapView(model=model)
    
    # Plot the heads
    im = pmap.plot_array(head, cmap='viridis')
    pmap.plot_inactive()
    pmap.plot_ibound()
    
    # Plot the grid lines
    pmap.plot_grid(lw=0.5, color="0.5")
    
    # Add contours
    interval = 2.0
    levels = np.arange(np.floor(head.min()), np.ceil(head.max()) + interval, interval)
    cs = pmap.contour_array(head, levels=levels, colors='black', linewidths=1.5)
    plt.clabel(cs, fmt='%1.1f')
    
    # Plot pathlines if provided, colored by particle group
    if pathlines is not None:
        # Filter pathlines by max_time if specified
        if max_time is not None:
            filtered_pathlines = []
            for pline in pathlines:
                # Filter points where time <= max_time
                mask = pline['time'] <= max_time
                if np.any(mask):
                    filtered_pathlines.append(pline[mask])
            pathlines = filtered_pathlines

        # Group pathlines by particle group (each well creates a group)
        from collections import defaultdict
        pathlines_by_group = defaultdict(list)

        for pline in pathlines:
            # Get particle group number (should be in the data)
            # If particlegroup field exists, use it; otherwise infer from particleid
            if 'particlegroup' in pline.dtype.names:
                group_id = pline['particlegroup'][0]
            else:
                # Infer group from particle ID (96 particles per well in this case)
                particle_id = pline['particleid'][0]
                group_id = (particle_id - 1) // 96  # 0, 1, or 2
            pathlines_by_group[group_id].append(pline)

        # Define colors for different wells
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']
        well_names = ['Well 1 (L1,R28,C65)', 'Well 2 (L1,R35,C34)', 'Well 3 (L1,R68,C88)']

        # Plot each group with a different color
        for group_id in sorted(pathlines_by_group.keys()):
            plines = pathlines_by_group[group_id]
            color = colors[group_id % len(colors)]
            label = well_names[group_id] if group_id < len(well_names) else f'Well {group_id+1}'
            pmap.plot_pathline(plines, colors=color, linewidths=1.0, alpha=0.7, label=label)

        # Add legend
        plt.legend(loc='best', fontsize=8)
    
    # Add a color bar
    plt.colorbar(im, label='Head [m]', shrink=0.8)
    
    # Add title and labels
    title = f'Head Distribution - {model.name}'
    if pathlines is not None:
        title += ' with Pathlines'
    plt.title(title)
    plt.xlabel('X-coordinate [m]')
    plt.ylabel('Y-coordinate [m]')
    
    plt.show()

# Create a workspace directory
model_ws = './my_model'
os.makedirs(model_ws, exist_ok=True)

import_ws = './biglake'

########################################################
# PART 2a - Load and run the model
########################################################

# Load the model (exclude observation packages that may have parsing issues)
print("Loading MODFLOW model...")
ml = flopy.modflow.Modflow.load('biglake.mfn', model_ws=import_ws,
                                 load_only=['dis', 'bas6', 'lpf', 'rch', 'wel', 'riv', 'ghb', 'pcg', 'oc'],
                                 check=False, version='mf2k', exe_name='mf2000')

# Change model workspace to new location (so original files aren't modified)
ml.change_model_ws(model_ws)

# Print summary information
print("\n" + "="*60)
print("MODEL SUMMARY")
print("="*60)
print(f"Model name: {ml.name}")
print(f"Model packages: {', '.join(ml.get_package_list())}")
print(f"Model dimensions: {ml.nlay} layers, {ml.nrow} rows, {ml.ncol} columns")
print(f"Grid spacing (delr): {ml.dis.delr.array.min():.2f} to {ml.dis.delr.array.max():.2f} [m]")
print(f"Grid spacing (delc): {ml.dis.delc.array.min():.2f} to {ml.dis.delc.array.max():.2f} [m]")
print(f"Number of stress periods: {ml.nper}")
print(f"Time units: {ml.dis.itmuni_dict[ml.dis.itmuni]} [d]")
# Length units: 0=undefined, 1=feet, 2=meters, 3=centimeters
lenuni_names = {0: 'undefined', 1: 'feet', 2: 'meters', 3: 'centimeters'}
lenuni_name = lenuni_names.get(ml.dis.lenuni, 'unknown')
print(f"Length units: {lenuni_name} [m]")

# Print boundary conditions info
ibound = ml.bas6.ibound.array
n_active = np.sum(ibound == 1)
n_inactive = np.sum(ibound == 0)
n_specified = np.sum(ibound == -1)
print(f"\nBoundary conditions:")
print(f"  Active cells: {n_active}")
print(f"  Inactive cells: {n_inactive}")
print(f"  Specified head cells: {n_specified}")

# Print initial head info (only for active cells)
strt = ml.bas6.strt.array
ibound = ml.bas6.ibound.array
# Mask out inactive cells (ibound == 0)
strt_active = strt[ibound != 0]
print(f"\nInitial head (active cells only):")
print(f"  Minimum: {strt_active.min():.2f} [m]")
print(f"  Maximum: {strt_active.max():.2f} [m]")
print(f"  Mean: {strt_active.mean():.2f} [m]")

# Print hydraulic conductivity info (only for active cells)
if hasattr(ml, 'lpf') and ml.lpf is not None:
    hk = ml.lpf.hk.array
    # Mask out inactive cells (ibound == 0)
    hk_active = hk[ibound != 0]
    print(f"\nHydraulic conductivity (HK, active cells only):")
    print(f"  Minimum: {hk_active.min():.6e} [m/d]")
    print(f"  Maximum: {hk_active.max():.6e} [m/d]")
    print(f"  Mean: {hk_active.mean():.6e} [m/d]")

print("="*60)

# Plot model inputs and boundary conditions
print("\nPlotting model inputs and boundary conditions...")
plot_inputs(ml)

# Write model files to new workspace
print("\nWriting model files to new workspace...")
ml.write_input()

# Fix GHB and RIV file formatting (FloPy uses insufficient field width for MODFLOW-2000)
import re

def fix_modflow_file_formatting(file_path):
    """
    Fix concatenated numbers in MODFLOW boundary condition files (GHB, RIV).
    FloPy sometimes writes numbers without sufficient spacing, causing concatenation.
    This function splits concatenated numbers and truncates the right number to maintain alignment.
    
    Args:
        file_path: Path to the MODFLOW file to fix
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for line in lines:
        # Helper function to truncate decimal part by n digits
        def truncate_decimal(decimal_str, n_digits):
            """Truncate the decimal part (after '0.') by n_digits from the right"""
            if n_digits <= 0:
                return decimal_str
            # decimal_str is like "0.00616674"
            if len(decimal_str) <= 2 + n_digits:  # "0." + at least n_digits
                # If too short, just return "0." or minimal value
                if len(decimal_str) <= 2:
                    return "0."
                return decimal_str[:len(decimal_str) - n_digits]
            return decimal_str[:-n_digits]
        
        # 1. Decimal number followed by "0." -> "117.6050.00616674" -> "117.605 0.0061667" (drop 1 digit)
        def fix_decimal_concatenation(match):
            left_part = match.group(1)
            right_part = match.group(2)  # "0.00616674"
            # We're adding 1 space, so drop 1 digit from right_part
            truncated_right = truncate_decimal(right_part, 1)
            return f'{left_part} {truncated_right}'
        
        fixed_line = re.sub(r'(\d+\.\d+)(0\.\d+)', fix_decimal_concatenation, line)
        
        # 2. Integer followed by "0." -> "1200.003" -> "120 0.00" (drop 1 digit)
        #    But avoid matching valid decimals like "120.0" (which should not be changed)
        def fix_integer_concatenation(match):
            start_pos = match.start()
            digits = match.group(1)
            zero_decimal = match.group(2)
            
            # Check if digits are part of an existing decimal number
            if start_pos > 0:
                # Check if immediately before is a digit, and before that might be a '.'
                if start_pos >= 2:
                    two_before = line[start_pos-2:start_pos]
                    if re.match(r'\d\.', two_before):
                        return match.group(0)  # Part of decimal like 'X.120.0'
                # Check if before is a digit
                if line[start_pos-1].isdigit():
                    # Could be part of decimal - check further back
                    lookback = max(0, start_pos-5)
                    preceding = line[lookback:start_pos]
                    if '.' in preceding:
                        # There's a decimal point before, might be part of decimal number
                        if re.search(r'\d\.\d*$', preceding):
                            return match.group(0)  # Don't change - part of decimal
            
            # Only split if there are 3+ digits (indicating likely concatenation)
            # Valid decimals like '10.0', '120.0' typically have 1-3 digits
            if len(digits) >= 4:
                # 4+ digits almost certainly concatenated (like '1200.003')
                # We're adding 1 space, so drop 1 digit from zero_decimal
                truncated_decimal = truncate_decimal(zero_decimal, 1)
                return f'{digits} {truncated_decimal}'
            elif len(digits) >= 3:
                # For 3 digits, be more careful - only split if at field start
                # and not part of a decimal (already checked above)
                if start_pos == 0 or (start_pos > 0 and line[start_pos-1].isspace()):
                    truncated_decimal = truncate_decimal(zero_decimal, 1)
                    return f'{digits} {truncated_decimal}'
            
            return match.group(0)  # Don't change short numbers (1-2 digits)
        
        fixed_line = re.sub(r'(\d+)(0\.\d+)', fix_integer_concatenation, fixed_line)
        fixed_lines.append(fixed_line)
    
    with open(file_path, 'w') as f:
        f.writelines(fixed_lines)

# Fix both GHB and RIV files
for fname in ['biglake.ghb', 'biglake.riv']:
    fpath = os.path.join(model_ws, fname)
    fix_modflow_file_formatting(fpath)

# Run the MODFLOW model
print("\nRunning MODFLOW model...")
success, buff = ml.run_model(silent=True, report=True)

if success:
    print("Model ran successfully!")
    
    # Load head results
    print("\nLoading head results from output file...")
    head_file = os.path.join(model_ws, 'biglake.hed')
    hds = flopy.utils.binaryfile.HeadFile(head_file)
    
    # Get head for the last time step
    times = hds.get_times()
    head = hds.get_data(totim=times[-1])
    print(f"Head data loaded for time: {times[-1]}")
    
    # Print some head statistics (only for active cells)
    ibound = ml.bas6.ibound.array
    # Mask out inactive cells (ibound == 0)
    head_active = head[ibound != 0]
    print(f"\nHead statistics (active cells only):")
    print(f"  Minimum: {head_active.min():.2f} [m]")
    print(f"  Maximum: {head_active.max():.2f} [m]")
    print(f"  Mean: {head_active.mean():.2f} [m]")
    
    # Plot the heads
    print("\nPlotting head distribution...")
    plot_solution(ml, head)
    
    print("\nDone!")
else:
    print("Model did not run successfully.")
    if isinstance(buff, list):
        print('\n'.join(buff))
    else:
        print(buff)

########################################################
# PART 2b Particle Tracking Analysis
########################################################

if success:
    print("\n" + "="*60)
    print("PARTICLE TRACKING ANALYSIS")
    print("="*60)

    try:
        import flopy.modpath as mp

        # Set particle tracking time limit (days) for visualization
        tracking_time_days = 3650  # 10 years

        # Create MODPATH6 model
        mp_name = f'{ml.name}_mp'
        mp_model = mp.Modpath6(
            modelname=mp_name,
            modflowmodel=ml,
            exe_name='mp6',
            model_ws=model_ws
        )

        # Create MODPATH6 BAS package with porosity
        mpbas = mp.Modpath6Bas(mp_model, prsity=0.3)

        # Create simulation for backward tracking from wells
        print(f"\nTracking particles backward from wells (display limited to {tracking_time_days} days)...")
        sim = mp_model.create_mpsim(
            trackdir='backward',
            simtype='pathline',
            packages='WEL',
            start_time=(0, 0, 0.0)
        )

        # Write and run MODPATH
        mp_model.write_input()
        mp_success, mp_buff = mp_model.run_model(silent=True, report=False)

        if mp_success:
            # Load and plot pathline results
            pathline_file = os.path.join(model_ws, f'{mp_name}.mppth')
            pathlines = flopy.utils.PathlineFile(pathline_file)
            pathline_data = pathlines.get_alldata()
            print(f"Loaded pathlines for {len(pathline_data)} particles")

            # Plot with time-filtered pathlines
            plot_solution(ml, head, pathlines=pathline_data, max_time=tracking_time_days)
        else:
            print("MODPATH did not run successfully")
            if mp_buff:
                print('\n'.join(str(x) for x in mp_buff) if isinstance(mp_buff, list) else str(mp_buff))

    except Exception as e:
        print(f"Error in particle tracking: {e}")

    print("\nDone!")

########################################################
# PART 2c Flow Budget Analysis
########################################################

if success:
    print("\n" + "="*60)
    print("FLOW BUDGET ANALYSIS")
    print("="*60)

    # Load list file to extract budget summary
    list_file = os.path.join(model_ws, 'biglake.out')
    mfl = flopy.utils.Mf6ListBudget(list_file) if hasattr(flopy.utils, 'Mf6ListBudget') else None

    # Alternative: Load cell budget file directly
    cbc_file = os.path.join(model_ws, 'biglake.ccf')
    cbc = flopy.utils.CellBudgetFile(cbc_file)

    # Get budget for last time step
    times = cbc.get_times()
    print(f"\nFlow budget at time = {times[-1]} days:")
    print("-" * 60)

    # Get budget records and compute totals
    records = cbc.get_unique_record_names()
    total_in = 0.0
    total_out = 0.0

    # Extract flow rates for each component
    budget_items = []
    for record in records:
        record_name = record.decode().strip()
        # Skip internal flow components
        if 'FLOW' in record_name and 'FACE' in record_name:
            continue

        # Get data and sum flows
        data_list = cbc.get_data(text=record, totim=times[-1])
        flow_rate = 0.0

        for data in data_list:
            if isinstance(data, list):
                # Special case: RECHARGE returns [layer_array, flow_array]
                if len(data) >= 2 and isinstance(data[1], np.ndarray):
                    flow_rate += data[1].sum()
            elif isinstance(data, np.ndarray):
                if data.dtype.names is not None and 'q' in data.dtype.names:
                    # Structured array with 'q' field
                    flow_rate += data['q'].sum()
                else:
                    # Regular array
                    flow_rate += np.sum(data)

        budget_items.append((record_name, flow_rate))

    # Print budget components
    for name, flow in budget_items:
        if flow > 0:
            print(f"  {name:20s}  IN:  {flow:12.2f} m³/d")
            total_in += flow
        elif flow < 0:
            print(f"  {name:20s}  OUT: {flow:12.2f} m³/d")
            total_out += flow

    print("-" * 60)
    print(f"  {'Total IN':20s}       {total_in:12.2f} m³/d")
    print(f"  {'Total OUT':20s}       {total_out:12.2f} m³/d")
    print(f"  {'Net (IN - OUT)':20s}       {total_in + total_out:12.2f} m³/d")
    if total_in > 0:
        print(f"  {'Percent Error':20s}       {100 * (total_in + total_out) / total_in:12.4f} %")


########################################################
# PART 2d Conductance sensitivity analysis
########################################################
if success:
    print("\n" + "="*60)
    print("CONDUCTANCE SENSITIVITY ANALYSIS")
    print("="*60)

    # Sensitivity analysis parameters
    min_cond_factor = 0.1
    max_cond_factor = 10.0
    n_increments = 50

    # Generate conductance multiplier values (log distribution for more detail at low values)
    cond_factors = np.linspace(min_cond_factor, max_cond_factor, n_increments)

    # Store results
    ghb_net_flows = []

    # Get original GHB conductance values
    original_ghb_data = ml.ghb.stress_period_data[0].copy()

    print(f"\nRunning {n_increments} model simulations...")
    print(f"Conductance factor range: {min_cond_factor} to {max_cond_factor}")

    for i, cond_factor in enumerate(cond_factors):
        # Modify GHB conductance
        modified_ghb_data = original_ghb_data.copy()
        modified_ghb_data['cond'] = original_ghb_data['cond'] * cond_factor

        # Update model with modified conductance
        ml.ghb.stress_period_data[0] = modified_ghb_data

        # Write only the GHB file
        ml.ghb.write_file()

        # Fix GHB file formatting (FloPy uses insufficient field width for MODFLOW-2000)
        ghb_file = os.path.join(model_ws, 'biglake.ghb')
        fix_modflow_file_formatting(ghb_file)


        # Delete old output files to ensure fresh results
        cbc_file = os.path.join(model_ws, 'biglake.ccf')
        hed_file = os.path.join(model_ws, 'biglake.hed')
        if os.path.exists(cbc_file):
            os.remove(cbc_file)
        if os.path.exists(hed_file):
            os.remove(hed_file)

        success_run, buff = ml.run_model(silent=True, report=False)

        if success_run:
            # Load cell budget file (fresh each time to avoid caching)
            cbc_file = os.path.join(model_ws, 'biglake.ccf')
            cbc = flopy.utils.CellBudgetFile(cbc_file)
            times = cbc.get_times()

            # Get GHB flow (same method as budget analysis)
            ghb_data_list = cbc.get_data(text='HEAD DEP BOUNDS', totim=times[-1])
            ghb_flow = 0.0
            for data in ghb_data_list:
                if isinstance(data, np.ndarray) and data.dtype.names is not None and 'q' in data.dtype.names:
                    ghb_flow += data['q'].sum()

            ghb_net_flows.append(ghb_flow)
        else:
            ghb_net_flows.append(np.nan)

        # Progress indicator
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/{n_increments} simulations (factor={cond_factor:.3f}, GHB flow={ghb_net_flows[-1]:.2f} m³/d)")

    # Restore original GHB data
    ml.ghb.stress_period_data[0] = original_ghb_data
    ml.write_input()

    print(f"\nCompleted all {n_increments} simulations")

    # Print summary statistics
    ghb_array = np.array(ghb_net_flows)
    print(f"\nGHB Flow Statistics:")
    print(f"  Min: {np.nanmin(ghb_array):.2f} m³/d")
    print(f"  Max: {np.nanmax(ghb_array):.2f} m³/d")
    print(f"  Mean: {np.nanmean(ghb_array):.2f} m³/d")

    # Plot results
    print("\nPlotting sensitivity analysis results...")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(cond_factors, ghb_net_flows, 'b-', linewidth=2, label='GHB Flow')
    ax.axvline(x=1.0, color='r', linestyle='--', linewidth=2, label='Baseline (factor=1.0)')
    ax.set_xlabel('GHB Conductance Multiplier', fontsize=12)
    ax.set_ylabel('Net GHB Flow [m³/d]', fontsize=12)
    ax.set_title('Sensitivity of GHB Flow to Conductance', fontsize=14)
    ax.set_xscale('linear')  # Log scale on x-axis to match the distribution
    ax.grid(True, alpha=0.3, which='both')
    ax.legend(loc='best')
    plt.tight_layout()
    plt.show()

    print("\nDone!")
