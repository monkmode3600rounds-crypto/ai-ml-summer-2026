import re
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

def dataframe(name):
    name=pd.DataFrame(list(is_product_dict.items()), columns=["Description", "is_product"])
    return name

def match_func(m):
    if m:
        return False
    else:
        return True

def check_display(text):
    is_product_pattern = re.compile(r"\b(?<=clear)\s*display\b", re.IGNORECASE)
    non_product_pattern = re.compile(r'\b(?:shop|for)\s*display\b', re.IGNORECASE)
    if non_product_pattern.search(text):
        return False
    elif is_product_pattern.search(text):
        return True
    elif re.search(r'\bdisplay\b', text, re.IGNORECASE):
        return "需人工確認"  # 落入灰色地帶
    return "no match"


print('Check number 1')
pattern = re.compile(
    r'\bdisplay\b(?!\s*(?:box|case|tray|carton|crate)\b)',  # display 後面不是 box/case/stand/only (problem here )
    re.IGNORECASE
) # what is * in regex?

test_cases=['robot mug in display box', 
'marvel mini hulk buster in display case 50mm x 50mm',
'home use display stand',
'Xiaomi note 17 for display only',
'camera display stand for display only',
"robot mug in display box",  

'cleaning the display',
'liquid display',
'Retina display',
'Asus 240 Hz display',

"crystal stud earrings clear display",             
"sample for display only",                
"shop display item",
"Display only toy truck" , # some problem for here 
"shop display Studio display",  
"for display Cover display",     
"LED display shop display",
"Cover display for display"]

# high probability words (first may be )]
#test case enhancement
is_product_dict={}

    
for t in test_cases:
    is_product_dict[t]= match_func(pattern.search(t)) 
print(is_product_dict)
# Could check number 2 dont skip the things that check 1 has already checked
print(f'The output of check number one is: ')
print()
print(dataframe(is_product_dict))
print("-"*30)

print("Check number 2")

false_keys = {k for k, v in is_product_dict.items() if not v}
for k in false_keys:
    is_product_dict[k]=check_display(k)
print()
print(f'The output of check number 2 is: ')
print()
print(dataframe(is_product_dict))

