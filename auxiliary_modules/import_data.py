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

def normalize_gatherings(table,normalizing_columns = ["name","position","email"]):
    for col in normalizing_columns:
        if col in table.columns:
            table[col] = table[col].apply(lambda x: str(x).lower())
            table[col] = table[col].apply(lambda x: x.replace("nan",""))