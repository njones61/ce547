# This script is a simple example of how to use the flopy package to build a well-stream interaction model.
# Before running this script, you need to install the flopy package. You can do this by running the following command:
# pip install flopy
# To install the MODFLOW executables, you can run the following command:
# get-modflow :flopy
# This will download and install the necessary MODFLOW executables for your system.
# You can then run the script by typing:
# python well_stream.py
# This will build the model and run the simulation.
# The results will be saved in the model_output directory.

# Import necessary libraries
import flopy
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Create a workspace directory
model_ws = './my_model'
os.makedirs(model_ws, exist_ok=True)

########################################################
# PART 1a - Pre-development model
########################################################

# Model parameters
nlay = 1
nrow = 40
ncol = 50
delr = 1000 / ncol  # x-dimension: 1000 ft / 50 cells = 20 ft/cell
delc = 800 / nrow   # y-dimension: 800 ft / 40 cells = 20 ft/cell
top = 200.0
botm = [0.0]

# Boundary conditions
hc_right = 150.0  # Specified head on the right boundary
K = 1.0  # Hydraulic conductivity in ft/day
recharge = 0.01 # Recharge in ft/day

# Time parameters
nper = 1
perlen = [1.0]
nstp = [1]
tsmult = [1.0]
steady = [True]

# Create the MODFLOW model object
ml = flopy.modflow.Modflow(modelname='pre_dev_mf', exe_name='mf2000',
                            version='mf2k', model_ws=model_ws)

# Add DIS package
dis = flopy.modflow.ModflowDis(ml, nlay=nlay, nrow=nrow, ncol=ncol,
                               delr=delr, delc=delc, top=top, botm=botm,
                               nper=nper, perlen=perlen, nstp=nstp,
                               tsmult=tsmult, steady=steady)

# Add BAS package
# ibound: 1 for active cells, 0 for inactive, -1 for specified head
ibound = np.ones((nlay, nrow, ncol), dtype=int)
ibound[:, :, -1] = -1  # Specified head on the rightmost column

# Initial head
strt = 200.0 * np.ones((nlay, nrow, ncol)) # Initial head everywhere

# Set specified head for boundary cells in the strt array
strt[ibound == -1] = hc_right

bas = flopy.modflow.ModflowBas(ml, ibound=ibound, strt=strt)

# Add LPF package (Layer-Property Flow)
lpf = flopy.modflow.ModflowLpf(ml, hk=K, vka=K, sy=0.15, ss=1e-5, laytyp=1)

# Add RCH package (Recharge)
rch = flopy.modflow.ModflowRch(ml, rech=recharge)

# Add PCG package (Preconditioned Conjugate-Gradient Solver)
pcg = flopy.modflow.ModflowPcg(ml, hclose=1e-3, rclose=1e-3, iter1=50, npcond=1)

# Add OC package (Output Control) to save heads
# Create a dictionary for output control options for the last stress period
save_every_time_step = [(0, 0, 0, 0)] # (kstp, kper, text, option)
# save head and drawdown at every time step of the simulation
spd = {(0, 0): ['print head', 'print drawdown', 'save head', 'save drawdown']}
oc = flopy.modflow.ModflowOc(ml, stress_period_data=spd, compact=True)

# Write the MODFLOW input files
ml.write_input()

# Run the MODFLOW model
success, buff = ml.run_model(silent=True, report=True)

if success:
    print("Model ran successfully!")
else:
    print("Model did not run successfully.")
    print(buff)

# Load results if the model ran successfully
if success:
    # Create the headfile object (using .hds extension)
    headobj = flopy.utils.binaryfile.HeadFile(os.path.join(model_ws, 'pre_dev_mf.hds'))
    # Get a list of all available times in the head file
    times = headobj.get_times()
    # Get the head data for the last time step
    head_predev = headobj.get_data(totim=times[-1])

    # Print some head values
    print(f"Head at (0, 0, 0): {head_predev[0, 0, 0]:.2f} ft")
    print(f"Head at (0, 0, {ncol-1}): {head_predev[0, 0, ncol-1]:.2f} ft")


# Plot the results
def plot_results(head, title, save_path=None):
    """
    Plot head distribution with contours.
    
    Parameters:
    -----------
    head : numpy array
        Head array with shape (nlay, nrow, ncol)
    title : str
        Title for the plot
    save_path : str, optional
        If provided, save the figure to this path instead of showing
    """
    import flopy.plot as fp

    # Create a figure with specified size (width, height in inches)
    fig = plt.figure(figsize=(10, 6))

    # Create the plotmapview object
    pmap = fp.PlotMapView(model=ml)

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

    # Add a color bar
    plt.colorbar(im, label='Head (ft)', shrink=0.8)

    # Add title and labels
    plt.title(title)
    plt.xlabel('X-coordinate (ft)')
    plt.ylabel('Y-coordinate (ft)')
    
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

