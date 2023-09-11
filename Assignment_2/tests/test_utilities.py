""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path

# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    display_diagnostics,
    display_directory_tree,
    is_gas_csv,
    merge_parent_and_basename,
)
import pytest

@pytest.mark.task12
def test_get_diagnostics(example_config):
    res = get_diagnostics(example_config)

    exp = {
        "files": 10,  # Total number of files (all types)
        "subdirectories": 5,  # Total number of subdirectories
        ".csv files": 8,  # Total number of .csv files
        ".txt files": 0,  # Total number of .txt files
        ".npy files": 2,  # Total number of .npy files
        ".md files": 0,  # Total number of .md files
        "other files": 0,  # Total number of other files
    }
    assert res == exp
    display_directory_tree(example_config,3)

@pytest.mark.task12
@pytest.mark.parametrize(
    "exception, dir",
    [(TypeError, 882719), 
     (TypeError, True), 
     (NotADirectoryError, 'tullball123'), 
     (NotADirectoryError, 'kulfil.txt')],
)

def test_get_diagnostics_exceptions(exception, dir):
   
    with pytest.raises(exception):
        get_diagnostics(dir)

@pytest.mark.task22
def test_is_gas_csv():
    valid =  ["CO2.csv", "CH4.csv", "N2O.csv", "SF6.csv", "H2.csv"]
    for filenames in valid: 
        assert is_gas_csv(filenames) is True
    
    invalid =  ["O2.csv", "CH5.csv", "N674.csv", "jeg_er_lei.csv"]
    for filenames in invalid: 
        assert is_gas_csv(filenames) is False
    
    assert is_gas_csv(Path("CO2.csv")) is True
    assert is_gas_csv("path/to/CO2.csv") is True
    assert is_gas_csv("/help/me/CH4.CSV") is True

@pytest.mark.task22
@pytest.mark.parametrize(
    "exception, path",
    [
        (ValueError, Path(__file__).parent.absolute()),
        (TypeError, 123),
        (TypeError, ["total/bs.csv"]),
        (TypeError, ["total/bs.md"]),
        (ValueError,"rar_fil")
    ],
)
def test_is_gas_csv_exceptions(exception, path):
    with pytest.raises(exception):
        is_gas_csv(path)


@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    
    example_config = Path(example_config)
      
    gasFormulas = ['CO2', 'CH4', 'N2O', 'SF6', 'H2']

    for gasses in gasFormulas: 
        path = example_config / f"{gasses}.csv"
        destDir = get_dest_dir_from_csv_file(example_config,path)

        assert destDir.is_dir()

        expName = f"gas_{gasses}"
        assert destDir.name == expName

        assert destDir.parent == example_config

    invalidGasFormula = 'superCoolGasFormulaName'
    invalidFilePath = example_config / f"{invalidGasFormula}.csv"
    
    with pytest.raises(ValueError): 
        get_dest_dir_from_csv_file(example_config,invalidFilePath)
    
    invalidDestParent = example_config / f'notDirectory'

    with pytest.raises(NotADirectoryError): 
        get_dest_dir_from_csv_file(invalidDestParent,example_config / "CO2.csv")
    
    with pytest.raises(ValueError): 
        get_dest_dir_from_csv_file(example_config,example_config)
    
    with pytest.raises(ValueError): 
        get_dest_dir_from_csv_file(example_config, example_config / "tull.txt")

@pytest.mark.task24
@pytest.mark.parametrize(
    "exception, dest_parent, file_path",
    [
        (ValueError, Path(__file__).parent.absolute(), "slayy.txt"),
        (TypeError, None, "kul_fil.txt"),  
        (TypeError, "parent_dir", None),  
        (TypeError, 732829, "file.cSv"),
        (TypeError, "amaze", True),  
        (NotADirectoryError, "nonexistent_dir", "file.csv"),
    ],
)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    with pytest.raises(exception): 
        get_dest_dir_from_csv_file(dest_parent,file_path)

@pytest.mark.task26
def test_merge_parent_and_basename():
    test_stuff = [
        ("/User/.../assignment2/pollution_data/by_src/src_agriculture/CO2.csv", "src_agriculture_CO2.csv"),
        ("some_dir/some_sub_dir", "some_dir_some_sub_dir"),
        ("some_dir/some_file.txt/", "some_dir_some_file.txt"),
    ]
    
    for input_path, expected_output in test_stuff:
        result = merge_parent_and_basename(input_path)
        assert result == expected_output

@pytest.mark.task26
@pytest.mark.parametrize(
    "exception, path",
    [
        (TypeError, 33),
        (ValueError, "assignment2")
    ],
)
def test_merge_parent_and_basename_exceptions(exception, path):
    with pytest.raises(exception): 
        merge_parent_and_basename(path)
