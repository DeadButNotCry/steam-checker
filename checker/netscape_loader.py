def normal_format(cookie):
    lines = cookie.split("\n")
    res = ""
    for line in lines:
        values = line.split("\t")
        res += f"{values[-2]}={values[-1]}; "
    return res

