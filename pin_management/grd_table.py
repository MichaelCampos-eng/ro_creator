import pandas as pd
import argparse
import os

def save(file_name, df, clear):
    clear()
    print(f"\nSaving dataframe as {file_name}...")
    df.to_csv(f"{file_name}.csv", index=False)
    print("Saved\n")

def setup(column_names):
    return pd.DataFrame(columns=column_names)

def display(df):
    print("\n======================")
    print("Ground Connections")
    print(f"{df}")
    print("======================\n")
    
def main():
    clear = lambda: os.system('cls')
    parser = argparse.ArgumentParser(description="Accept a list of column name in str")
    parser.add_argument("-cn", "--column_names", nargs="+", type=str, help="List of column names", required=True)
    parser.add_argument("-fn", "--file_name", type=str, help="Save as name", required=True)
    args = parser.parse_args()
    if len(args.column_names) != 2:
        raise ValueError("There can only be TWO columns")
    
    df = setup(args.column_names)
    
    while True:
        left_command = input(f"Add to {args.column_names[0]}: ")

        if left_command == "Q":
            save(args.file_name, df, clear=clear)
            break

        if left_command.split(" ")[0] == "remove":
            try: 
                index = int(left_command.split(" ")[1])
                df.drop(index, inplace=True)
                df.reset_index(drop=True, inplace=True)
                display(df)
                print(f"Entry at index {index} removed\n")
                continue
            except Exception as e:
                print(f"Invalid integer: {left_command[1]}")
        
        right_command = input(f"Add to {args.column_names[1]}: ")

        if right_command == "Q":
            save(args.file_name, df)
            break

        if right_command.split(" ")[0] == "remove":
            try: 
                index = int(right_command.split(" ")[1])
                df.drop(index, inplace=True)
                df.reset_index(drop=True, inplace=True)
                display(df)
                print(f"Entry at index {index} removed\n")
                continue
            except Exception as e:
                print(f"Invalid integer: {right_command[1]}")
        clear()

        left_column, right_column = df.columns
        new_row = pd.DataFrame({left_column: [left_command.replace(" ", "")], 
                                right_column: [right_command.replace(" ", "")]})
        df = pd.concat([df, new_row])
        df_sorted = df.apply(lambda row: tuple(sorted([row[left_column], row[right_column]])), axis=1)
        df_no_duplicates = pd.DataFrame(df_sorted, columns=['pair']).drop_duplicates()
        df = pd.DataFrame(df_no_duplicates['pair'].to_list(), columns=[left_column, right_column])
        display(df)

if __name__ == "__main__":
    main()