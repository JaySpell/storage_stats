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
    '''print all_tiers_totals
    chart_values = {'ids':  }

    for tier in all_tiers_json.items():
        chart_utils.donutchart(chart_values)
    '''

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

    '''
    Create growth charts
    '''

    #Get last years information
    last_year = parse_utils.get_last_year()

    #Parse data
    for tier_name, dates in last_year.iteritems():
        #Sort by date
        all_dates = sorted(dates.keys())
        used_space = []

        #Get used space
        for date in sorted(dates):
            used_space.append(dates[date][0])

        #Convert to TB from the GB
        used_space = map(parse_utils.convert_gb_tb, used_space)

        #Create growth charts using data
        chart_utils.growthchart(tiername=tier_name,
                    dates=all_dates, used=used_space)


    #Render output in jinja2
    t = env.get_template('tiers.html').render(tiers=tier_output)

    #Open output file / insert new content into output file
    with open(OUTPUT_FILE, 'w') as o_file:
        o_file.write(t)

if __name__ == "__main__":
    create_charts()
