def tier(word: str, weight: list[str]) -> list[float]:
    print(f"tiers: {len(weight)}")

    m = float(pow(2, len(weight)) - 1.0)  # max rank
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
            print(f"  tier {i}: {rank=} {r=} {t=} {percent=}")
            # w += (r - p) * percent + p
            w += r * percent
            p = t
    return [rank, w]


kb0 = "aoeuhtns"
kb1 = "id"
kb2 = "',.pgcrl"
kb3 = "yf"
kb4 = ";qjkmwvz"
kb5 = "xb"
kb = [kb0, kb1, kb2, kb3, kb4, kb5]


print(tier("apple", kb[0:3]))
print("\n")
print(tier("ypplc", kb[0:3]))
print("\n")
print(tier("hone", [kb0]))
print("\n")
print(tier("hone", kb[0:2]))
print("\n")
