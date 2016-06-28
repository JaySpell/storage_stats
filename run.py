import parse_utils
import chart_utils
import json
import os
import config
import re
from jinja2 import Template, Environment, FileSystemLoader
import pprint

#import config
TIER_CONFIG = config.TIER_CONFIG
CURRENT_FILE = config.CURRENT_FILE
OUTPUT_FILE = config.OUTPUT_FILE
TEMP_DIR = config.TEMP_DIR

#Setup jinja2 environement
env = Environment(loader=FileSystemLoader(TEMP_DIR),
                trim_blocks=True)

def create_charts(**kwargs):
    '''
    Function utilizes parse_utils & chart_utils to create charts..
    Required -- TIER_CONFIG (json) to parse / systems to create charts on
    Returns -- html version of charts
    '''

    with open(TIER_CONFIG) as json_data:
        storage_tiers = json.load(json_data)

    #Get the totals for all systems in tier
    all_tiers_totals = {}
    for tiers in storage_tiers['storage_tiers'].iteritems():
        all_tiers_totals[tiers[0]] = parse_utils.storage_total(tiers[1],
                CURRENT_FILE)

    #Convert to percentages
    all_tiers_percents = {}
    for tiers in all_tiers_totals.iteritems():
        all_tiers_percents[tiers[0]] = parse_utils.space_percent(tiers[1])

    '''Create pie charts'''
    for tier in all_tiers_percents.iteritems():
        chart_utils.piechart(tier[1], title=tier[0])

    #Create donut charts

    #Combine the html into the storage stats
    tier_output = []
    updated_output = []
    for tiername in storage_tiers['storage_tiers'].keys():
        inside_body = False
        open_file = tiername.replace(' ', '') + '.html'
        with open(open_file, 'r') as a_file:
            for line in a_file:
                if '<body>' in line or inside_body:
                    updated_output.append(line)
                    if '</body>' not in line: inside_body = True
                else: inside_body = False
        updated_output.pop(0)
        updated_output.pop(len(updated_output) - 1)
        tier_output.append(updated_output)
        updated_output = []


    #Create growth charts by tier
    tier_graphs = _get_growth_chart()

    #Create growth charts by svc
    svc_graphs = _get_growth_chart(return_type="svc")

    #Render output in jinja2
    t = env.get_template('tiers.html').render(
        tiers=tier_output,
        graphs=tier_graphs,
        svc=svc_graphs)

    #Open output file / insert new content into output file
    with open(OUTPUT_FILE, 'w') as o_file:
        o_file.write(t)


def _get_growth_chart(return_type="tier"):

    #Get last years information
    if return_type == "tier":
        last_year = parse_utils.get_last_year()
    elif return_type == "svc":
        last_year = parse_utils.get_last_year(tos="svc")
    else:
        return "Not valid return type.."

    #Parse data
    r_graphs = {}
    for a_name, dates in last_year.iteritems():
        #Sort by date
        all_dates = sorted(dates.keys())
        used_space = []

        #Get used space
        for date in sorted(dates):
            used_space.append(dates[date][0])

        #Convert to TB from the GB
        used_space = map(parse_utils.convert_gb_tb, used_space)

        #Create growth charts using data
        r_graphs[a_name] = chart_utils.growthchart(
                                    tiername=a_name.upper(),
                                    dates=all_dates,
                                    used=used_space)

    return r_graphs

if __name__ == "__main__":
    create_charts()
    parse_utils.add_data_archive()
