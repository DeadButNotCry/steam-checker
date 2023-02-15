def str_format(cookie):
    lines = cookie.split("\n")
    res = ""
    for line in lines:
        if line != '':
            values = line.split("\t")
            res += f"{values[-2]}={values[-1]}; "
    return res


def json_cookies(cookie):
    lines = cookie.split("\n")
    res = []
    for line in lines:
        if line != '':
            values = line.split("\t")
            res.append({
                "name": values[-2],
                "value": values[-1],
                "domain": "steamcommunity.com",
                "SameSite": None
            })
    return res
