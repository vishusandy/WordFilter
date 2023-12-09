def tier(word: str, weight: list[str]) -> list[float]:
    m = float(pow(2, len(weight)) - 1.0)  # max rank
    print(f"{m=}")
    rank = 0.0  # tier rank
    w = 0.0  # weight (% contained in each tier)
    p = 0  # previous tier
    for i, chars in enumerate(weight):
        ws = [c in chars for c in word]
        if any(ws):
            t = pow(2, i)
            r = t / m  # tier percentage
            rank += r
            percent = ws.count(True) / len(word)
            w += (r - p) * percent + p
            print(f"tier {i}: {p=} {t=} {r=} {percent=} w{i}={ (r - p) * percent + p}")
            p = t
    return [rank, w]


kb0 = "aoeuhtns"
kb1 = "id"
kb2 = "',.pgcrl"
kb3 = "yf"
kb4 = ";qjkmwvz"
kb5 = "xb"
kb = [kb0, kb1, kb2, kb3, kb4, kb5]




tier("apple", kb[0:3])
tier("ypplc", kb[0:3])
tier("hone", [kb0])
tier("hone", kb[0:2])
