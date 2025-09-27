import json


class JsonHandler:
    def __init__(path):
        self.path = path
        print(path)

    # with open("documentation/data.json", "r", encoding="utf-8") as f:
    #     print(json.load(f))


data = JsonHandler("documentation/data.json")