#!/usr/bin/env python3
"""
Debug script to examine head data structure and identify plotting issues.
"""

import flopy
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

def debug_head_data():
    """
    Debug the head data loading and structure.
    """
    # Define paths
    current_dir = Path(__file__).parent
    model_path = current_dir / "bbottoms_MODFLOW"
    model_name = "bbottoms"
    
    print("=" * 60)
    print("DEBUGGING HEAD DATA")
    print("=" * 60)
    
    # Try to load head file
    head_file = os.path.join(model_path, f"{model_name}.hed")
    if os.path.exists(head_file):
        print(f"Head file exists: {head_file}")
        print(f"File size: {os.path.getsize(head_file)} bytes")
        
        try:
            # Load head file using FloPy
            headobj = flopy.utils.HeadFile(head_file)
            print(f"Head object created successfully")
            print(f"Available times: {headobj.get_times()}")
            print(f"Available kstpkper: {headobj.get_kstpkper()}")
            
            # Get data
            head_data = headobj.get_data()
            print(f"Head data shape: {head_data.shape}")
            print(f"Head data type: {head_data.dtype}")
            print(f"Head data min: {np.nanmin(head_data)}")
            print(f"Head data max: {np.nanmax(head_data)}")
            print(f"Head data mean: {np.nanmean(head_data)}")
            print(f"Number of NaN values: {np.isnan(head_data).sum()}")
            print(f"Number of infinite values: {np.isinf(head_data).sum()}")
            
            # Check for specific values
            unique_vals = np.unique(head_data)
            print(f"Unique values (first 20): {unique_vals[:20]}")
            
            # Try different time steps
            if len(headobj.get_times()) > 0:
                print(f"\nTrying first time step...")
                head_data_t0 = headobj.get_data(totim=headobj.get_times()[0])
                print(f"Time 0 head data shape: {head_data_t0.shape}")
                print(f"Time 0 head data min: {np.nanmin(head_data_t0)}")
                print(f"Time 0 head data max: {np.nanmax(head_data_t0)}")
            
            # Try different kstpkper
            if len(headobj.get_kstpkper()) > 0:
                print(f"\nTrying first kstpkper...")
                kstpkper = headobj.get_kstpkper()[0]
                head_data_kp = headobj.get_data(kstpkper=kstpkper)
                print(f"KSTPKPER {kstpkper} head data shape: {head_data_kp.shape}")
                print(f"KSTPKPER {kstpkper} head data min: {np.nanmin(head_data_kp)}")
                print(f"KSTPKPER {kstpkper} head data max: {np.nanmax(head_data_kp)}")
            
            return head_data
            
        except Exception as e:
            print(f"Error loading head file: {e}")
            import traceback
            traceback.print_exc()
    
    return None

def try_alternative_head_loading():
    """
    Try alternative methods to load head data.
    """
    print("\n" + "=" * 60)
    print("TRYING ALTERNATIVE HEAD LOADING METHODS")
    print("=" * 60)
    
    current_dir = Path(__file__).parent
    model_path = current_dir / "bbottoms_MODFLOW"
    model_name = "bbottoms"
    
    # Try reading as binary file directly
    head_file = os.path.join(model_path, f"{model_name}.hed")
    
    try:
        # Try to read as raw binary
        with open(head_file, 'rb') as f:
            raw_data = f.read()
            print(f"Raw binary file size: {len(raw_data)} bytes")
            print(f"First 100 bytes: {raw_data[:100]}")
            
            # Look for MODFLOW header information
            if b'MODFLOW' in raw_data or b'HEAD' in raw_data:
                print("Found MODFLOW/HEAD identifiers in binary data")
            
    except Exception as e:
        print(f"Error reading raw binary: {e}")
    
    # Try HDF5 version if it exists
    h5_file = os.path.join(model_path, f"{model_name}.hed.h5")
    if os.path.exists(h5_file):
        print(f"\nHDF5 head file exists: {h5_file}")
        try:
            import h5py
            with h5py.File(h5_file, 'r') as f:
                print("HDF5 head file contents:")
                for key in f.keys():
                    print(f"  {key}")
                    if isinstance(f[key], h5py.Dataset):
                        print(f"    Shape: {f[key].shape}, Type: {f[key].dtype}")
                        data = f[key][:]
                        print(f"    Data min: {np.nanmin(data)}, max: {np.nanmax(data)}")
        except ImportError:
            print("h5py not available")
        except Exception as e:
            print(f"Error reading HDF5: {e}")

def create_test_plot(head_data):
    """
    Create a simple test plot to debug visualization issues.
    """
    if head_data is None:
        print("No head data to plot")
        return
    
    print("\n" + "=" * 60)
    print("CREATING TEST PLOT")
    print("=" * 60)
    
    # Create a simple plot
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Raw data
    plt.subplot(2, 2, 1)
    if len(head_data.shape) == 3:
        data_to_plot = head_data[0, :, :]  # First layer
    else:
        data_to_plot = head_data
    
    plt.imshow(data_to_plot, cmap='viridis', aspect='auto')
    plt.title('Raw Head Data')
    plt.colorbar(label='Head (m)')
    
    # Plot 2: Data with different colormap
    plt.subplot(2, 2, 2)
    plt.imshow(data_to_plot, cmap='plasma', aspect='auto')
    plt.title('Head Data (Plasma colormap)')
    plt.colorbar(label='Head Head Data (Plasma colormap)')
    plt.colorbar(label='Head (m)')
    
    # Plot 3: Contour plot
    plt.subplot(2, 2, 3)
    try:
        contours = plt.contour(data_to_plot, colors='black', alpha=0.7)
        plt.clabel(contours, inline=True, fontsize=8)
        plt.title('Head Contours')
    except Exception as e:
        plt.text(0.5, 0.5, f'Contour error:\n{str(e)}', 
                transform=plt.gca().transAxes, ha='center', va='center')
        plt.title('Head Contours (Failed)')
    
    # Plot 4: Histogram
    plt.subplot(2, 2, 4)
    plt.hist(data_to_plot.flatten(), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Head Distribution Histogram')
    plt.xlabel('Head (m)')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('debug_head_plot.png', dpi=300, bbox_inches='tight')
    print("Debug plot saved as 'debug_head_plot.png'")
    plt.show()

if __name__ == "__main__":
    # Debug head data
    head_data = debug_head_data()
    
    # Try alternative loading methods
    try_alternative_head_loading()
    
    # Create test plot
    create_test_plot(head_data)
