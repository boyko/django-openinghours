
from itertools import groupby

# Facebook rule format


def parse_rule(rule, value):
    day, nr, verb = rule.split('_')

    return {
        verb: value,
        'day': day,
        'nr': nr
    }


def sort_rules_key(rule):
    return '{day}{nr}'.format(**rule)


def parse_rules(rules):
    rule_dicts = [parse_rule(rule, value) for rule, value in rules.items()]

    sorted_rules = sorted(rule_dicts, key=sort_rules_key)
    final_rules = []

    for key, group in groupby(sorted_rules, sort_rules_key):
        rule_dict = {}
        [rule_dict.update(g) for g in group]
        final_rules.append(rule_dict)

    return final_rules


