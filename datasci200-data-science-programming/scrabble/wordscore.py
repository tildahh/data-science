def score_word(word: str) -> int:
    '''
    takes each word and returns the score
    based on the scrabble letter dictionary of scores
    '''
    scores = {
            "a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
            "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
            "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
            "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
            "x": 8, "z": 10
    }
    score = 0
    for char in word:
        char_lower = char.lower()
        if char_lower in scores:
            score += scores[char_lower]
    return score