from pathlib import Path
import os
from typing import Dict, List


def get_diagnostics(dir: str or Path) -> Dict[str, int]:
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


