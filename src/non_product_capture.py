# Part 1 預處理整個Description欄位
from rapidfuzz import process, fuzz
import re


def normalize_text(s):
    if pd.isna(s):
        return s
    s = str(s)
    s = s.lower().strip()                       #  Lowercase + Removing spaces at the front and back of the character
    s = re.sub(r'\s+', ' ', s)                  # Consecutive space -> A space 
    s = s.replace('\u00A0', ' ')                # Non-breaking white space -> normal spacing
    s = re.sub(r'[“”‘’`]', '"', s)             # Standardize quotation marks as double quotation mark (straight style)
    s = re.sub(r'[\u2013\u2014]', '-', s)       # Standardize the use of em dashes
    s = re.sub(r'[^\w\s\-\']+', ' ', s)        #Turn all non character/ numbers/  Underscores / en dash / apostrophe -> a space
    s = re.sub(r'\s+', ' ', s).strip()           
    return s


#Function to evaluate the peformance of masks
def results(set1, set2):
    set1_diff=set(set1)-set(set2)
    set2_diff=set(set2)-set(set1)
    return set1_diff, set2_diff


def fuzz_catcher(cands):
    matches_dict={}
    for notes in notes_dict:
        #do it outside maybe in the each of the notes
        matches_dict[notes] = [
            (c, process.extractOne(c, notes_dict[notes], scorer=fuzz.partial_ratio)) # problem here c is checking a limited note 
            for c in cands
        ]
        print(f"The matchables for {notes} are : {matches_dict[notes]}")
    return matches_dict

#Turns a dictionary into an ordinary list 
def raw_list_converter(a):
    raw=[]
    for type in a.keys():
       for word in a[type]:
           raw.append(word[1][1])
    return raw


df['Desc_norm'] = df['Description'].apply(normalize_text)


#Part 2
#用已知keyword list做「邊界比對」(避免部分字串誤匹配)
#remember to check the keywordlist for fair comparison.

# 先escape你的keywords（你已經做了，但要注意大小寫與空白已被normalise）
keywordlist = [re.escape(normalize_text(k.lower())) for k in keywordlist]

# 把長的phrase放前面，短的字放後面，減少誤判（重要）
keywordlist = sorted(keywordlist, key=lambda x: -len(x))

pattern = r'\b(?:' + '|'.join(keywordlist) + r')\b'   # word boundaries
# 如果某些keyword含空白（phrase），上面仍可匹配，因為desc已經把多空白縮成1

mask = df['Desc_norm'].str.contains(pattern, regex=True, na=False)


#Part 3 若有pattern error或特殊符號導致錯誤

#確保pattern字串是合法的regex（你用re.escape已經大幅降低錯誤）。

#若仍出錯，直接先用 simple substring search（速度快、無regex副作用）：
pattern1_5 = r'|'.join(keywordlist)

#Non boundary checking
mask1_5 = df['Desc_norm'].str.contains(pattern1_5, regex=True, na=False)

#Evaluate the running conditions of mask1_5 and mask 1 whether mask 1 is the subset of mask 1_5

a,b=results(df[mask]['Desc_norm'].tolist(), df[mask1_5]['Desc_norm'].tolist())

print(f'Things only mask have: {a}')
print(f'Things only_mask1_5 have: {b}')


# Part 4 用fuzzy matching (fuzzywuzzy / rapidfuzz)，只在剩下未分類的小sample上跑：

#checking the results of each method:

cands1 = df.loc[~mask, 'Desc_norm'].value_counts().index[:1000] #Fuzz masked never catches things that mask 1 already have 
cands1_5 = df.loc[~mask1_5, 'Desc_norm'].value_counts().index[:1000] #Fuzz mask never catches things that mask 1_5 already have

raw_cands1=raw_list_converter(fuzz_catcher(cands1))
raw_cands1_5=raw_list_converter(fuzz_catcher(cands1_5))


a,b=results(df[mask]['Desc_norm'].tolist(), raw_cands1)

print(f'The words that only mask have is{a}')
print(f'The words that  mask with fuzz have more is:{b}')

a,b=results(df[mask1_5]['Desc_norm'].tolist(), raw_cands1)

print(f'The words that only mask1_5 have is{a}')
print(f'The words that  mask1_5 with fuzz have more is:{b}')

# calculate precision to decide which one preserves of each one manually
print(f'The wordlist of raw_cands 1 is {raw_cands1}')
print(f'The wordlist of raw_cands 1_5 is {raw_cands1_5}')

#Anything does the better one lacks using the results function
"""results(better one, old one)[0]"""

#add back to the 3 types list and merge to keywordlist and re-do
#Whereas the precision step and another mask will be removed


