from collections import Counter
from wordscore import score_word

def run_scrabble(rack: str):
    """
    Given a Scrabble rack (2-7 characters, uppercase/lowercase letters,
    and up to one '*' and one '?'), return a tuple:
    (
      [(score, WORD), (score, WORD), ...],  # All valid words you can form
      total_number_of_words
    )

    The list is sorted by descending score, then by alphabetical order.
    Return (list_of_tuples, count_of_valid_words)
    """
    rack = rack.strip()
    if len(rack) < 2 or len(rack) > 7:
        return ("Error: the number of tiles must be between 2 and 7"
                f"You provided {len(rack)} tiles")

    # Convert rack to uppercase for consistency
    rack_upper = rack.upper()

    # Count wildcards: up to one *, up to one ?
    star_count = rack_upper.count('*')
    quest_count = rack_upper.count('?')
    total_wildcards = star_count + quest_count

    # Check the total wildcards restriction, must be <= 2, and can only have 1 * and 1 ?
    if star_count > 1 or quest_count > 1 or total_wildcards > 2:
        return ("ERROR: You may use at most one '*' and at most one '?' "
                f"Detected {star_count} '*' and {quest_count} '?'")

    # Check that all characters are valid: A-Z or * or ?
    for ch in rack_upper:
        if not (ch.isalpha() or ch in ['*', '?']):
            return ("ERROR: Invalid character detected. Only letters, '*' or "
                    "'?' are allowed. Found: " + ch)

    # 2. Build a frequency map of the letters
    rack_counter = Counter()
    wildcard_count = 0

    for ch in rack_upper:
        if ch == '*' or ch == '?':
            wildcard_count += 1
        else:
            rack_counter[ch] += 1

    # 3. Read all possible english scrabble words from sowpods.txt
    with open("sowpods.txt","r") as infile:
        raw_input = infile.readlines()
        data = [datum.strip('\n') for datum in raw_input]

    # 4. Function to check if a word can be formed and return the best possible score
    def can_form_and_score(word):
        """
        Check if 'word' can be formed from rack_counter + wildcard_count
        Return the best possible score if yes, else -1
        """
        from copy import deepcopy

        temp_counter = deepcopy(rack_counter)
        wc = wildcard_count
        temp_score = 0

        for letter in word:
            if temp_counter[letter] > 0:
                # Use a real letter
                temp_counter[letter] -= 1
                temp_score += score_word(letter) # add letter value
            else: # Use a wildcard, if available
                if wc > 0:
                    wc -= 1 # wildcard scores 0
                else:
                    return -1  # cannot form the word at all

        return temp_score

    # 5. Find all valid words that can be formed
    from collections import defaultdict
    best_scores = defaultdict(int)  # word -> best_score

    # Only look at words up to length = len(rack), since we can't form longer words than the number of tiles
    max_length = len(rack_upper)

    for w in data:
        word_upper = w.upper() # ensure uppercase

        if len(word_upper) <= max_length:
            score_val = can_form_and_score(word_upper)
            if score_val > -1:
                # Keep only the highest score for this word
                if score_val > best_scores[word_upper]:
                    best_scores[word_upper] = score_val

    # 6. Sort results: descending by score, then alphabetical
    # best_scores is a dict {WORD: score}
    scored_words = [(v, k) for k, v in best_scores.items()] # convert to list of (score, WORD)

    # Sort by (-score, then word), alphabetical words
    scored_words.sort(key=lambda x: (-x[0], x[1]))

    # 7. Build final result
    total_valid = len(scored_words)
    return (scored_words, total_valid) # return tuple
