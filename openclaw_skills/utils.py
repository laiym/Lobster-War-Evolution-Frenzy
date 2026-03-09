import json

def dict_to_json(d):
    return json.dumps(d, ensure_ascii=False)

def json_to_dict(s):
    return json.loads(s) if s else {}
