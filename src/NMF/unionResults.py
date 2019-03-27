import json

def main(files):
    """
    union the results for each individual result

    @param: files: type, array of strings, which are the json file paths for each individual test dataset
    return: None
    """
    submission = []
    for file in files:
        with open(f, 'r') as f:
            submission += json.load(f)
    
    with open('submission.json', 'w') as f:
        f.write(json.dumps(submission))

if __name__ == '__main__':
    files = [

    ]
    main(files)