"""This is the mane script orchestrating the restructuring and plotting of the content of the pollution_data directory.
"""

# Import necessary packages here
from pathlib import Path
import shutil
import tempfile
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    display_diagnostics,
    display_directory_tree,
    is_gas_csv,
    merge_parent_and_basename,
    delete_directories
)
from analytic_tools.plotting import(
    plot_pollution_data
)

def restructure_pollution_data(pollution_dir: str or Path, dest_dir: str or Path) -> None:
    """This function searches the tree of pollution_data directory pointed to by pollution_dir for .csv files
        that satisfy the criteria described in the assignment. It then moves a renamed copy of these files to gas-specific
        sub-directories in dest_dir, which will be created based on the gasses present in pollution_data directory.

    Parameters:
        - pollution_dir (str or pathlib.Path) : The absolute path to pollution_data directory
        - dest_dir (str or pathlib.Path) : The absolute path to new directory where gas-specific subdirectories will
                                     be created, which must be pollution_data_restructured/by_gas

    Returns:
    None

    Pseudocode:
    1. Iterate through the contents of `pollution_dir`
    2. Find valid .csv files for gasses ([`[gas_formula].csv` files of correct gas types).
    3. Create/assign new directory to store them under `dest_dir` using `get_dest_dir_from_csv_file`
    4. Assign a new name using `merge_parent_and_basename` and copy the file to the new destination.
       If the file happens already to exist there, it should be overwritten.
    """

    if not isinstance(pollution_dir,(str,Path)) or not isinstance(dest_dir,(str,Path)): 
        raise TypeError("Object is not path-like")

    pollution_dir = Path(pollution_dir)
    print(pollution_dir)
    dest_dir = Path(dest_dir)
    print(dest_dir)

    if not dest_dir.exists() or not pollution_dir.exists():
        raise NotADirectoryError(f'{dest_dir} {pollution_dir} Directory doesnt exist')

    for path in pollution_dir.rglob('*'):
        try: 
            if is_gas_csv(path): 
                dest_gas_dir = get_dest_dir_from_csv_file(dest_dir, path)
                new_name = merge_parent_and_basename(path)
                dest_path = dest_gas_dir / new_name
                shutil.copy(path, dest_path)
        except ValueError as e: 
            print(e)

def analyze_pollution_data(work_dir: str or Path) -> None:
    """Do the restructuring of the pollution_data and plot
       the statistics showing emissions of each gas as function of all the corresponding
       sources. The new structure and the plots are saved in a separate directory under work_dir

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the new directories will be created

    Returns:
    None

    Pseudocode:
    - Create pollution_data_restructured in work_dir
    - Populate it with a by_gas subdirectory
    - Make a call to restructure_pollution_data
    - Populate pollution_data_restructured with a subdirectory named figures
    - Make a call to plot_pollution_data
    """

    if not isinstance(work_dir, (str,Path)): 
        raise TypeError(f'{work_dir} is not a Path-like object')
    
    work_dir = Path(work_dir)

    if not work_dir.is_dir(): 
        raise NotADirectoryError(f'{work_dir} is not directory or doesnt exist')
                  
    pollution_dir = work_dir / "pollution_data"
    
    restructured_dir = work_dir / "pollution_data_restructured"
    restructured_dir.mkdir(parents=True)

    content = get_diagnostics(pollution_dir)
    display_diagnostics(pollution_dir,content)
    display_directory_tree(pollution_dir,3)

    by_gas_dir = restructured_dir / "by_gas"
    by_gas_dir.mkdir(parents=True)
    
    restructure_pollution_data(pollution_dir,by_gas_dir)

    figures_dir = restructured_dir / "figures"
    figures_dir.mkdir(parents=True)

    plot_pollution_data(by_gas_dir, figures_dir)

def analyze_pollution_data_tmp(work_dir: str or Path) -> None:
    """Do the restructuring of the pollution_data in a temporary directory and create the figures
       showing emissions of each gas as function of all the corresponding
       sources. The new figures are saved in a real directory under work_dir.

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the figures will be saved

    Returns:
    None

    Pseudocode:
    - Create a temporary directory and copy pollution_data directory to it
    - Perform the same operations as in analyze_pollution_data
    - Copy (or directly save) the figures to a directory named `figures` under the original working directory pointed to by `work_dir`
    """
     
    if not isinstance(work_dir, (str,Path)): 
        raise TypeError(f'{work_dir} is not a Path-like object')
    
    work_dir = Path(work_dir)

    if not work_dir.is_dir(): 
        raise NotADirectoryError(f'{work_dir} is not directory or doesnt exist')

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        shutil.copytree(work_dir / "pollution_data", temp_dir / "pollution_data")
    
        pollution_dir = temp_dir / "pollution_data"
    
        restructured_dir = temp_dir / "pollution_data_restructured"
        restructured_dir.mkdir(parents=True)

        content = get_diagnostics(pollution_dir)
        display_diagnostics(pollution_dir,content)
        display_directory_tree(pollution_dir,3)

        by_gas_dir = restructured_dir / "by_gas"
        by_gas_dir.mkdir(parents=True)
        
        restructure_pollution_data(pollution_dir,by_gas_dir)

        figures_dir = work_dir / "figures"
        figures_dir.mkdir(parents=True)

        plot_pollution_data(by_gas_dir, figures_dir)


if __name__ == "__main__":
    work_dir =  '/Users/tonjesandanger/Desktop/IN4110/IN3110-tonjevs/assignment2'
    analyze_pollution_data(work_dir)
    
