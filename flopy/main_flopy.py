import flopy
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

def load_modflow_model(model_path):
    """
    Load an existing MODFLOW model from the specified path.
    
    Parameters:
    -----------
    model_path : str
        Path to the directory containing MODFLOW files
        
    Returns:
    --------
    mf : flopy.modflow.mf.Modflow
        Loaded MODFLOW model object
    """
    print(f"Loading MODFLOW model from: {model_path}")
    
    # Change to the model directory
    os.chdir(model_path)
    
    # Try to load the model using FloPy's load functionality
    try:
        # For MODFLOW-2000 models, we need to specify the model name
        model_name = "bbottoms"
        
        # Load the model
        mf = flopy.modflow.mf.Modflow.load(
            f"{model_name}.nam",
            model_ws=model_path,
            version="mf2k",
            verbose=True
        )
        print("Model loaded successfully!")
        return mf
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Attempting to create model from scratch...")
        
        # If loading fails, create the model structure manually
        return create_model_from_files(model_path, model_name)

def create_model_from_files(model_path, model_name):
    """
    Create a MODFLOW model object by reading individual files.
    
    Parameters:
    -----------
    model_path : str
        Path to the directory containing MODFLOW files
    model_name : str
        Name of the model
        
    Returns:
    --------
    mf : flopy.modflow.mf.Modflow
        Created MODFLOW model object
    """
    print("Creating model from individual files...")
    
    # Create the model
    mf = flopy.modflow.mf.Modflow(model_name, model_ws=model_path, version="mf2k")
    
    # Read discretization file
    dis_file = os.path.join(model_path, f"{model_name}.dis")
    if os.path.exists(dis_file):
        print("Reading discretization file...")
        # Parse the DIS file manually
        with open(dis_file, 'r') as f:
            lines = f.readlines()
        
        # Extract model dimensions from line 5
        dim_line = lines[4].strip().split()
        nlay, nrow, ncol, nper = int(dim_line[0]), int(dim_line[1]), int(dim_line[2]), int(dim_line[3])
        
        print(f"Model dimensions: {nlay} layers, {nrow} rows, {ncol} columns, {nper} stress periods")
        
        # Create discretization package
        flopy.modflow.mfdis.ModflowDis(
            mf, nlay=nlay, nrow=nrow, ncol=ncol, nper=nper,
            delr=66.7, delc=66.7,  # Approximate cell dimensions
            top=68.9, botm=66.7,  # Approximate elevations
            perlen=[1.0], nstp=[1], tsmult=[1.0], steady=[True]
        )
    
    # Read LPF file for hydraulic properties
    lpf_file = os.path.join(model_path, f"{model_name}.lpf")
    if os.path.exists(lpf_file):
        print("Reading LPF file...")
        # Create LPF package with default values
        flopy.modflow.mflpf.ModflowLpf(
            mf, hk=1e-4, hani=1.0, vka=1e-4, ss=1e-5, sy=0.1
        )
    
    # Read other packages if they exist
    packages = ['rch', 'riv', 'wel', 'drn', 'oc']
    for pkg in packages:
        pkg_file = os.path.join(model_path, f"{model_name}.{pkg}")
        if os.path.exists(pkg_file):
            print(f"Found {pkg.upper()} package file")
            # Add basic package structure (simplified)
            if pkg == 'rch':
                flopy.modflow.mfrch.ModflowRch(mf, rech=1e-6)
            elif pkg == 'riv':
                flopy.modflow.mfriv.ModflowRiv(mf)
            elif pkg == 'wel':
                flopy.modflow.mfwel.ModflowWel(mf)
            elif pkg == 'drn':
                flopy.modflow.mfdrn.ModflowDrn(mf)
            elif pkg == 'oc':
                flopy.modflow.mfoc.ModflowOc(mf)
    
    return mf

def run_modflow_simulation(mf, model_path):
    """
    Run the MODFLOW simulation.
    
    Parameters:
    -----------
    mf : flopy.modflow.mf.Modflow
        MODFLOW model object
    model_path : str
        Path to the model directory
        
    Returns:
    --------
    success : bool
        True if simulation runs successfully
    """
    print("Running MODFLOW simulation...")
    
    try:
        # Write input files
        mf.write_input()
        
        # Run the model
        success, buff = mf.run_model(silent=False, report=True)
        
        if success:
            print("MODFLOW simulation completed successfully!")
        else:
            print("MODFLOW simulation failed!")
            
        return success
        
    except Exception as e:
        print(f"Error running simulation: {e}")
        return False