def plot_cross_section(model, head, row, title=None, save_path=None, head_initial=None):
    """
    Plot a cross-section along a designated row showing cell elevations and head.
    
    Parameters:
    -----------
    model : flopy.modflow.Modflow
        The MODFLOW model object
    head : numpy array
        Head array with shape (nlay, nrow, ncol)
    row : int
        Row index (0-based) for the cross-section
    title : str, optional
        Title for the plot
    save_path : str, optional
        If provided, save the figure to this path instead of showing
    head_initial : numpy array, optional
        Initial head array to plot as a reference line (pre-development conditions)
    """
    # Get model discretization information
    dis = model.get_package('DIS')
    nlay = dis.nlay
    ncol = dis.ncol
    delr = dis.delr.array  # Cell width in row direction (x-direction)
    top = dis.top.array
    botm = dis.botm.array
    
    # Calculate x-coordinates (cell centers and edges)
    # Handle both scalar and array delr
    if np.isscalar(delr) or (isinstance(delr, np.ndarray) and delr.size == 1):
        cell_width = float(delr) if np.isscalar(delr) else float(delr[0])
        x_edges = np.arange(0, (ncol + 1) * cell_width, cell_width)
    else:
        # Variable delr
        x_edges = np.zeros(ncol + 1)
        for i in range(ncol):
            x_edges[i + 1] = x_edges[i] + delr[i]
    
    x_centers = x_edges[:-1] + np.diff(x_edges) / 2
    
    # Extract head values for the specified row (layer 0 for single layer)
    head_line = head[0, row, :]  # Shape: (ncol,)
    
    # Get top and bottom elevations
    # Handle scalar or array top
    if np.isscalar(top) or (isinstance(top, np.ndarray) and top.size == 1):
        cell_top = float(top) if np.isscalar(top) else float(top[0])
        top_array = np.full(ncol, cell_top)
    elif top.ndim == 2:
        top_array = top[row, :]
    else:
        top_array = np.full(ncol, float(top[0]))
    
    # Handle bottom elevations
    if botm.ndim == 3:
        botm_array = botm[0, row, :]  # First layer bottom
    elif botm.ndim == 2:
        botm_array = botm[row, :]
    elif botm.ndim == 1:
        botm_array = np.full(ncol, float(botm[0]))
    else:
        botm_array = np.full(ncol, float(botm))
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Plot cell geometry (top and bottom lines for each cell)
    for i in range(ncol):
        x_left = x_edges[i]
        x_right = x_edges[i + 1]
        cell_top = top_array[i]
        cell_botm = botm_array[i]
        
        # Draw cell boundaries (left, right, top, bottom)
        ax.plot([x_left, x_left], [cell_botm, cell_top], 'k-', linewidth=0.5)
        ax.plot([x_right, x_right], [cell_botm, cell_top], 'k-', linewidth=0.5)
        ax.plot([x_left, x_right], [cell_top, cell_top], 'k-', linewidth=0.5)
        ax.plot([x_left, x_right], [cell_botm, cell_botm], 'k-', linewidth=0.5)
    
    # Plot head line (blue)
    ax.plot(x_centers, head_line, 'b-', linewidth=2, label='Simulated Head')
    
    # Fill between water table and base elevation (0 ft) with light blue
    ax.fill_between(x_centers, 0, head_line, color='lightblue', alpha=0.5)
    
    # Plot initial water table (reference line) if provided
    if head_initial is not None:
        head_initial_line = head_initial[0, row, :]  # Extract initial head for the row
        ax.plot(x_centers, head_initial_line, 'r--', linewidth=1.5, 
                label='Initial Water Table (Pre-Development)', alpha=0.7)
    
    # Formatting
    ax.set_xlabel('Distance (ft)')
    ax.set_ylabel('Elevation (ft)')
    ax.set_title(title if title else f'Cross-Section at Row {row}')
    ax.grid(True, alpha=0.3)
    # solid white fill on the legend background
    ax.legend(loc='lower center', facecolor='white', framealpha=1.0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

plot_results(head_predev, 'Pre-Development Conditions (Steady State)')

plot_cross_section(ml, head_predev, 20, 'Pre-Development Conditions (Steady State) - Row 20')


########################################################
# PART 1b - Well-stream interaction model (steady state)
########################################################

# Create a new model for Part 1b to avoid overwriting Part 1a files
ml_well = flopy.modflow.Modflow(modelname='well_mf', exe_name='mf2000',
                                 version='mf2k', model_ws=model_ws)

# Add DIS package (same as Part 1a)
dis_well = flopy.modflow.ModflowDis(ml_well, nlay=nlay, nrow=nrow, ncol=ncol,
                                    delr=delr, delc=delc, top=top, botm=botm,
                                    nper=nper, perlen=perlen, nstp=nstp,
                                    tsmult=tsmult, steady=steady)

# Add BAS package (same as Part 1a)
bas_well = flopy.modflow.ModflowBas(ml_well, ibound=ibound, strt=strt)

# Add LPF package (same as Part 1a)
lpf_well = flopy.modflow.ModflowLpf(ml_well, hk=K, vka=K, sy=0.15, ss=1e-5, laytyp=1)

# Add RCH package (same as Part 1a)
rch_well = flopy.modflow.ModflowRch(ml_well, rech=recharge)

# Add WEL package (Well) 
# Well Q = -8000 ft³/day (negative = extraction/pumping)
# Location: layer 0 (layer 1 in 1-indexed), row 20 (row 21 in 1-indexed), col 41 (col 42 in 1-indexed)
well_data = {0: [(0, 20, 41, -8000.0)]}  # {stress_period: [(layer, row, col, flux), ...]}
wel = flopy.modflow.ModflowWel(ml_well, stress_period_data=well_data)

# Add PCG package (same as Part 1a)
pcg_well = flopy.modflow.ModflowPcg(ml_well, hclose=1e-3, rclose=1e-3, iter1=50, npcond=1)

# Add OC package (same as Part 1a)
oc_well = flopy.modflow.ModflowOc(ml_well, stress_period_data=spd, compact=True)

# Write the MODFLOW input files
ml_well.write_input()

# Run the MODFLOW model
success_well, buff_well = ml_well.run_model(silent=True, report=True)

if success_well:
    print("Model with well ran successfully!")
else:
    print("Model with well did not run successfully.")
    print(buff_well)

# Load results if the model ran successfully
if success_well:
    # Create the headfile object - use the well model name
    headobj_well = flopy.utils.binaryfile.HeadFile(os.path.join(model_ws, 'well_mf.hds'))
    # Get a list of all available times in the head file
    times_well = headobj_well.get_times()
    # Get the head data for the last time step
    head_well = headobj_well.get_data(totim=times_well[-1])
    
    # Print some head values
    print(f"Head at (0, 0, 0): {head_well[0, 0, 0]:.2f} ft")
    print(f"Head at well location (0, 20, 41): {head_well[0, 20, 41]:.2f} ft")
    print(f"Head at (0, 0, {ncol-1}): {head_well[0, 0, ncol-1]:.2f} ft")
    
    # Plot the results
    plot_results(head_well, 'Well-Stream Interaction Model (Steady State)')
    
    # Plot cross-section at row 20
    plot_cross_section(ml_well, head_well, 20, 'Well-Stream Interaction Model - Row 20', head_initial=head_predev)


def storage_loss(head1, head2, sy):
    """
    Calculate the total volume of water removed from storage between two head solutions.
    
    Parameters:
    -----------
    head1 : numpy array
        First head solution (e.g., pre-development) with shape (nlay, nrow, ncol)
    head2 : numpy array
        Second head solution (e.g., post-development) with shape (nlay, nrow, ncol)
    sy : float
        Specific yield (dimensionless)
    
    Returns:
    --------
    total_storage_loss : float
        Total volume of water removed from storage (ft³)
    """
    # Get cell dimensions from module-level variables (delr and delc)
    # These are defined earlier in the script
    global delr, delc
    
    # Handle scalar or array delr and delc
    if np.isscalar(delr) or (isinstance(delr, np.ndarray) and delr.size == 1):
        cell_width = float(delr) if np.isscalar(delr) else float(delr[0])
    else:
        # Variable delr - will need to handle per column
        cell_width = None
    
    if np.isscalar(delc) or (isinstance(delc, np.ndarray) and delc.size == 1):
        cell_height = float(delc) if np.isscalar(delc) else float(delc[0])
    else:
        # Variable delc - will need to handle per row
        cell_height = None
    
    # Calculate head difference (head1 - head2)
    # Positive values indicate water removed from storage
    head_diff = head1 - head2
    
    # Calculate storage loss for each cell
    # Volume = area * head_difference * specific_yield
    if cell_width is not None and cell_height is not None:
        # Uniform cell size
        cell_area = cell_width * cell_height
        storage_loss_per_cell = cell_area * head_diff * sy
    else:
        # Variable cell sizes - calculate per cell
        nlay, nrow, ncol = head1.shape
        storage_loss_per_cell = np.zeros_like(head1)
        
        for lay in range(nlay):
            for row in range(nrow):
                for col in range(ncol):
                    # Get cell dimensions
                    if isinstance(delr, np.ndarray) and len(delr) > 1:
                        cell_w = delr[col]
                    else:
                        cell_w = float(delr) if np.isscalar(delr) else float(delr[0])
                    
                    if isinstance(delc, np.ndarray) and len(delc) > 1:
                        cell_h = delc[row]
                    else:
                        cell_h = float(delc) if np.isscalar(delc) else float(delc[0])
                    
                    cell_area = cell_w * cell_h
                    storage_loss_per_cell[lay, row, col] = cell_area * head_diff[lay, row, col] * sy
    
    # Sum over all cells to get total storage loss
    total_storage_loss = np.sum(storage_loss_per_cell)
    
    return total_storage_loss

# Calculate the amount of water removed from storage in the aquifer due to the well pumping.
# This is the difference in head between the pre-development and post-development conditions. 
# The volume of water removed from storage is the product of the area of the cell, the difference in head, and the specific yield.
# The specific yield is 0.15.
# This needs to be done for each cell in the model.

total_storage_loss = storage_loss(head_predev, head_well, 0.15)
print(f"Total storage loss: {total_storage_loss:,.2f} ft³")

########################################################
# PART 1c - Well-stream interaction model (transient)
########################################################

# Convert model to transient
# Total simulation time: 2000 days
# Single stress period with 200 time steps (10 days per time step)
nper_transient = 1
num_days_transient = 2000
num_time_steps = 200
perlen_transient = [num_days_transient]
nstp_transient = [num_time_steps]
tsmult_transient = [1.0]
steady_transient = [False]

# Create a new model for transient simulation to avoid overwriting previous results
ml_transient = flopy.modflow.Modflow(modelname='transient_mf', exe_name='mf2000',
                                      version='mf2k', model_ws=model_ws)

# Add DIS package for transient simulation
dis_transient = flopy.modflow.ModflowDis(ml_transient, nlay=nlay, nrow=nrow, ncol=ncol,
                                         delr=delr, delc=delc, top=top, botm=botm,
                                         nper=nper_transient, perlen=perlen_transient,
                                         nstp=nstp_transient, tsmult=tsmult_transient,
                                         steady=steady_transient)

# Add BAS package - use pre-development head as initial condition
# Starting from pre-development allows us to see the transient response to well pumping
strt_transient = head_predev.copy()  # Start from pre-development conditions
bas_transient = flopy.modflow.ModflowBas(ml_transient, ibound=ibound, strt=strt_transient)

# Add LPF package (same as before, sy=0.15 for transient)
# Set ipakcb=53 to write budget data to unit 53
lpf_transient = flopy.modflow.ModflowLpf(ml_transient, hk=K, vka=K, sy=0.15, ss=1e-5, laytyp=1, ipakcb=53)

# Add RCH package (same recharge, with ipakcb=53)
rch_transient = flopy.modflow.ModflowRch(ml_transient, rech=recharge, ipakcb=53)

# Add WEL package (same well, with ipakcb=53)
well_data_transient = {0: [(0, 20, 41, -8000.0)]}
wel_transient = flopy.modflow.ModflowWel(ml_transient, stress_period_data=well_data_transient, ipakcb=53)

# Add PCG package (same solver settings)
pcg_transient = flopy.modflow.ModflowPcg(ml_transient, hclose=1e-3, rclose=1e-3, iter1=50, npcond=1)

# Add OC package to save heads and budget every nth time step
output_interval = 2
spd_transient = {(0, i): ['save head', 'save budget'] for i in range(0, num_time_steps+1, output_interval)}  # Save head and budget
oc_transient = flopy.modflow.ModflowOc(ml_transient, stress_period_data=spd_transient, compact=True)

# Write the MODFLOW input files first
ml_transient.write_input()

# Add BUDGET SAVE UNIT to OC file (MODFLOW 2000 needs this to write budget file)
oc_file = os.path.join(model_ws, 'transient_mf.oc')
if os.path.exists(oc_file):
    with open(oc_file, 'r') as f:
        oc_lines = f.readlines()
    
    # Check if BUDGET SAVE UNIT already exists
    has_budget_unit = any('BUDGET SAVE UNIT' in line for line in oc_lines)
    
    if not has_budget_unit:
        # Find the line with "DRAWDOWN SAVE UNIT" and add "BUDGET SAVE UNIT" after it
        # This follows the pattern: HEAD SAVE UNIT, DRAWDOWN SAVE UNIT, BUDGET SAVE UNIT
        for i, line in enumerate(oc_lines):
            if 'DRAWDOWN SAVE UNIT' in line:
                # Insert BUDGET SAVE UNIT line after DRAWDOWN SAVE UNIT
                budget_unit_line = 'BUDGET SAVE UNIT    53\n'
                oc_lines.insert(i + 1, budget_unit_line)
                break
        
        # Write back to file
        with open(oc_file, 'w') as f:
            f.writelines(oc_lines)
        print("Added BUDGET SAVE UNIT to OC file.")

# Add budget file to name file (MODFLOW 2000 requires budget file in name file)
nam_file = os.path.join(model_ws, 'transient_mf.nam')
if os.path.exists(nam_file):
    with open(nam_file, 'r') as f:
        nam_lines = f.readlines()
    
    # Check if budget file entry already exists
    has_budget = any('DATA(BINARY)' in line and ('53' in line or 'cbc' in line.lower()) for line in nam_lines)
    
    if not has_budget:
        # Add budget file entry (unit 53 is standard for budget files)
        budget_line = 'DATA(BINARY)      53  transient_mf.cbc REPLACE\n'
        # Find where to insert (after OC line, before DATA lines)
        insert_pos = len(nam_lines)
        for i, line in enumerate(nam_lines):
            if 'OC' in line and 'transient_mf.oc' in line:
                insert_pos = i + 1
                break
        
        nam_lines.insert(insert_pos, budget_line)
        
        # Write back to file
        with open(nam_file, 'w') as f:
            f.writelines(nam_lines)
        print("Added budget file entry to name file.")

# Delete any existing empty budget file and create a new empty one
# MODFLOW needs the file to exist before it can write to it
cbc_file_path = os.path.join(model_ws, 'transient_mf.cbc')
if os.path.exists(cbc_file_path):
    if os.path.getsize(cbc_file_path) == 0:
        os.remove(cbc_file_path)
        print("Deleted empty budget file.")
    else:
        # If budget file exists and has data, keep it
        pass

# Create an empty budget file so MODFLOW can write to it
# This ensures the file exists when MODFLOW tries to open it
if not os.path.exists(cbc_file_path):
    with open(cbc_file_path, 'wb') as f:
        pass  # Create empty binary file
    print("Created empty budget file for MODFLOW to write to.")

# Run the transient MODFLOW model
success_transient, buff_transient = ml_transient.run_model(silent=True, report=True)

# Check if budget file was created and has data
cbc_check = os.path.join(model_ws, 'transient_mf.cbc')
budget_file_empty = False
if os.path.exists(cbc_check):
    if os.path.getsize(cbc_check) == 0:
        budget_file_empty = True
        print("\nWarning: Budget file is empty. Re-running model with budget file in name file...")
        # Delete empty file
        os.remove(cbc_check)
        # Re-run the model
        success_transient, buff_transient = ml_transient.run_model(silent=True, report=True)

if success_transient:
    print("Transient model ran successfully!")
else:
    print("Transient model did not run successfully.")
    print(buff_transient)

# Load results if the model ran successfully
if success_transient:
    # Create the headfile object - use the transient model name
    headobj_transient = flopy.utils.binaryfile.HeadFile(os.path.join(model_ws, 'transient_mf.hds'))
    # Get a list of all available times in the head file
    times_transient = headobj_transient.get_times()
    
    # Debug: Print information about available time steps
    print(f"\nNumber of time steps in head file: {len(times_transient)}")
    print(f"First time: {times_transient[0]:.2f} days")
    print(f"Last time: {times_transient[-1]:.2f} days")
    if len(times_transient) > 10:
        print(f"Sample times: {[f'{t:.1f}' for t in times_transient[0:5]]} ... {[f'{t:.1f}' for t in times_transient[-5:]]}")
    
    # Compare head values at different time steps to check if they're changing
    if len(times_transient) > 1:
        head_first = headobj_transient.get_data(totim=times_transient[0])
        head_last = headobj_transient.get_data(totim=times_transient[-1])
        print(f"\nHead at (0, 0, 0) - First time step: {head_first[0, 0, 0]:.2f} ft")
        print(f"Head at (0, 0, 0) - Last time step: {head_last[0, 0, 0]:.2f} ft")
        print(f"Head at well (0, 20, 41) - First time step: {head_first[0, 20, 41]:.2f} ft")
        print(f"Head at well (0, 20, 41) - Last time step: {head_last[0, 20, 41]:.2f} ft")
        print(f"Difference: {head_last[0, 20, 41] - head_first[0, 20, 41]:.4f} ft")

    # Get the head data for a specific time step
    time_step = 1
    if time_step >= len(times_transient):
        time_step = len(times_transient) - 1
        print(f"\nWarning: Requested time step index too large, using last time step")
    
    head_transient_time = headobj_transient.get_data(totim=times_transient[time_step])
    
    # Print some head values
    print(f"\nHead at (0, 0, 0) at time step {time_step} (Day {int(times_transient[time_step])}): {head_transient_time[0, 0, 0]:.2f} ft")
    print(f"Head at well location (0, 20, 41) at time step {time_step} (Day {int(times_transient[time_step])}): {head_transient_time[0, 20, 41]:.2f} ft")
    print(f"Total simulation time: {times_transient[-1]:.2f} days")
    
    # Plot the results with contours at the selected time step 
    # Need to use ml_transient for the plot

    title = f'Well-Stream Interaction Model (Transient) - Day {int(times_transient[time_step])}'
    plot_results(head_transient_time, title)

    plot_cross_section(ml_transient, head_transient_time, 20, title, head_initial=head_predev)


########################################################
# Animation Functions
########################################################

def animate_head_map(headobj, model, output_gif='head_animation.gif', fps=5):
    """
    Create an animated GIF showing the evolution of head over time.
    
    Parameters:
    -----------
    headobj : flopy.utils.binaryfile.HeadFile
        Head file object from the transient simulation
    output_gif : str
        Output filename for the GIF
    fps : int
        Frames per second for the animation
    """
    try:
        import imageio.v2 as imageio
    except ImportError:
        print("Error: imageio is required for creating GIFs. Install with: pip install imageio")
        return
    
    # Get all available times
    times = headobj.get_times()
    
    # First, find the global min and max head values across all time steps
    print("Calculating global head range across all time steps...")
    head_min_global = np.inf
    head_max_global = -np.inf
    for time in times:
        head = headobj.get_data(totim=time)
        head_min_global = min(head_min_global, head.min())
        head_max_global = max(head_max_global, head.max())
    
    print(f"Global head range: {head_min_global:.2f} to {head_max_global:.2f} ft")
    
    # Set up contour levels based on global range
    interval = 2.0
    levels_global = np.arange(np.floor(head_min_global), np.ceil(head_max_global) + interval, interval)
    
    # Create temporary directory for frames
    temp_dir = os.path.join(model_ws, 'animation_frames')
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Generating {len(times)} frames for animation...")
    
    # Generate frames
    frame_files = []
    for i, time in enumerate(times):
        head = headobj.get_data(totim=time)
        frame_path = os.path.join(temp_dir, f'frame_{i:04d}.png')
        # Use plot_results but need to create plot with correct model
        import flopy.plot as fp
        fig = plt.figure(figsize=(10, 6))
        pmap = fp.PlotMapView(model=model)
        # Use global min/max for consistent color scaling across all frames
        im = pmap.plot_array(head, cmap='viridis', vmin=head_min_global, vmax=head_max_global)
        pmap.plot_inactive()
        pmap.plot_ibound()
        pmap.plot_grid(lw=0.5, color="0.5")
        # Use global contour levels for consistency
        cs = pmap.contour_array(head, levels=levels_global, colors='black', linewidths=1.5)
        plt.clabel(cs, fmt='%1.1f')
        plt.colorbar(im, label='Head (ft)', shrink=0.8)
        plt.title(f'Well-Stream Interaction Model (Transient) - Day {int(time)}')
        plt.xlabel('X-coordinate (ft)')
        plt.ylabel('Y-coordinate (ft)')
        plt.savefig(frame_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
        frame_files.append(frame_path)
        
        if (i + 1) % 20 == 0:
            print(f"  Generated {i + 1}/{len(times)} frames...")
    
    print(f"Creating animated GIF: {output_gif}")
    
    # Create GIF from frames
    images = []
    for frame_file in frame_files:
        images.append(imageio.imread(frame_file))
    
    # Convert fps to duration in milliseconds (duration = 1000 / fps)
    duration = 1000 / fps
    imageio.mimsave(output_gif, images, duration=duration, loop=0)
    
    # Clean up temporary frames
    for frame_file in frame_files:
        try:
            os.remove(frame_file)
        except:
            pass
    try:
        os.rmdir(temp_dir)
    except:
        pass
    
    print(f"Animation saved to: {output_gif}")

def animate_cross_section(model, headobj, row, output_gif='cross_section_animation.gif', fps=5, head_initial=None):
    """
    Create an animated GIF showing the evolution of head in a cross-section over time.
    
    Parameters:
    -----------
    model : flopy.modflow.Modflow
        The MODFLOW model object
    headobj : flopy.utils.binaryfile.HeadFile
        Head file object from the transient simulation
    row : int
        Row index (0-based) for the cross-section
    output_gif : str
        Output filename for the GIF
    fps : int
        Frames per second for the animation
    head_initial : numpy array, optional
        Initial head array (pre-development conditions) to plot as reference line
    """
    try:
        import imageio.v2 as imageio
    except ImportError:
        print("Error: imageio is required for creating GIFs. Install with: pip install imageio")
        return
    
    # Get all available times
    times = headobj.get_times()
    
    # Create temporary directory for frames
    temp_dir = os.path.join(model_ws, 'animation_frames')
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Generating {len(times)} cross-section frames for animation...")
    
    # Generate frames
    frame_files = []
    for i, time in enumerate(times):
        head = headobj.get_data(totim=time)
        frame_path = os.path.join(temp_dir, f'cross_section_frame_{i:04d}.png')
        plot_cross_section(model, head, row, 
                          title=f'Cross-Section at Row {row} - Day {int(time)}',
                          save_path=frame_path, head_initial=head_initial)
        frame_files.append(frame_path)
        
        if (i + 1) % 20 == 0:
            print(f"  Generated {i + 1}/{len(times)} frames...")
    
    print(f"Creating animated GIF: {output_gif}")
    
    # Create GIF from frames
    images = []
    for frame_file in frame_files:
        images.append(imageio.imread(frame_file))
    
    # Convert fps to duration in milliseconds (duration = 1000 / fps)
    duration = 1000 / fps
    imageio.mimsave(output_gif, images, duration=duration, loop=0)
    
    # Clean up temporary frames
    for frame_file in frame_files:
        try:
            os.remove(frame_file)
        except:
            pass
    try:
        os.rmdir(temp_dir)
    except:
        pass
    
    print(f"Animation saved to: {output_gif}")



########################################################
# Flow Budget Analysis
########################################################

if success_transient:
    # Read budget data from the CBC file
    cbc_file = os.path.join(model_ws, 'transient_mf.cbc')
    
    if os.path.exists(cbc_file) and os.path.getsize(cbc_file) > 0:
        print(f"\nReading budget data from CBC file: {cbc_file}")
        
        try:
            import flopy.utils.binaryfile as bf
            cbc = bf.CellBudgetFile(cbc_file)
            
            # Get available budget record types
            available_records = cbc.get_unique_record_names()
            print(f"Available budget record types: {available_records}")
            
            # Get all times from the budget file
            times_budget = cbc.get_times()
            print(f"Found {len(times_budget)} time steps in budget file")
            
            # Time step size (10 days per step)
            dt = 10.0  # days
            
            # Initialize arrays to store values
            storage_change_rate = []  # Storage change rate (ft³/day, positive = water released)
            stream_discharge = []  # Flow to/from specified head cells (ft³/day, positive = flow into aquifer)
            
            # Extract storage and constant head flow for each time step
            for i, time in enumerate(times_budget):
                # Get storage term (STORAGE)
                # In MODFLOW CBC files with COMPACT BUDGET, storage values are already rates (ft³/day)
                # Negative values mean water is being removed from storage
                try:
                    storage = cbc.get_data(text='STORAGE', totim=time)[0]
                    # Handle structured array (if it has 'q' field) or regular array
                    if isinstance(storage, np.ndarray) and storage.dtype.names is not None:
                        # Structured array - extract 'q' field (flow values)
                        storage_values = storage['q']
                    else:
                        # Regular array
                        storage_values = storage
                    
                    # Sum over all cells to get total storage change rate (ft³/day)
                    # Negative values mean water is being removed from storage
                    total_storage_rate = np.sum(storage_values)
                    # Convert to positive = water released from storage
                    # Values are already rates, not volumes
                    storage_change_rate.append(-total_storage_rate)
                    if i < 3:  # Debug: print first few values
                        print(f"  Time {time:.1f} days: Storage rate = {total_storage_rate:.2f} ft³/day")
                except Exception as e:
                    print(f"  Error getting STORAGE at time {time}: {e}")
                    storage_change_rate.append(0.0)
                
                # Get constant head flow
                # Use the exact record name from available_records: '   CONSTANT HEAD'
                chd_flow = None
                chd_text_name = None
                for text_name in ['   CONSTANT HEAD', 'CONSTANT HEAD', 'CHD', 'HEAD DEP BOUNDS', 'HEAD DEP BOUND']:
                    try:
                        chd_data = cbc.get_data(text=text_name, totim=time)[0]
                        chd_text_name = text_name
                        # Handle structured array (if it has 'q' field) or regular array
                        if isinstance(chd_data, np.ndarray) and chd_data.dtype.names is not None:
                            # Structured array - extract 'q' field (flow values)
                            chd_flow = chd_data['q']
                        else:
                            # Regular array
                            chd_flow = chd_data
                        break
                    except:
                        continue
                
                if chd_flow is not None:
                    # Sum only positive values (FLOW IN) - flow into aquifer from constant head cells
                    # Negative values are FLOW OUT (flow out of aquifer)
                    chd_flow_in = chd_flow[chd_flow > 0]  # Filter to only positive values
                    total_chd_in = np.sum(chd_flow_in) if len(chd_flow_in) > 0 else 0.0
                    stream_discharge.append(total_chd_in)
                    if i < 3:  # Debug: print first few values
                        total_chd_out = np.sum(chd_flow[chd_flow < 0]) if len(chd_flow[chd_flow < 0]) > 0 else 0.0
                        print(f"  Time {time:.1f} days: Constant head FLOW IN = {total_chd_in:.2f} ft³/day, FLOW OUT = {total_chd_out:.2f} ft³/day")
                else:
                    stream_discharge.append(0.0)
                    if i < 3:  # Debug
                        print(f"  Time {time:.1f} days: No constant head data found")
            
            # Convert to numpy arrays
            times_budget = np.array(times_budget)
            storage_change_rate = np.array(storage_change_rate)
            stream_discharge = np.array(stream_discharge)
            
            # In MODFLOW CBC files with COMPACT BUDGET, storage values are already rates (ft³/day)
            # No conversion needed - use values directly as rates
            
            # Calculate cumulative storage change (total volume removed from storage)
            # Need to convert rates to volumes by multiplying by time intervals, then sum
            if len(times_budget) > 1:
                # First interval is from 0 to first time (so it's just the first time value)
                # Subsequent intervals are differences between consecutive times
                time_intervals = np.concatenate([[times_budget[0]], np.diff(times_budget)])
            else:
                time_intervals = np.array([times_budget[0]])
            
            # Volume change per time step = rate * time interval
            storage_volume_change = storage_change_rate * time_intervals
            
            # Cumulative storage change (total volume removed from storage)
            cumulative_storage = np.cumsum(storage_volume_change)
            
            print(f"\nStorage calculation details:")
            print(f"  Times in CBC file (end of time steps): {times_budget[:5] if len(times_budget) >= 5 else times_budget}")
            print(f"  Time intervals: {time_intervals[:5] if len(time_intervals) >= 5 else time_intervals}")
            print(f"  First time: {times_budget[0]:.1f} days, interval: {time_intervals[0]:.1f} days")
            print(f"  First storage rate: {storage_change_rate[0]:.2f} ft³/day")
            print(f"  First volume change: {storage_volume_change[0]:.2f} ft³")
            print(f"  Second time: {times_budget[1]:.1f} days, interval: {time_intervals[1]:.1f} days" if len(times_budget) > 1 else "")
            print(f"  Second storage rate: {storage_change_rate[1]:.2f} ft³/day" if len(storage_change_rate) > 1 else "")
            print(f"  Second volume change: {storage_volume_change[1]:.2f} ft³" if len(storage_volume_change) > 1 else "")
            print(f"  Last time: {times_budget[-1]:.1f} days, interval: {time_intervals[-1]:.1f} days")
            print(f"  Final storage rate: {storage_change_rate[-1]:.2f} ft³/day")
            print(f"  Final volume change: {storage_volume_change[-1]:.2f} ft³")
            print(f"  Final cumulative storage: {cumulative_storage[-1]:,.2f} ft³")
            print(f"  Number of time steps: {len(times_budget)}")
            print(f"  Note: Storage values from CBC are already rates (ft³/day)")
            
            # Create the plot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
            
            # Plot 1: Rate of storage change vs time
            ax1.plot(times_budget, storage_change_rate, 'b-', linewidth=2, label='Storage Change Rate')
            ax1.set_ylabel('Storage Change Rate (ft³/day)', fontsize=12)
            ax1.set_title('Aquifer Storage Change vs Time', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            ax1.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
            
            # Plot 2: Stream discharge (specified head cells) vs time
            ax2.plot(times_budget, stream_discharge, 'g-', linewidth=2, label='Stream Discharge')
            ax2.set_xlabel('Time (days)', fontsize=12)
            ax2.set_ylabel('Stream Discharge (ft³/day)', fontsize=12)
            ax2.set_title('Stream Discharge (Qin from Constant Head Cells) vs Time', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
            
            plt.tight_layout()
            plt.show()
            
            # Print summary statistics
            print(f"\nFlow Budget Analysis Summary:")
            print(f"Total simulation time: {times_budget[-1]:.2f} days")
            print(f"Average storage change rate: {np.mean(storage_change_rate):,.2f} ft³/day")
            print(f"Final storage change rate: {storage_change_rate[-1]:,.2f} ft³/day")
            print(f"Total cumulative storage change: {cumulative_storage[-1]:,.2f} ft³")
            print(f"Average stream discharge: {np.mean(stream_discharge):,.2f} ft³/day")
            print(f"Final stream discharge: {stream_discharge[-1]:,.2f} ft³/day")
            
        except Exception as e:
            print(f"\nError reading budget file: {e}")
            print("The budget file may be corrupted or in an unexpected format.")
            import traceback
            traceback.print_exc()
    else:
        print(f"\nBudget file not found or is empty: {cbc_file}")
else:
    print("\nCannot perform flow budget analysis - transient model did not run successfully.")


########################################################
# Create animations
########################################################

# Create animations if transient model ran successfully
if success_transient:
    print("\nCreating head map animation...")
    animate_head_map(headobj_transient, ml_transient, output_gif='head_evolution.gif', fps=5)

    print("\nCreating cross-section animation...")
    animate_cross_section(ml_transient, headobj_transient, 20, output_gif='cross_section_evolution.gif', fps=5, head_initial=head_predev)
