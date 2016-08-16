import parse_utils
import chart_utils
import datetime
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

    #Create % growth area


    #Render output in jinja2
    t = env.get_template('tiers.html').render(
        tiers=tier_output,
        graphs=tier_graphs,
        svc=svc_graphs)

    #Open output file / insert new content into output file
    with open(OUTPUT_FILE, 'w') as o_file:
        o_file.write(t)

def _get_growth_chart(return_type="tier"):
    """creates growth charts

    Creates a set of bokeh charts utilizing the data from the last year
    that is pulled utilizing parse_utils.get_last_year -- chart_utils is then
    used to take that data and create bokeh charts

    Args:
        return_type: either 'tier' or 'svc' can be passed

    Returns:
        A dict with keys mapping to either tier or svc name and the values
        containing the bokeh charts which are based on div / jscript
    """

    #Get last years information using get_last_year from parse_utils
    if return_type == "tier":
        last_year = parse_utils.get_last_year()
    elif return_type == "svc":
        last_year = parse_utils.get_last_year(tos="svc")
    else:
        return "Not valid return type.."

    COLOR_FILE = config.COLOR_FILE
    with open(COLOR_FILE, 'r') as colors_json:
        colors = json.load(colors_json)

    #Parse data
    r_graphs = {}
    for a_name, dates in last_year.iteritems():
        #Sort by date
        all_dates = sorted(dates.keys())
        used_space = []
        total_space = []

        #Get used space
        for date in sorted(dates):
            used_space.append(dates[date][0])
            total_space.append(dates[date][2])

        #Convert to TB from the GB
        used_space = map(parse_utils.convert_gb_tb, used_space)
        total_space = map(parse_utils.convert_gb_tb, total_space)

        #Create growth charts using data
        r_graphs[a_name] = chart_utils.growthchart(
                                    tiername=a_name.upper(),
                                    dates=all_dates,
                                    used=used_space,
                                    total=total_space,
                                    colors=colors)

    return r_graphs

def _percent_growth(return_type='tier'):
    r_percents = {}

    #Data from last year
    data_last_year = parse_utils.get_last_year(tos=return_type)

    #Get dates
    today = datetime.date.today()
    first = today.replace(day=1)
    today_format = datetime.datetime.strptime(
            first.strftime("%Y-%m-%d"), "%Y-%m-%d"
        )
    lastyear = first - datetime.timedelta(days=182)
    lastyear_format = datetime.datetime.strptime(
            lastyear.strftime("%Y-%m-%d"), "%Y-%m-%d"
        )


    for a_name in data_last_year.iterkeys():
        print "Data last year %d" % data_last_year[a_name][today_format][0]
        print "Data this year %d" % data_last_year[a_name][lastyear_format][0]
        diff = float(
                data_last_year[a_name][today_format][0] -
                data_last_year[a_name][lastyear_format][0]
            )
        print "Difference %d" % diff
        percent = float(diff / data_last_year[a_name][today_format][0])
        print "Percent change %f" % percent
        r_percents[a_name] = percent

    return r_percents

if __name__ == "__main__":
    #create_charts()
    pass
