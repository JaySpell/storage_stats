CURRENT_FILE = "/home/kcup/python/graph/output"

def group_totals(strg_list):
    free_total = int(0)
    used_total = int(0)
    space_total = int(0)
    f_total = []
    u_total = []
    s_total = []

    for str_sys in strg_list:
        a_file = str_file_open()
        for line in a_file:
            lsplit = line.split(',')
            if lsplit[1] in str_sys:
                free_total = int(free_total) + int(lsplit[7])
                used_total = int(used_total) + int(lsplit[9])
                space_total = free_total + used_total
        f_total.append(free_total)
        u_total.append(used_total)
        s_total.insert(0, space_total)
        a_file.close()
    r_totals = {'free': [sum(f_total)],
            'used': [sum(u_total)],
            'space': [sum(s_total)]}
    return r_totals

def space_percent(r_totals):
    s_totals = r_totals['space'][0]
    r_percent = lambda x: float(x)/float(s_totals)

    n_list = map(r_percent, r_totals['free'])
    r_totals['free'] = n_list.pop(0)

    n_list = map(r_percent, r_totals['used'])
    r_totals['used'] = n_list.pop(0)

    return r_totals

def str_file_open(current_file=CURRENT_FILE):
    a_file = open(current_file, 'r')
    return a_file

def convert_to_tb(space_bytes):
    space_TB = space_bytes / 1024 / 1024 / 1024 / 1024
    return space_TB
