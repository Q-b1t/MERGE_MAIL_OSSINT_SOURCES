import pandas as pd

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