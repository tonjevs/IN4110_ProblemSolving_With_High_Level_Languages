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
    
