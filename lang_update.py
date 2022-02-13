from deep_translator import MyMemoryTranslator
from deep_translator import GoogleTranslator
import pandas as pd
from tqdm import tqdm

langlist=["English","Hindi","Bengali","Gujrati","Kannada","Malayalam","Marathi","Tamil","Telugu","Arabic","Burmese","Spanish","French","Italian","Russian","Hebrew"]
langcodes=["en","hi","bn","gu","kn","ml","mr","ta","te","ar","my","es","fr","it","ru","iw"]

sheets=["Home Page","Search Page","Press Page","Doctors Profile Page","Contact Page","Career Page","Blogs Page","About Page","Privacy Policy Page","Terms and Conditions Page","Patient Dashboard","Doctor Dashboard"]
xls=pd.ExcelFile('Translations.xlsx')

def translate(langcode):
    trans_text=[]
    for i in tx:
        try:
            b = MyMemoryTranslator(source="en", target=langcode).translate(text=i)
        except:
                try:
                    b = GoogleTranslator(source='auto', target=langcode).translate(text=i)
                except Exception as e:
                    b = i
        trans_text.append(b)
    return trans_text

for s in sheets[3:]:
    df = pd.read_excel(xls, s)
    tx=df['value']

    for n,c in zip(langlist,langcodes):
        df[n]=translate(c)
    print(s)
    df.to_excel(f'{s}.xlsx')

