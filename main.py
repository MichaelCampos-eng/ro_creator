from wrman.conn_management.list_manager import *
import argparse
from wrman.converter.ro_tests import *
import pandas as pd
from wrman.config_classes.config import *
from wrman.utils.labels import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List manager")
    parser.add_argument("-f", "--folder_path", type=str, help="File path to save list as csv")
    parser.add_argument("-t", "--table", type=str, help="Options: wire, unused, ground")
    args = parser.parse_args()
    
    if not args.folder_path:
        raise ValueError("Insert a folder path")
    if not args.table:
        raise ValueError("Insert a table type")
    
    if args.table == "wire":
        ok = WireList()
        ok.begin_cli(folder_path=args.folder_path)
    elif args.table == "unused":
        ok = IsolatedList()
        ok.begin_cli(folder_path=args.folder_path)
    elif args.table == "ground":
        ok = GroundList()
        ok.begin_cli(folder_path=args.folder_path)
    else:
        raise ValueError("Invalid table type")