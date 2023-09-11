from pathlib import Path
import os
from typing import Dict, List


def get_diagnostics(dir: str or Path) -> Dict[str, int]:
    """Get diagnostics for the directory tree, with root directory pointed to by dir.
       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md and other files in the whole directory tree.

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest

    Returns:
        res (Dict[str, int]) : a dictionary of the findings with following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    """

    res = {
        "files": 0,
        "subdirectories": 0,
        ".csv files": 0,
        ".txt files": 0,
        ".npy files": 0,
        ".md files": 0,
        "other files": 0,
    }
    if not isinstance(dir, (str,Path)):
        raise TypeError("Invalid type for directiory. Expected a path...")
    
    path = Path(dir)

    if not path.is_dir():
        raise NotADirectoryError(f"'{dir}' is not a directiory...")
    
    if not path.exists():
        raise NotADirectoryError(f"'{dir}' doesn't exist...")
    

    for paths in path.rglob('*'):  
        if paths.is_file(): 
            res['files'] += 1
            pathname = str(paths)
            if '.csv' in pathname:
                res['.csv files'] += 1
            elif '.txt' in pathname :
                res['.txt files'] += 1
            elif '.npy' in pathname:
                res['.npy files'] += 1
            elif '.md' in pathname :
                res['.md files'] += 1
            else:
                res['other files'] += 1
        elif path.is_dir():
            res['subdirectories'] += 1

    return res


def display_diagnostics(dir: str or Path, contents: Dict[str, int]) -> None:
    """Display diagnostics for the directory tree, with root directory pointed to by dir.
        Objects to display: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    Parameters:
        dir (str or pathlib.Path) : Absolute path the directory of interest
        contents (Dict[str, int]) : a dictionary of the same type as return type of get_diagnostics, has the form:

            .. highlight:: python
            .. code-block:: python

                {
                    "files": 0,
                    "subdirectories": 0,
                    ".csv files": 0,
                    ".txt files": 0,
                    ".npy files": 0,
                    ".md files": 0,
                    "other files": 0,
                }

    Returns:
        None
    """

    if not isinstance(dir, (str,Path)):
        raise TypeError("Invalid type for directiory. Expected a path...")
    
    if not isinstance(contents, (str,dict)):
        raise TypeError("Invalid type for contents. Expected a dictionary...")
    
    path = Path(dir)

    if not path.is_dir():
        raise NotADirectoryError(f"'{dir}' is not a directiory...")
    
    if not path.exists():
        raise NotADirectoryError(f"'{dir}' doesn't exist...")
    
    print(f"Diagnostic for path: {path}")

    for fileType, number in contents.items():
        print(f"{fileType}: {number}")

def display_directory_tree(dir: str or Path, maxfiles: int = 3) -> None:
    """Display a directory tree, with root directory pointed to by dir.
       Limit the number of files to be displayed for convenience to maxfiles.
       This tree is built with inspiration from the code written by "Flimm" at https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest
        maxfiles (int) : Maximum number of files to be displayed at each level in the tree, default to three.

    Returns:
        None

    """
    if not isinstance(dir, (str,Path)):
        raise TypeError("Invalid type for directiory. Expected a path...")
    
    if not isinstance(maxfiles, (int)):
        raise TypeError("Invalid type for maxfiles. Expected type int")
    
    path = Path(dir)
    
    if not path.is_dir():
        raise NotADirectoryError(f"'{dir}' is not a directiory...")
    
    if not path.exists():
        raise NotADirectoryError(f"'{dir}' doesn't exist...")
    
    if maxfiles < 1:
        raise ValueError("Maxfiles should have more that 1 file:/")
    

    print(f'Root: {path.name} /')
    path = path / "by_src"
    for paths in path.rglob('*'):
        if paths.is_dir():
            print(f'-  {paths.name}')
            subdir = list(paths.glob('*'))
            for items in subdir[:maxfiles]: 
                if items.is_dir(): 
                    print(f'   - {items.name}')
                elif items.is_file(): 
                    print(f'   - {items.name}')
            if len(subdir) > maxfiles:
                print(f'   - ({len(subdir) - maxfiles} more)')
               
