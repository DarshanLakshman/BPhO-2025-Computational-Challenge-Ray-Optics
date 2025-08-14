def get_colour(f):
    f = f / (10 ** 12)
    if f < 405:
        return 0, 0, 0
    elif 405 <= f < 480:
        t = (f - 405) / 75
        return t, 0, 0
    elif 480 <= f < 510:
        t = (f - 480) / 30
        return 1, 0.5 * t, 0
    elif 510 <= f < 530:
        t = (f - 510) / 20
        return 1, 0.5 + 0.5 * t, 0
    elif 530 <= f < 600:
        t = (f - 530) / 70
        return 1 - t, 1, 0
    elif 600 <= f < 620:
        t = (f - 600) / 20
        return 0, 1, t
    elif 620 <= f < 680:
        t = (f - 620) / 60
        return 0, 1 - t, 1
    elif 680 <= f <= 790:
        t = (f - 680) / 110
        return 0.5 * t, 0, 1
    else:
        return 0, 0, 0