import pandas as pd
from termcolor import colored
from collections import Counter
import re 


def read_text_file(filename):
    with open(filename,"r",encoding="utf-8") as f:
        lines = f.readlines()
    f.close()
    return [line.strip() for line in lines]
    

def get_mail_df(filename):
    mails = read_text_file(filename=filename)
    mails_table = pd.DataFrame({"email":mails})
    return mails_table 

def get_excel_table(filename):
    return pd.read_excel(filename)

def normalize_gatherings(table,normalizing_columns = ["name","position","email"]):
    for col in normalizing_columns:
        if col in table.columns:
            table[col] = table[col].apply(lambda x: str(x).lower())
            table[col] = table[col].apply(lambda x: x.replace("nan",""))

# validate if the files where passed as parameters
def get_metadata(leaks,list,gatherings):
    inputs = [leaks,list,gatherings]
    keys = ["leaks","email_list","gatherings"]
    metadata = []
    # initialize metadata dictionary
    for inpt,key in zip(inputs,keys):
        sample = dict()
        if inpt is not None:
            sample["name"] = inpt
            sample["present"] = True
        else:
            sample["name"] = None
            sample["present"] = False
        sample["type"]= key
        metadata.append(sample)
    return metadata

def validate_name(filename):
    pattern = r"[A-Za-z0-9-_]{3,20}.(xlsx | csv | txt)"
    assert re.match(pattern,filename),colored(f"[-] {filename} name is not valid. Please limit to numbers, lower and upper case letters, and special characters: \"-\",\"_\". Please do not include the file extention.","red")

# validate if the files have the propper format and that there are at least two files
def validate_metadata(metadata):
    metadata = pd.DataFrame(metadata)
    counts = metadata["present"].value_counts()
    assert counts[True] >= 2, colored("The program requires at least 2 files in order to perform a merge operation.","red")

    #for name in metadata["name"]:
        #if name is None:
            #continue
        #validate_name(name)

def fetch_data(metadata):
    contents = dict()
    for sample in metadata:
        if sample["present"]:
            if sample["type"] == "email_list":
                contents[sample["type"]] = get_mail_df(filename=sample["name"])
            else:
                contents[sample["type"]] = get_excel_table(filename=sample["name"])
                assert "email" in contents[sample["type"]].columns and "name" in contents[sample["type"]], colored(f"The table in {sample['name']} has not the appropriate format. Please make sure the columns \"email\" and \"name\" are present.","red")
                normalize_gatherings(contents[sample["type"]])
        else:
            continue 
    return contents

def save_table(parsed_table,save_path,output_format,verbose):
    """
    Inputs: 
        - parsed_table: A processed pandas dataframe.
        - save_path: The to which the table will be saved as an excel book.
    """
    if output_format == "csv":
        filename = save_path + "." + "csv"
        parsed_table.to_csv(filename,index = False)
    else:
        filename = save_path + "." + "xlsx"
        parsed_table.to_excel(filename, index=False)
         
    if verbose:
        print(colored(f"[+] Breached data saved to {filename}","green"))

def merge_tables(data_dumps,metadata):
    leaks_present, mails_present,gatherings_present = metadata[0]["present"], metadata[1]["present"], metadata[2]["present"]
    if leaks_present and mails_present and gatherings_present:
        leaks_table,mails_table,gatherings_table = data_dumps["leaks"],data_dumps["email_list"],data_dumps["gatherings"]
        merged_table = leaks_table.merge(mails_table,how="outer",on="email")
        merged_table = merged_table.merge(gatherings_table,how="outer",on="email")
    elif leaks_present and mails_present and not gatherings_present:
        leaks_table,mails_table = data_dumps["leaks"],data_dumps["email_list"]
        merged_table = leaks_table.merge(mails_table,how="outer",on="email")
    elif leaks_present and not mails_present and gatherings_present:
        leaks_table,gatherings_table = data_dumps["leaks"],data_dumps["gatherings"]
        merged_table = leaks_table.merge(gatherings_table,how="outer",on="email")
    else:
        mails_table,gatherings_table = data_dumps["email_list"],data_dumps["gatherings"]
        merged_table = mails_table.merge(gatherings_table,how="outer",on="email")
    return merged_table
        