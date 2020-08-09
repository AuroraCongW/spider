def join_list(lst):
    length = len(lst)
    if length == 0 :
        return ""
    elif length == 1 :
        return lst[0]
    else:
        return "".join(lst)