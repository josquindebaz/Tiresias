""" Prospéro month distribution to heatmap svg
Author Josquin Debaz
GPL 3
"""
import re

from mod.HeatmapDataProcessor import HeatmapDataProcessor
from mod.HeatmapSvgWriter import HeatmapSvgWriter


def parse_data(data):
    values = {}
    months = {"janvier": 1,
              "février": 2,
              "mars": 3,
              "avril": 4,
              "mai": 5,
              "juin": 6,
              "juillet": 7,
              "août": 8,
              "septembre": 9,
              "octobre": 10,
              "novembre": 11,
              "décembre": 12}

    for line in data.split("\n"):
        if not re.search("sans date", line) and not re.match(r"^\s*$", line):
            row = line.split('\t')
            _date = row[0].split("/")
            year = int(_date[1])
            if year in values:
                values[year][months[_date[0]]] = int(row[1])
            else:
                values[year] = {months[_date[0]]: int(row[1])}
    return values


def create_svg(monthly_values):
    data_processor = HeatmapDataProcessor(monthly_values)
    svg_writer = HeatmapSvgWriter(step=50, data=data_processor)

    return svg_writer.produce_svg()