def load_simulation_results(model_path, model_name):
    """
    Load simulation results from output files.
    
    Parameters:
    -----------
    model_path : str
        Path to the model directory
    model_name : str
        Name of the model
        
    Returns:
    --------
    results : dict
        Dictionary containing loaded results
    """
    print("Loading simulation results...")
    
    results = {}
    
    # Try to load head file
    head_file = os.path.join(model_path, f"{model_name}.hed")
    if os.path.exists(head_file):
        try:
            # Load head file using FloPy
            headobj = flopy.utils.HeadFile(head_file)
            results['head'] = headobj.get_data()
            
            # Handle MODFLOW no-data values (-999.0)
            # Replace -999.0 with NaN for proper plotting
            head_data = results['head'].copy()
            head_data[head_data == -999.0] = np.nan
            results['head_clean'] = head_data
            
            print(f"Loaded head data: {results['head'].shape}")
            print(f"Original head range: {np.nanmin(results['head']):.3f} to {np.nanmax(results['head']):.3f}")
            print(f"Cleaned head range: {np.nanmin(results['head_clean']):.3f} to {np.nanmax(results['head_clean']):.3f}")
            print(f"Number of no-data cells: {(results['head'] == -999.0).sum()}")
            
        except Exception as e:
            print(f"Error loading head file: {e}")
    
    # Try to load budget file
    budget_file = os.path.join(model_path, f"{model_name}.ccf")
    if os.path.exists(budget_file):
        try:
            # Load budget file using FloPy
            budgetobj = flopy.utils.CellBudgetFile(budget_file)
            results['budget'] = budgetobj
            print("Loaded budget file")
        except Exception as e:
            print(f"Error loading budget file: {e}")
    
    # Try to load HDF5 file for arrays
    h5_file = os.path.join(model_path, f"{model_name}.h5")
    if os.path.exists(h5_file):
        try:
            import h5py
            with h5py.File(h5_file, 'r') as f:
                print("HDF5 file contents:")
                for key in f.keys():
                    print(f"  {key}")
                    if isinstance(f[key], h5py.Dataset):
                        print(f"    Shape: {f[key].shape}, Type: {f[key].dtype}")
        except ImportError:
            print("h5py not available for HDF5 file reading")
        except Exception as e:
            print(f"Error reading HDF5 file: {e}")
    
    return results

