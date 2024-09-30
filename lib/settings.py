import json


def get_settings() -> dict:
    settings_obj = None

    with open('./settings.json', 'r') as f:
        set_json_txt = f.read()
        #print(set_json_txt)
        settings_obj = json.loads(set_json_txt)
        print('done')

    return settings_obj
