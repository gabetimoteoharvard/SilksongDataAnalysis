import json
from data_scrape import make_json_file

def process(string):
    """Remove symbols and punctuation from string"""

    symbols = (',', '.', '?', '/', '!')

    new_str = ''
    for ch in string:
        if ch not in symbols:
            new_str += ch
    return new_str  

def get_double_word_json():
    double_word_frequency = {} # structure - 'word1 word2' : {'total': int, 'negative': int, 'positive': int}

    try:
        with open('skong', 'r') as f:
            data = json.load(f)

        for review in data["reviews"]:
            text = review["review"]
            positive = review["voted_up"]

            repetition_set = set()

            wrds = process(text).split()
            for i in range(len(wrds) - 1):
                double_word = f'{wrds[i]} {wrds[i + 1]}'.lower()
                if double_word not in repetition_set:
                    repetition_set.add(double_word)

                    if double_word not in double_word_frequency:
                        double_word_frequency[double_word] = {'total': 1, 'negative': 0, 'positive': 0}
                    else:
                        double_word_frequency[double_word]['total'] += 1
                    
                    if positive:
                        double_word_frequency[double_word]['positive'] += 1
                    else:
                        double_word_frequency[double_word]['negative'] += 1

        
    except Exception as e:
        print(f'Error processing file: {e}')

    filtered_ = dict(filter(lambda x: x[1]['total'] >= 1000, double_word_frequency.items()))
    make_json_file(filtered_, filename="double_word_data")

def main():
    return

if __name__ == "__main__":
    main()