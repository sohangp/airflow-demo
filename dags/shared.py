# Files starting with upper-case character are pictures of a cat
def label_func(x):
    return "cat" if x[0].isupper() else "dog"