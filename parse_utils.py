import json

CURRENT_FILE = "/home/kcup/python/graph/output"

def group_totals(storage):
    free_total = int(0)
    used_total = int(0)
    space_total = int(0)
    f_total = []
    u_total = []
    s_total = []

    for storage_system in storage:
        a_file = str_file_open()
        for line in a_file:
            lsplit = line.split(',')
            if lsplit[1] in storage_system:
                free_total = int(free_total) + int(lsplit[7])
                used_total = int(used_total) + int(lsplit[9])
                space_total = free_total + used_total
        f_total.append(free_total)
        u_total.append(used_total)
        s_total.insert(0, space_total)
        a_file.close()
    all_totals = {'free': [sum(f_total)],
            'used': [sum(u_total)],
            'space': [sum(s_total)]}
    return all_totals

def storage_total(storage):
    free_total = int(0)
    used_total = int(0)
    space_total = int(0)
    f_total = []
    u_total = []
    s_total = []

    with open(CURRENT_FILE) as a_file:
        for line in a_file:
            lsplit = line.split(',')
            if lsplit[1] in storage:
                free_total = int(free_total) + int(lsplit[7])
                used_total = int(used_total) + int(lsplit[9])
                space_total = free_total + used_total
        f_total.append(free_total)
        u_total.append(used_total)
        s_total.insert(0, space_total)
        all_totals = {'free': [sum(f_total)],
                'used': [sum(u_total)],
                'space': [sum(s_total)]}
    return all_totals

def space_percent(all_totals, sel_out="dict", sub_output_type="list"):
    '''
    Takes the list of values and returns the % value.
    Input should be a dict with the following
    {
        'used': [used_float],
        'free': [free_float],
        'space': [total of the two]
    }
    '''
    s_totals = all_totals['space'][0]

    if not s_totals == 0:
        r_percent = lambda x: float(x)/float(s_totals)
        n_list = list(map(r_percent, all_totals['free']))
        all_totals['free'] = n_list.pop(0)
        n_list = list(map(r_percent, all_totals['used']))
        all_totals['used'] = n_list.pop(0)

    if sel_out == "list":
        rn_list = [
        all_totals['free'],
        all_totals['used'],
        ]
        all_totals = rn_list

    return all_totals

def str_file_open(current_file=CURRENT_FILE):
    a_file = open(current_file, 'r')
    return a_file

def convert_to_tb(space_bytes):
    space_TB = space_bytes / 1024 / 1024 / 1024 / 1024
    return space_TB

def parse_storage_csv(storage_systems, file_to_parse=CURRENT_FILE,
    output_type='dict'):
    open_file = open(file_to_parse, 'r')
    storage_sys_total = {}

    for storage_system in storage:
        for line in open_file:
            lsplit = line.split(',')
            if lsplit[1] in storage_system:
                storage_sys_total[storage_system] = {
                        'name': storage_system,
                        'free': int(lsplit[7]),
                        'used': int(lsplit[9]),
                        'space': sum(int(lsplit[7] + int(lsplit[9])))
                        }
    open_file.close()

    if ouput_type == "json":
        with open('storage_sys_total.json', 'w') as fp:
            json.dump(storage_sys_total, fp)

    return storage_sys_total
