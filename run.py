import parse_utils
import chart_utils
import json
import os

TIER_CONFIG = '/home/kcup/python/graph/json/tier.json'


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
        all_tiers_totals[tiers[0]] = parse_utils.storage_total(tiers[1])

    #Convert to percentages
    all_tiers_percents = {}
    for tiers in all_tiers_totals.iteritems():
        all_tiers_percents[tiers[0]] = parse_utils.space_percent(tiers[1])

    #Create charts
    for tier in all_tiers_percents.iteritems():
        chart_utils.piechart(tier[1], title=tier[0])

if __name__ == "__main__":
    create_charts()