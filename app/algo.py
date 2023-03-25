# returns stock price difference between buying price to selling price
# TICKER,PER,DATE,TIME,OPEN,HIGH,LOW,CLOSE,VOL,OPENINT
# b - base price
def algo(data, d2, d1, s, u1, u2):

    win = float(u1 - s)
    loss = float(d1 - s)

    buy_triggered = False
    minute = 1

    result = 0

    for row in data:

        o = row["OPEN"]
        h = row["HIGH"]
        l = row["LOW"]
        c = row["CLOSE"]

        # "eveything happens in the same minute"
        if (h >= u1) and (l <= s):
            return loss

        # Only check for second and later minutes
        # if trigger and sell was within the same minute
        # and stop loss was not triggered
        if minute < 1:
            minute += 1
            continue

        if (h >= u2) and (l > s):
            return win

        # case 1, going up, buy at u1, sell at u2
        if h >= u1:
            buy_triggered = True

        if buy_triggered and l > s:
            result = c - u1

        if buy_triggered and l <= s:
            return loss

    # by default, return 1/4th of atr
    return result
