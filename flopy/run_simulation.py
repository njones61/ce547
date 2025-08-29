#!/usr/bin/env python3
"""
Simple script to run a new MODFLOW simulation using the existing model structure.
This demonstrates how to use the main analysis code to run simulations.
"""

from main_flopy import load_modflow_model, run_modflow_simulation
from pathlib import Path

def run_new_simulation():
    """
    Run a new MODFLOW simulation using the existing model structure.
    """
    # Define paths
    current_dir = Path(__file__).parent
    model_path = current_dir / "bbottoms_MODFLOW"
    model_name = "bbottoms"
    
    print("=" * 60)
    print("Running New MODFLOW Simulation")
    print("=" * 60)
    
    # Load the existing model
    mf = load_modflow_model(str(model_path))
    
    if mf is None:
        print("Failed to load model. Exiting.")
        return
    
    # Run the simulation
    success = run_modflow_simulation(mf, str(model_path))
    
    if success:
        print("\nSimulation completed successfully!")
        print("You can now run the main analysis script to view results:")
        print("python main_flopy.py")
    else:
        print("\nSimulation failed. Check the error messages above.")

if __name__ == "__main__":
    run_new_simulation()
