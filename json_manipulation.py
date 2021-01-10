import json
d = []
for i in range(10):
    with open(str(i)+".json", "r", encoding="utf-8") as f:
        d.append(json.loads(f.read()))
json_list = []
for category0 in d:
    for key1, value1 in category0.items():
        category0_child = list()
        for key2, value2 in value1.items():
            category1_child = list()
            for key3, value3 in value2.items():
                category2_child = list()
                if len(value3) < 1:
                ## sol1
                    category1_child.append({"category2_name": key3, "category2_child": category2_child})
                    continue
                for category3 in value3:
                    category2_child.append({"category3_name": category3})
                ## sol1
                category1_child.append({"category2_name": key3, "category2_child": category2_child})
            category0_child.append({"category1_name": key2, "category1_child": category1_child})
        json_list.append({"category0_name": key1, "category0_child": category0_child})

with open("json_list.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(json_list, ensure_ascii=False))