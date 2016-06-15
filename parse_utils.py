import json
import config
import datetime

CURRENT_FILE = config.CURRENT_FILE
TIER_CONFIG = config.TIER_CONFIG
ARCHIVE_FILE = config.ARCHIVE_FILE
SVC_FILE = config.SVC_FILE

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

def storage_total(storage, current_file):
    free_total = int(0)
    used_total = int(0)
    space_total = int(0)
    f_total = []
    u_total = []
    s_total = []

    with open(current_file) as a_file:
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

def growth_data():
    pass

def get_last_year():
    #Get data from last year - ARCHIVE_FILE
    data_last_year = find_data_year_old()

    #Get info per SVC
    svc_stats = _get_svc_stats(data_last_year)

    #Get info per tier
    tier_stats = _get_tier_stats(data_last_year)

    last_year = {"last_year": [
                    {"svc": svc_stats},
                    {"tier": tier_stats}
                ]}

    if return_type == "tier":
        return "tier"
    elif return_type == "svc":
        return "svc"
    else:
        return "Invalid return type.."

def _get_svc_stats(data_set):
    '''with open(SVC_FILE, 'r') as svc_json:
        svc = json.load(svc_json)
        for '''

def _get_tier_stats(data_set):
    tier_return = []

    with open(TIER_CONFIG, 'r') as tier_json:
        tiers = json.load(tier_json)
        t_data = []
        for tier in tiers['storage_tiers'].iteritems():
            for a_tier in tier[1]:
                for row in data_set:
                    name = row.split(',')[0]
                    if name in a_tier:
                        t_data.append(row)
                tier_return.append(t_data)
    return tier_return

def find_data_year_old(filename=ARCHIVE_FILE):
    r_data = []
    with open(filename, 'r') as a_file:
        for line in a_file:
            lsplit = line.split(',')
            time = lsplit[1]
            if _is_year_old(time):
                r_data.append(line)
    s_data = sorted(r_data,
            key = lambda row: datetime.datetime.strptime(row.split(',')[1],
                    "%Y-%m-%d"))
    return s_data

def _is_year_old(str_date):
    today = datetime.date.today()
    first = today.replace(day=1)
    lastyear = first - datetime.timedelta(days=365)
    l_date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    c_date = datetime.datetime(lastyear.year, lastyear.month, lastyear.day)
    if l_date >= c_date:
        return True
    else:
        return False

def add_data_archive(a_file=ARCHIVE_FILE, c_file=CURRENT_FILE):
    pass
