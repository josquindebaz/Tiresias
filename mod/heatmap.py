""" Prospéro month distribution to heatmap svg
Author Josquin Debaz
GPL 3
"""

import re

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
        if not re.search("sans date", line) and not re.match("^\s*$", line):
            row = line.split('\t')
            _date = row[0].split("/")
            year = int(_date[1])
            if year in values:
                values[year][months[_date[0]]] = int(row[1])
            else:
                values[year] = {months[_date[0]]: int(row[1])}
    return(values)

def create_svg(values):
    max_value = max([max(month.values())
                      for month in
                      [values for values in values.values()]])
    min_value = min([min(month.values())
                      for month in
                      [values for values in values.values()]])
    
    svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">\n'

    for month in range(1, 13):
        svg += '<text x="25" y="%s" font-family="sans-serif" \
font-size="12">%s</text>\n' %(month*50+25, month)

    y = 0
    for year in range(min(values), max(values)+1):
        y += 50
        svg += ' <text x="%s" y="35" font-family="sans-serif" \
font-size="12">%s</text>\n' %(y+10, year)

        for month in range(1, 13):
            if month in values[year]:
                svg += '<rect width="50" height="50" '
                svg += 'x="%d" y="%d" '%(y,month*50)
                svg += 'style="stroke:gray;stroke-width:1;fill:blue;'
                svg += 'fill-opacity:%s">'%(values[year][month]/float(max_value))
                svg += '<title>%s/%s: %s</title>'%(month,
                                                   year,
                                                   values[year][month])
                svg += '</rect>\n'

    svg += '<rect width="50" height="50" x="%s" y="100" \
style="stroke:gray;stroke-width:1;fill:blue;fill-opacity:\
%s"></rect>'%(y+60,min_value/float(max_value))
    svg += '\n <text x="%s" y="130" font-family="sans-serif" \
font-size="14">%s</text>\n' %(y+120, min_value)
    svg += '<rect width="50" height="50" x="%s" y="150" \
style="stroke:gray;stroke-width:1;fill:blue"></rect>'%(y+60)
    svg += '\n <text x="%s" y="180" font-family="sans-serif" \
font-size="14">%s</text>\n' %(y+120, max_value)
    
    svg += "\n</svg>"
    return svg

