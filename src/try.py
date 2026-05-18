

try:
    a=list(map(int, input("plese enter a list of numbers: ")))   
    assert len(a) < 4, "The list has exceed the maximum length of 4"
except AssertionError as e:
    print("The the list has exceeded maximum length  of 4")
else:
    print(f'This is mylist: {a}')