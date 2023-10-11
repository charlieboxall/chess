def inverse_mapping(f):
    return f.__class__(map(reversed, f.items()))

translate_rows = {
    "1" : 7,
    "2" : 6,
    "3" : 5,
    "4" : 4,
    "5" : 3,
    "6" : 2,
    "7" : 1,
    "8" : 0,
}
reversed_translate_rows = inverse_mapping(translate_rows)

translate_cols = {
    "a" : 0,
    "b" : 1,
    "c" : 2,
    "d" : 3,
    "e" : 4,
    "f" : 5,
    "g" : 6,
    "h" : 7,
}
reversed_translate_cols = inverse_mapping(translate_cols)

