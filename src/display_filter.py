import re

pattern = re.compile(
    r'\bdisplay\b(?!\s*(box|case|stand|only)\b)',  # display 後面不是 box/case/stand/only
    re.IGNORECASE
) # what is * in regex?

test_cases = [
    "crystal stud earrings clear display",   # 應該不算 operational（display 前是 clear，形容包裝）
    "robot mug in display box",               # display box → 排除
    "sample for display only",                # display only → 這個才是真正 operational
    "shop display item",                      # shop display → operational
]

for t in test_cases:
    match = pattern.search(t)
    print(t, "->", "match" if match else "no match")


whitelist_pattern = re.compile(r'\b(display box|display case|clear display|display stand)\b', re.IGNORECASE)
operational_pattern = re.compile(r'\b(display only|shop display|for display)\b', re.IGNORECASE)

def check_display(text):
    if operational_pattern.search(text):
        return "operational"
    elif whitelist_pattern.search(text):
        return "normal product"
    elif re.search(r'\bdisplay\b', text, re.IGNORECASE):
        return "需人工確認"  # 落入灰色地帶
    return "no match"

for t in test_cases:
    print(t, "->", check_display(t))