def visualize_results(results, model_path, model_name):
    """
    Create visualizations of the simulation results.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing simulation results
    model_path : str
        Path to the model directory
    model_name : str
        Name of the model
    """
    print("Creating visualizations...")
    
    # Set up the plotting
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'MODFLOW Simulation Results: {model_name}', fontsize=16)
    
    # Plot 1: Head distribution using cleaned data
    if 'head_clean' in results:
        ax1 = axes[0, 0]
        head_data = results['head_clean'][0, :, :]  # First layer, all rows, all columns
        
        # Use masked array to handle NaN values properly
        masked_data = np.ma.masked_invalid(head_data)
        
        im1 = ax1.imshow(masked_data, cmap='viridis', aspect='auto', interpolation='nearest')
        ax1.set_title('Head Distribution (Layer 1)')
        ax1.set_xlabel('Column')
        ax1.set_ylabel('Row')
        plt.colorbar(im1, ax=ax1, label='Head (m)')
        
        # Add some statistics to the plot
        valid_data = head_data[~np.isnan(head_data)]
        if len(valid_data) > 0:
            ax1.text(0.02, 0.98, f'Min: {np.min(valid_data):.1f} m\nMax: {np.max(valid_data):.1f} m\nMean: {np.mean(valid_data):.1f} m', 
                    transform=ax1.transAxes, verticalalignment='top', 
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 2: Head contours using cleaned data
    if 'head_clean' in results:
        ax2 = axes[0, 1]
        head_data = results['head_clean'][0, :, :]
        
        # Remove NaN values for contouring
        valid_mask = ~np.isnan(head_data)
        if valid_mask.any():
            # Create coordinate arrays
            rows, cols = head_data.shape
            x = np.arange(cols)
            y = np.arange(rows)
            X, Y = np.meshgrid(x, y)
            
            # Apply mask to coordinates and data
            X_valid = X[valid_mask]
            Y_valid = Y[valid_mask]
            head_valid = head_data[valid_mask]
            
            # Create contour plot with valid data
            try:
                # Use tricontour for irregular data
                triang = plt.tri.Triangulation(X_valid, Y_valid)
                contours = ax2.tricontour(triang, head_valid, colors='black', alpha=0.7, levels=10)
                ax2.clabel(contours, inline=True, fontsize=8)
                ax2.set_title('Head Contours (Layer 1)')
            except Exception as e:
                # Fallback to regular contour if tricontour fails
                contours = ax2.contour(head_data, colors='black', alpha=0.7, levels=10)
                ax2.clabel(contours, inline=True, fontsize=8)
                ax2.set_title('Head Contours (Layer 1)')
        else:
            ax2.text(0.5, 0.5, 'No valid head data\nfor contouring', 
                    transform=ax2.transAxes, ha='center', va='center')
            ax2.set_title('Head Contours (Layer 1)')
        
        ax2.set_xlabel('Column')
        ax2.set_ylabel('Row')
    
    # Plot 3: Head histogram using cleaned data
    if 'head_clean' in results:
        ax3 = axes[1, 0]
        head_data = results['head_clean'][0, :, :]
        valid_data = head_data[~np.isnan(head_data)]
        
        if len(valid_data) > 0:
            ax3.hist(valid_data.flatten(), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
            ax3.set_title('Head Distribution Histogram')
            ax3.set_xlabel('Head (m)')
            ax3.set_ylabel('Frequency')
            ax3.grid(True, alpha=0.3)
            
            # Add statistics
            ax3.axvline(np.mean(valid_data), color='red', linestyle='--', alpha=0.8, label=f'Mean: {np.mean(valid_data):.1f}')
            ax3.axvline(np.median(valid_data), color='orange', linestyle='--', alpha=0.8, label=f'Median: {np.median(valid_data):.1f}')
            ax3.legend()
        else:
            ax3.text(0.5, 0.5, 'No valid head data\nfor histogram', 
                    transform=ax3.transAxes, ha='center', va='center')
            ax3.set_title('Head Distribution Histogram')
    
    # Plot 4: Budget summary (if available)
    ax4 = axes[1, 1]
    if 'budget' in results:
        try:
            budget = results['budget']
            # Get available budget terms
            budget_terms = budget.get_unique_record_names()
            ax4.text(0.1, 0.9, f'Available Budget Terms:', transform=ax4.transAxes, fontsize=12, fontweight='bold')
            y_pos = 0.8
            for i, term in enumerate(budget_terms[:10]):  # Show first 10 terms
                ax4.text(0.1, y_pos, f'  {term}', transform=ax4.transAxes, fontsize=10)
                y_pos -= 0.05
            ax4.set_title('Budget Information')
            ax4.axis('off')
        except Exception as e:
            ax4.text(0.5, 0.5, f'Budget data\nnot available\n{str(e)}', 
                    transform=ax4.transAxes, ha='center', va='center')
            ax4.set_title('Budget Information')
            ax4.axis('off')
    else:
        ax4.text(0.5, 0.5, 'No budget data\navailable', 
                transform=ax4.transAxes, ha='center', va='center')
        ax4.set_title('Budget Information')
        ax4.axis('off')
    
    plt.tight_layout()
    
    # Save the plot
    output_file = os.path.join(model_path, f"{model_name}_results.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Results visualization saved to: {output_file}")
    
    # Show the plot
    plt.show()
    
    # Create additional FloPy-specific visualizations
    create_flopy_plots(results, model_path, model_name)

def create_flopy_plots(results, model_path, model_name):
    """
    Create additional visualizations using FloPy's built-in plotting utilities.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing simulation results
    model_path : str
        Path to the model directory
    model_name : str
        Name of the model
    """
    print("Creating FloPy-specific visualizations...")
    
    if 'head' in results:
        try:
            # Create a FloPy-style head plot
            fig, ax = plt.subplots(1, 1, figsize=(12, 10))
            
            # Get the head data
            head_data = results['head'][0, :, :]  # First layer
            
            # Create a proper masked array for MODFLOW no-data values
            masked_head = np.ma.masked_where(head_data == -999.0, head_data)
            
            # Create the plot
            im = ax.imshow(masked_head, cmap='RdYlBu_r', aspect='auto', interpolation='nearest')
            
            # Add title and labels
            ax.set_title(f'MODFLOW Head Distribution - {model_name}', fontsize=16, fontweight='bold')
            ax.set_xlabel('Column', fontsize=12)
            ax.set_ylabel('Row', fontsize=12)
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.set_label('Head (m)', fontsize=12)
            
            # Add grid
            ax.grid(True, alpha=0.3, color='black')
            
            # Add statistics text box
            valid_data = masked_head.compressed()  # Get non-masked values
            if len(valid_data) > 0:
                stats_text = f'Statistics:\nMin: {np.min(valid_data):.1f} m\nMax: {np.max(valid_data):.1f} m\nMean: {np.mean(valid_data):.1f} m\nStd: {np.std(valid_data):.1f} m'
                ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9), fontsize=10)
            
            plt.tight_layout()
            
            # Save the FloPy plot
            flopy_output_file = os.path.join(model_path, f"{model_name}_flopy_head.png")
            plt.savefig(flopy_output_file, dpi=300, bbox_inches='tight')
            print(f"FloPy head visualization saved to: {flopy_output_file}")
            
            # Show the plot
            plt.show()
            
        except Exception as e:
            print(f"Error creating FloPy plot: {e}")
            import traceback
            traceback.print_exc()

