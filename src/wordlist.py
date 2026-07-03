# Part 1 預處理整個Description欄位


import re

def normalize_text(s):
    if pd.isna(s):
        return s
    s = str(s)
    s = s.lower().strip()                       # 小寫 + 去頭尾
    s = re.sub(r'\s+', ' ', s)                  # 多空白 -> 1個
    s = s.replace('\u00A0', ' ')                # 非斷行空白 -> 一般空白
    s = re.sub(r'[“”‘’`]', '"', s)             # 統一單雙引號
    s = re.sub(r'[\u2013\u2014]', '-', s)       # 長破折號統一
    s = re.sub(r'[^\w\s\-\']+', ' ', s)         # 非字元/數字/底線/破折號/撇號 -> 空白
    s = re.sub(r'\s+', ' ', s).strip()
    return s

df['Desc_norm'] = df['Description'].apply(normalize_text)


#Part 2
#用已知keyword list做「邊界比對」(避免部分字串誤匹配)

# 先escape你的keywords（你已經做了，但要注意大小寫與空白已被normalise）
keywordlist = [re.escape(normalize_text(k.lower())) for k in keywordlist]

# 把長的phrase放前面，短的字放後面，減少誤判（重要）
keywordlist = sorted(keywordlist, key=lambda x: -len(x))

pattern = r'\b(?:' + '|'.join(keywordlist) + r')\b'   # word boundaries
# 如果某些keyword含空白（phrase），上面仍可匹配，因為desc已經把多空白縮成1

mask = df['desc_norm'].str.contains(pattern, regex=True, na=False)
non_product_df = df[mask]

#Part 3 若有pattern error或特殊符號導致錯誤

#確保pattern字串是合法的regex（你用re.escape已經大幅降低錯誤）。

#若仍出錯，直接先用 simple substring search（速度快、無regex副作用）：
pattern1_5 = r'|'.join(keywordlist)

#Non boundary checking
mask1_5 = df['desc_norm'].str.contains(pattern1_5, regex=True, na=False)



#mask 2 is never used in this code what is the use of it?

# Part 4 用fuzzy matching (fuzzywuzzy / rapidfuzz)，只在剩下未分類的小sample上跑：

from rapidfuzz import process, fuzz

#mask 1 and mask 2 then compare

cands1 = df.loc[~mask, 'desc_norm'].value_counts().index[:1000] 
cands1_5 = df.loc[~mask1_5, 'desc_norm'].value_counts().index[:1000] 
matches_type = {}

def fuzz_catcher(cands):
    for notes in notes_dict:
        notes_dict[notes] = list(map(normalize_text, notes_dict[notes]))
        matches_list_type[notes] = [
            (c, process.extractOne(c, notes_dict[notes], scorer=fuzz.partial_ratio))
            for c in cands
        ]
        print(f"The matchable for {notes} is: {matches_list_type[notes]}")
        return matches_type
    
print(fuzz_catcher(cands1))
print(fuzz_catcher(cands1_5))
final_candidates=set(fuzz_catcher(cands1))-set(fuzz_catcher(cands1_5))
print(final_candidates)