def is_gas_csv(path: str or Path) -> bool:
    """Checks if a csv file pointed to by path is an original gas statistics file.
        An original file must be called '[gas_formula].csv' where [gas_formula] is
        in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
         - path (str of pathlib.Path) : Absolute path to .csv file that will be checked

    Returns
         - (bool) : Truth value of whether the file is an original gas file
    """

    if not isinstance(path, (str,Path)):
        raise TypeError("Invalid type for directiory. Expected a path...")
    
    path = Path(path)

    if path.suffix.lower() != '.csv':
        raise ValueError("File is not a .csv")
    
    gasses = ["CO2", "CH4", "N2O", "SF6", "H2"]

    filename = path.stem
    
    if filename in gasses: 
        return True
    
    return False


def get_dest_dir_from_csv_file(dest_parent: str or Path, file_path: str or Path) -> Path:
    """Given a file pointed to by file_path, derive the correct gas_[gas_formula] directory name.
        Checks if a directory "gas_[gas_formula]", exists and if not, it creates one as a subdirectory under dest_parent.

        The file pointed to by file_path must be a valid file. A valid file must be called '[gas_formula].csv' where [gas_formula]
        is in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
        - dest_parent (str or pathlib.Path) : Absolute path to parent directory where gas_[gas_formula] should/will exist
        - file_path (str or pathlib.Path) : Absolute path to file that gas_[gas_formula] directory will be derived from

    Returns:
        - (pathlib.Path) : Absolute path to the derived directory

    """
    dest_parent = Path(dest_parent)
    dest_path = Path(file_path)

    if not isinstance(dest_parent, Path) or not isinstance(dest_path, Path): 
        raise TypeError("dest should be path-like")
    
    if not dest_parent.is_dir(): 
        raise NotADirectoryError(f'{dest_parent} is not a directory')
    
    gas_formula = dest_path.stem
    
    valid = ['CO2', 'CH4', 'N2O', 'SF6', 'H2']

    if gas_formula not in valid: 
        raise ValueError(f'Invalid gas: {gas_formula}')
    
    if dest_path.suffix.lower() != '.csv' : 
        raise ValueError(f'{dest_path} is not a .csv file')
    
    dest_dir = dest_parent / f"gas_{gas_formula}"

    if not dest_dir.exists():
        dest_dir.mkdir(parents=True)
    
    return dest_dir
    
    


def merge_parent_and_basename(path: str or Path) -> str:
    """This function merges the basename and the parent-name of a path into one, uniting them with "_" character.
       It then returns the basename of the resulting path.

    Parameters:
        - path (str or pathlib.Path) : Absolute path to modify

    Returns:
        - new_base (str) : New basename of the path
    """
    path = Path(path)

    if not isinstance(path,Path): 
        raise TypeError("Path is not path")
    
    part = path.parts

    if len(part) < 2 : 
        raise ValueError("path doesn't contain both a parent and a child")

    parent = part[-2]
    baseName = part[-1]
    new_base = f"{parent}_{baseName}".replace(os.sep, '_')
    return new_base


def delete_directories(path_list: List[str or Path]) -> None:
    """Prompt the user for permission and delete the objects pointed to by the paths in path_list if
       permission is given. If the object is a directory, its whole directory tree is removed.

    Parameters:
        - path_list (List[str | Path]) : a list of absolute paths to all the objects to be removed.


    Returns:
    None
    """
    #Tror ikke denne fungerer helt riktig men det må jo være noe sånt
    for path in path_list: 
        path = Path(path)
        if not path.exists():
            print(f'Path {path} doesnt exist')
            continue
       
        if path.is_file():
            os.remove(path)
            print(f"Deleted file: {path}")
  
        elif path.is_dir(): 
            input = input(f'Do yoy want to deliete the file: {path} ? (yes/no)').strip().lower()
            if input == "yes": 
                try: 
                    os.rmdir(path)
                    print(f"Dir: {path} has been delieted")
                except OSError as e: 
                    print("An error has ocurred while trying to deliete directory")
                    print(f'{e}')
        else : 
            print(f'This ios neither a file nor a directory')


