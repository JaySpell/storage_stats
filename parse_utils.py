import json
import config
import datetime
import csv
import pprint
import pandas as pd

CURRENT_FILE = config.CURRENT_FILE
TIER_CONFIG = config.TIER_CONFIG
ARCHIVE_FILE = config.ARCHIVE_FILE
SVC_FILE = config.SVC_FILE
EXCEL_FILE = config.EXCEL_FILE

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

def convert_gb_tb(space_gb):
    space_TB = space_gb / 1024
    return int(space_TB)

def convert_byte_gb(space):
    space_GB = int(space) / 1024 / 1024 / 1024
    return str(space_GB).encode('utf-8')

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

def get_last_year(tos="tier"):
    #Get data from last year - ARCHIVE_FILE
    data_last_year = find_data_year_old()

    if tos == "tier":
        #Get info per tier
        r_stats = _get_stats(data_last_year)
    elif tos == "svc":
        #Get info per svc
        r_stats = _get_stats(data_last_year, tos='svc')

    return r_stats

def _get_stats(data_set, tos='tier', **kwargs):
    _return = {}

    if tos == 'tier':
        file_to_open = TIER_CONFIG
        _return = _get_tier_stats(data_set, file_to_open)
    elif tos == 'svc':
        file_to_open = SVC_FILE
        _return = _get_svc_stats(data_set, file_to_open)

    return _return

def _get_tier_stats(data_set, file_to_open):
    _return = {}

    with open(file_to_open, 'r') as open_json:
        tiers = json.load(open_json)

    for tier, storage in tiers['storage_tiers'].iteritems():
        _return[tier] = {}
        for row in data_set:
            _return = _get_data_tos(row, storage, tier, _return)

    return _return

def _get_svc_stats(data_set, file_to_open):
    _return = {}

    with open(SVC_FILE, 'r') as svc_json:
        svc = json.load(svc_json)

    s_data = []
    for a_svc, tiers in svc.iteritems():
        _return[a_svc] = {}
        for tier, storage in tiers.iteritems():
            for row in data_set:
                _return = _get_data_tos(row, storage, a_svc, _return)

    return _return

def _get_data_tos(row, storage, r_type, _return):
    name = row.split(',')[0]
    if name in storage:
        row_date = datetime.datetime.strptime(row.split(',')[1],
            "%Y-%m-%d")

        #If dict does not have the date of row already in return create
        #new row with date
        if row_date not in _return[r_type]:
            _return[r_type][row_date] = [
                row.split(',')[5], #used
                row.split(',')[3], #available
                row.split(',')[2]  #total
                ]

        #New data added to existing data within the dict for the storage
        #system and date [used, available, total]
        else:
            _return[r_type][row_date] = [
                float(_return[r_type][row_date][0]) +
                        float(row.split(',')[5]),
                float(_return[r_type][row_date][1]) +
                        float(row.split(',')[3]),
                float(_return[r_type][row_date][2]) + (
                            float(row.split(',')[2])
                        )
                ]

    return _return

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
    '''
    Function takes the output from SVC and combines it
    into the pool_history CSV file
    ARCHIVE_FILE (AF)
        mdisk_grp, date, total, avail, allocated, used, vol_cap, vol_used,
            assigned, unassigned, real_config, mdisk_avail, pool_#_mdisks,
            pool_#_vols
    CURRENT_FILE (CF)
        id, mdisk_grp, status, pool_#_mdisks, pool_#_vols, total, extent_size,
            avail, virt_cap, used, real_cap, overallocation, warning, easy_tier,
            compression, comp_virt_cap, comp_uncomp_cap, parent_mdisk_grp,
            parent_mdisk_grp_name, child_mdisk_grp, child_mdisk_grp_cnt,
            child_mdisk_grp_cap, type, encrypt
    -- Mappings ---
        AF[0] = CF[1]  = mdisk group name
        AF[1]          = date
        AF[2] = CF[5]  = total
        AF[3] = CF[7]  = available
        AF[4] = CF[7]  = allocated (used)
        AF[5] = CF[10] = used space
        AF[6] = CF[8]  = volume capacity
    '''
    current_date = datetime.date.today()
    first_day_month = current_date.replace(day=1)
    current_month_output = []

    with open(CURRENT_FILE, 'r') as cf:
        reader = csv.reader(cf)
        for row in reader:
            new_row = []
            if "mdisk_count" not in row:
                new_row = [
                        row[1] + "," +                   #mdisk group name
                        str(first_day_month) + "," +     #date
                        convert_byte_gb(row[5]) + "," +  #total
                        convert_byte_gb(row[7]) + "," +  #available
                        convert_byte_gb(row[7]) + "," +  #allocated
                        convert_byte_gb(row[10]) + "," + #used
                        convert_byte_gb(row[8]) + "," +  #vol capacity
                        ("0," * 8) + "0"                 #zero fill remaining
                    ]
            else:
                continue
            current_month_output.append(new_row)

    with open(ARCHIVE_FILE, 'a+') as af:
        for line in current_month_output:
            af.write(str(line[0]))
            af.write("\n")

def _create_excel(last_year):
    e_sheets = {}
    for group in last_year:
        for a_group, sheet in group.items():
            e_sheets[a_group] = {}
            for date, values in sheet.items():
                e_sheets[a_group][date] = {
                    'Free': values[0],
                    'Used': values[1],
                    'Total': values[2]
                }

    def add_tb_row(df):
        size_tb = lambda sizegb: sizegb / 1024
        for col in df:
            space_tb = []
            space_tb.append(map(size_tb, df[col]))
            df[col+'_In_TB'] = space_tb[0]
        return df

    writer = pd.ExcelWriter(EXCEL_FILE, engine='xlsxwriter')
    for group, sheet in e_sheets.items():
        sheet_name = group
        df = pd.DataFrame.from_dict(sheet)
        df = df.T
        df = add_tb_row(df)
        df.to_excel(writer, sheet_name=sheet_name)
    writer.save()
