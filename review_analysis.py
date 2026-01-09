import json
from data_scrape import make_json_file

def process(string: str):
    """Remove symbols and punctuation from string"""

    symbols = (',', '.', '?', '/', '!')

    new_str = ''
    for ch in string:
        if ch not in symbols:
            new_str += ch
    return new_str  

def get_num_word_json(num: int, threshold: int, name: str):
    """Gets file of data of 'num' consecutive words in review data that are present in at
    least 'threshold' reviews"""

    word_frequency = {} # structure - 'word_1 word_2 ... word_num' : {'total': int, 'negative': int, 'positive': int}

    try:
        with open('skong', 'r') as f:
            data = json.load(f)

        for review in data["reviews"]:
            text = review["review"]
            positive = review["voted_up"]

            repetition_set = set()

            wrds = process(text).split()
            for i in range(len(wrds) - num + 1):
                num_word = ''
                for j in range(i, i + num):
                    num_word += f'{wrds[j]} '
                num_word = num_word.strip().lower()

                if num_word not in repetition_set:
                    repetition_set.add(num_word)

                    if num_word not in word_frequency:
                        word_frequency[num_word] = {'total': 1, 'negative': 0, 'positive': 0}
                    else:
                        word_frequency[num_word]['total'] += 1
                    
                    if positive:
                        word_frequency[num_word]['positive'] += 1
                    else:
                        word_frequency[num_word]['negative'] += 1

        
    except Exception as e:
        print(f'Error processing file: {e}')

    filtered_ = dict(filter(lambda x: x[1]['total'] >= threshold, word_frequency.items()))
    make_json_file(filtered_, filename=name)


def main():
    return

if __name__ == "__main__":
    main()