import json


def parseJSON(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    print(data["maps"])
if __name__ == "__main__":
    filename = "testjson.json"
    parseJSON(filename)