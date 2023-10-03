import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auxiliary_modules.import_data import *
from argparse import ArgumentParser,Namespace


if __name__ == '__main__':
    # create cli
    parser = ArgumentParser()
    parser.add_argument("-m","--mails_list",help="A text file containing a list of emails",type=str,default=None,nargs="?")
    parser.add_argument("-g","--manual_gatherings",help="A excel book containing manual gatherings of employees and emails",type=str,default=None,nargs="?")
    parser.add_argument("-l","--leaks_table",help="An excel book containing emails leaks",type=str,default=None,nargs="?")
    parser.add_argument("-v","--verbose",help="Whether to output information on the script's progress in the console",type=bool,default=False,nargs="?")
    parser.add_argument("-o","--output_file",help="Name of the output file (default: \"merged_data\")",type=str,default="merged_data",nargs="?")
    parser.add_argument("-f","--output_format",help="It can be either \"excel\" or \"csv\" (default: \"excel\")",type=str,default="excel",nargs="?")



    # fetch arguments
    args: Namespace = parser.parse_args()

    # input files
    mails_text_file_path = args.mails_list
    leaks_excel_file_path = args.leaks_table
    manual_gatherings_excel_file_path = args.manual_gatherings
    merged_data_file_path = args.output_file
    verbose = args.verbose
    output_format = args.output_format

    # validate the files that exists
    metadata = get_metadata(leaks=leaks_excel_file_path,list=mails_text_file_path,gatherings=manual_gatherings_excel_file_path)
    validate_metadata(metadata=metadata)
    data_dumps = fetch_data(metadata=metadata)
    merge_tables(data_dumps=data_dumps,metadata=metadata)
    merged_table = merge_tables(metadata=metadata,data_dumps=data_dumps)
    save_table(parsed_table=merged_table,save_path=merged_data_file_path,output_format=output_format,verbose=verbose)    

    """
    # read values
    leaks_dump = get_excel_table(filename=leaks_excel_file_path)
    mail_text_file_dump = get_mail_df(filename=mails_text_file_path)
    manual_gatherings_dump = get_excel_table(filename=manual_gatherings_excel_file_path)

    # normalize the values if the string columns to merge as much data as possible
    normalize_gatherings(manual_gatherings_dump)
    normalize_gatherings(leaks_dump)
    
    # merge the leaks data with the raw mail dump
    merged_leaks_mails = leaks_dump.merge(mail_text_file_dump,how="outer",on="email")
    # meget the merged data with the manual gatherings
    merged_leaks_mails_gatherings = merged_leaks_mails.merge(manual_gatherings_dump,how="outer",on="email")

    # remove redundant columns
    for col in merged_leaks_mails_gatherings.columns:
        if "Unnamed" in col:
            merged_leaks_mails_gatherings.drop(col,axis=1, inplace=True)

    
    if "name_x" in merged_leaks_mails_gatherings.columns:
        merged_leaks_mails_gatherings["name_x"].update(merged_leaks_mails_gatherings["name_y"])
        merged_leaks_mails_gatherings.drop("name_y",axis=1,inplace=True)
        merged_leaks_mails_gatherings.rename(columns={"name_x": "name"},inplace=True)
    # export
    merged_leaks_mails_gatherings.to_excel(merged_data_file_path)
    """