def analyze_model_performance(model_path, model_name):
    """
    Analyze model performance and convergence.
    
    Parameters:
    -----------
    model_path : str
        Path to the model directory
    model_name : str
        Name of the model
    """
    print("Analyzing model performance...")
    
    # Check output file
    output_file = os.path.join(model_path, f"{model_name}.out")
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                lines = f.readlines()
            
            # Look for convergence information
            convergence_info = []
            for line in lines:
                if any(keyword in line.lower() for keyword in ['convergence', 'iteration', 'residual']):
                    convergence_info.append(line.strip())
            
            if convergence_info:
                print("\nConvergence Information:")
                for info in convergence_info[:10]:  # Show first 10 lines
                    print(f"  {info}")
            else:
                print("No convergence information found in output file")
                
        except Exception as e:
            print(f"Error reading output file: {e}")
    
    # Check cell summary if available
    summary_file = os.path.join(model_path, f"{model_name}.CellSummary.csv")
    if os.path.exists(summary_file):
        try:
            import pandas as pd
            df = pd.read_csv(summary_file)
            print(f"\nCell Summary Statistics:")
            print(f"  Total cells: {len(df)}")
            if 'Head' in df.columns:
                print(f"  Head range: {df['Head'].min():.3f} to {df['Head'].max():.3f}")
                print(f"  Mean head: {df['Head'].mean():.3f}")
        except ImportError:
            print("pandas not available for CSV analysis")
        except Exception as e:
            print(f"Error reading cell summary: {e}")

def main():
    """
    Main function to run the complete MODFLOW analysis workflow.
    """
    # Define paths
    current_dir = Path(__file__).parent
    model_path = current_dir / "bbottoms_MODFLOW"
    model_name = "bbottoms"
    
    print("=" * 60)
    print("MODFLOW Simulation Analysis with FloPy")
    print("=" * 60)
    
    # Check if model directory exists
    if not model_path.exists():
        print(f"Error: Model directory not found: {model_path}")
        return
    
    # Load the model
    mf = load_modflow_model(str(model_path))
    
    if mf is None:
        print("Failed to load model. Exiting.")
        return
    
    # Display model information
    print("\nModel Information:")
    print(f"  Name: {mf.name}")
    print(f"  Version: {mf.version}")
    print(f"  Working directory: {mf.model_ws}")
    
    # List available packages
    print("\nAvailable packages:")
    for pkg in mf.get_package_list():
        print(f"  {pkg}")
    
    # Run simulation (optional - comment out if you just want to analyze existing results)
    print("\n" + "=" * 40)
    print("SIMULATION STEP (Optional)")
    print("=" * 40)
    print("Uncomment the following line if you want to run a new simulation:")
    print("# run_modflow_simulation(mf, str(model_path))")
    
    # Load existing results
    print("\n" + "=" * 40)
    print("LOADING EXISTING RESULTS")
    print("=" * 40)
    results = load_simulation_results(str(model_path), model_name)
    
    # Analyze model performance
    print("\n" + "=" * 40)
    print("MODEL PERFORMANCE ANALYSIS")
    print("=" * 40)
    analyze_model_performance(str(model_path), model_name)
    
    # Create visualizations
    print("\n" + "=" * 40)
    print("CREATING VISUALIZATIONS")
    print("=" * 40)
    visualize_results(results, str(model_path), model_name)
    
    # Demonstrate FloPy utilities
    print("\n" + "=" * 40)
    print("DEMONSTRATING FLOPY UTILITIES")
    print("=" * 40)
    demonstrate_flopy_utilities(results, str(model_path), model_name)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)

