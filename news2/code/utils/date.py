def choice_date(date):
    date_lst = date.split()
    if len(date_lst) == 0:
        return 0
    month = date_lst[0]
    year = date_lst[2]
    if year == "2020" and month == "July" or month == "Jul" :
        return 1
    return 0