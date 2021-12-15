import requests
import json
from pathlib import Path
import os
import threading


def get_gift_codes():
    cash_gift_dict = {}
    gift_dict = {}
    gift_effects_dict = {}

    cash_gift_json = requests.get(
        'https://open.douyucdn.cn/api/RoomApi/room/520').text
    gift_effects_json = requests.get(
        'https://webconf.douyucdn.cn/resource/common/gift/flash'
        '/gift_effect.json').text
    gift_json = requests.get(
        'https://webconf.douyucdn.cn/resource/common/prop_gift_list'
        '/prop_gift_config.json').text

    gift_effects_json = gift_effects_json.replace('DYConfigCallback(', '')[0:-2]
    gift_json = gift_json.replace('DYConfigCallback(', '')[0:-2]
    cash_gift_json = json.loads(cash_gift_json)['data']['gift']
    gift_effects_json = json.loads(gift_effects_json)['data']['flashConfig']
    gift_json = json.loads(gift_json)['data']

    # reformat
    # without json.replace this object is a list
    for i in range(len(cash_gift_json)):
        cash_gift_dict[str(cash_gift_json[i]['id'])] = {
            'code': cash_gift_json[i]['id'],
            'name': cash_gift_json[i]['name'],
            'exp': cash_gift_json[i]['gx'],
            'effect_code': 0
        }

    for gift in gift_effects_json:
        gift_effects_dict[gift] = {
            'effect_code': gift,
            'effect_name': gift_effects_json[gift]['name']
        }

    for gift in gift_json:
        gift_dict[gift] = {
            'code': gift,
            'name': gift_json[gift]['name'],
            'exp': gift_json[gift]['exp'],
            'effect_code': gift_json[gift]['effect'],
        }

    # merge two gift dicts
    gift_all_dict = cash_gift_dict | gift_dict

    # compare if name from props dict vary from effects
    # TODO - validate if this step is necessary
    res = {}
    res_vary = {}

    for gift in gift_all_dict:
        code = gift_all_dict[gift]['code']
        name = gift_all_dict[gift]['name']
        exp = gift_all_dict[gift]['exp']
        code_effect = gift_all_dict[gift]['effect_code']
        if code_effect != 0:
            name_from_effect = gift_effects_dict[str(code_effect)][
                'effect_name']
        else:
            name_from_effect = 'No Effects'

        # reconstruct
        if name == name_from_effect or name_from_effect == 'No Effects':
            res[gift] = {
                'code': code,
                'name': name,
                'exp': exp,
                'effect_code': code_effect,
                'effect_name': name_from_effect
            }
        else:
            res_vary[gift] = {
                'code': code,
                'name': name,
                'exp': exp,
                'effect_code': code_effect,
                'effect_name': name_from_effect
            }

    return res, res_vary


def construct_config_file(res: tuple, path: str):
    # read original config file
    raw = Path(path).read_text()
    split_raw = raw.splitlines()

    # initialise array&dict instance
    original = {}
    arr_code = []
    arr_name = []
    arr_exp = []

    for txt in split_raw:
        single = txt.split(',')
        arr_code.append(single[0])
        arr_name.append(single[1])
        arr_exp.append(single[2])

    # reconstruct dict from raw for comparison
    if all(length == len(arr_code) for length in [len(arr_name), len(arr_exp)]):
        for i in range(len(arr_code)):
            original[str(arr_code[i])] = {
                'code': arr_code[i],
                'name': arr_name[i],
                'exp': arr_exp[i]
            }
    else:
        raise RuntimeError('原配置文件输入数组长度不一致')

    # retrieve from tuple index 0
    fetched_gifts = res[0]

    # iterate through local config to see if there is a mismatch
    # if there is, move conflict items to a new dict
    conflict = {}
    for gift in original:
        if gift in fetched_gifts:
            if original[gift]['code'] == fetched_gifts[gift]['code'] and \
                    original[gift]['name'] != fetched_gifts[gift]['name']:
                conflict[gift] = {
                    'local': original[gift],
                    'remote': fetched_gifts[gift]
                }
                del original[gift]
                del fetched_gifts[gift]

    # if len(conflict) == 0:

    print('test')

    with open('test_text/codes.txt', 'w') as file:
        file.write('test')


if __name__ == '__main__':
    construct_config_file(get_gift_codes(), 'test_text/raw.txt')