def demonstrate_flopy_utilities(results, model_path, model_name):
    """
    Demonstrate FloPy's built-in utilities for MODFLOW result visualization.
    This shows the proper FloPy way to handle MODFLOW data.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing simulation results
    model_path : str
        Path to the model directory
    model_name : str
        Name of the model
    """
    print("Demonstrating FloPy built-in utilities...")
    
    try:
        # Import FloPy plotting utilities
        from flopy.plot import PlotMapView
        from flopy.utils import HeadFile, CellBudgetFile
        
        # Create a simple model structure for plotting
        # Note: In a real application, you'd load the full model
        print("Creating FloPy plotting utilities demonstration...")
        
        # Method 1: Using FloPy's PlotMapView (requires model object)
        print("Note: PlotMapView requires a full model object with grid information")
        print("This demonstrates the concept of FloPy's plotting approach")
        
        # Method 2: Direct data manipulation with FloPy utilities
        if 'head' in results:
            print("\nUsing FloPy's HeadFile utilities:")
            
            # Get head data with proper time indexing
            head_file = os.path.join(model_path, f"{model_name}.hed")
            headobj = HeadFile(head_file)
            
            # Get available times and stress periods
            times = headobj.get_times()
            kstpkper = headobj.get_kstpkper()
            
            print(f"Available times: {times}")
            print(f"Available stress periods: {kstpkper}")
            
            # Get data for specific time/stress period
            if len(times) > 0:
                head_data = headobj.get_data(totim=times[0])
                print(f"Head data for time {times[0]}: shape {head_data.shape}")
                
                # Create a proper masked array for MODFLOW conventions
                # MODFLOW uses -999.0 for no-data values
                masked_head = np.ma.masked_where(head_data == -999.0, head_data)
                
                # Create a professional MODFLOW-style plot
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
                
                # Plot 1: Standard MODFLOW head plot
                im1 = ax1.imshow(masked_head[0, :, :], cmap='RdYlBu_r', 
                                aspect='auto', interpolation='nearest')
                ax1.set_title(f'MODFLOW Head - {model_name}\n(Time: {times[0]})', fontsize=14, fontweight='bold')
                ax1.set_xlabel('Column', fontsize=12)
                ax1.set_ylabel('Row', fontsize=12)
                ax1.grid(True, alpha=0.3, color='black')
                
                # Add colorbar
                cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.8)
                cbar1.set_label('Head (m)', fontsize=12)
                
                # Plot 2: Enhanced head plot with statistics
                im2 = ax2.imshow(masked_head[0, :, :], cmap='viridis', 
                                aspect='auto', interpolation='nearest')
                ax2.set_title(f'Enhanced Head Visualization\n(Time: {times[0]})', fontsize=14, fontweight='bold')
                ax2.set_xlabel('Column', fontsize=12)
                ax2.set_ylabel('Row', fontsize=12)
                ax2.grid(True, alpha=0.3, color='black')
                
                # Add colorbar
                cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.8)
                cbar2.set_label('Head (m)', fontsize=12)
                
                # Add statistics overlay
                valid_data = masked_head.compressed()
                if len(valid_data) > 0:
                    stats_text = (f'Statistics:\n'
                                f'Min: {np.min(valid_data):.1f} m\n'
                                f'Max: {np.max(valid_data):.1f} m\n'
                                f'Mean: {np.mean(valid_data):.1f} m\n'
                                f'Std: {np.std(valid_data):.1f} m\n'
                                f'Cells: {len(valid_data)}')
                    
                    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
                            verticalalignment='top', fontsize=10,
                            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))
                
                plt.tight_layout()
                
                # Save the FloPy utilities plot
                flopy_utils_output = os.path.join(model_path, f"{model_name}_flopy_utilities.png")
                plt.savefig(flopy_utils_output, dpi=300, bbox_inches='tight')
                print(f"FloPy utilities demonstration saved to: {flopy_utils_output}")
                
                plt.show()
                
        # Method 3: Demonstrate budget file utilities
        if 'budget' in results:
            print("\nUsing FloPy's CellBudgetFile utilities:")
            budget_file = os.path.join(model_path, f"{model_name}.ccf")
            budgetobj = CellBudgetFile(budget_file)
            
            # Get available budget terms
            budget_terms = budgetobj.get_unique_record_names()
            print(f"Available budget terms: {budget_terms}")
            
            # Show how to extract specific budget data
            if len(budget_terms) > 0:
                print(f"Example: First budget term is '{budget_terms[0]}'")
                print("You can extract this data using: budgetobj.get_data(text=budget_terms[0])")
        
        print("\nFloPy utilities demonstration complete!")
        print("Key points:")
        print("1. FloPy automatically handles MODFLOW file formats")
        print("2. Use HeadFile and CellBudgetFile for result loading")
        print("3. Handle -999.0 no-data values with masked arrays")
        print("4. PlotMapView provides grid-aware plotting (requires full model)")
        
    except ImportError as e:
        print(f"FloPy plotting utilities not available: {e}")
        print("This is normal if you're using an older version of FloPy")
    except Exception as e:
        print(f"Error demonstrating FloPy utilities: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

