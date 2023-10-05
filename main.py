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
    if verbose:
        print(colored(f"[+] Validating input and output files.","blue"))
    validate_metadata(metadata=metadata,verbose=verbose)
    validate_output_file(merged_data_file_path)
    data_dumps = fetch_data(metadata=metadata,output_format=output_format)
    merge_tables(data_dumps=data_dumps,metadata=metadata,verbose=verbose)
    merged_table = merge_tables(metadata=metadata,data_dumps=data_dumps,verbose=verbose)
    save_table(parsed_table=merged_table,save_path=merged_data_file_path,output_format=output_format,verbose=verbose)    
