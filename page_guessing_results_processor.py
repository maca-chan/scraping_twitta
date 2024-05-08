from csv import DictReader
from re import search
from sys import argv


pages_count = 0


def get_results_dict(dictReader):
    results = {}

    for row in dictReader:
        results_row = {}
        message = row["Content"]
        number_match = search(r'[\d]+', message)
        
        if not number_match:
            continue

        timestamp = row["Timestamp"]
        results_row["guess"] = int(number_match.group())
        results_row["message"] = message
        results_row["timestamp"] = timestamp

        results[(row["Handle"], timestamp)] = results_row

    return results


def sorting_scoring_function(item):
    return abs(item[1]["guess"] - pages_count)


# Requires Python 3.7+ to keep insertion order
def sort_results_by_guess(results):
    return {k: v for k, v in 
            sorted(results.items(), 
                   key=sorting_scoring_function)}


def format_results(results):
    return "\n".join(
        [f"{k[0]}: {v['guess']} - ({v['message']} [{v['timestamp']}])" 
         for k, v in list(results.items())[:5]])


def main():
    global pages_count
    if len(argv) != 3:
        print("Usage: python page_guessing_results.py <pages_count> <results_csv>")
        return

    pages_count = int(argv[1])
    dictReader = DictReader(open(argv[2], "r", encoding="utf-8"))

    print(
        format_results(
            sort_results_by_guess(
                get_results_dict(dictReader))))


if __name__ == "__main__":
    main()