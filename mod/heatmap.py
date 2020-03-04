""" Prospéro month distribution to heatmap svg
Author Josquin Debaz
GPL 3
"""

import re

def quartiles(values):
    """return quartiles of a series"""
    values = sorted(values)
    size = len(values)
    if size % 2:
        first = values[(size//4)]
        median = values[(size//2)]
        third = values[(size*3//4)]
    else:
        first = (values[size//4] + values[(size//4)+1])/2
        median = (values[size//2] + values[(size//2)+1])/2
        third = (values[size*3//4] + values[(size*3//4)+1])/2
    return first, median, third

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
    text_num = []
    for year, months in values.items():
        for month, texts in months.items():
            text_num.append(texts)
    max_value = max(text_num)
    min_value = min(text_num)
    first_q, median, third_q = quartiles(text_num)
    
    svg = ''
    for month in range(12, 0, -1):
        svg += '<text x="25" y="%s" font-family="sans-serif" \
font-size="12">%s</text>\n' %(645-month*50, month)

    y = 0
    for year in range(min(values), max(values)+1):
        y += 50
        for month in range(12, 0, -1):
            if month in values[year]:
                svg += '<rect width="50" height="50" '
                svg += 'x="%d" y="%d" '%(y, 620-month*50)
                svg += 'style="stroke:gray;stroke-width:1;fill:blue;'
                svg += 'fill-opacity:%s">'%(values[year][month]/float(max_value))
                svg += '<title>%s/%s: %s</title>'%(month,
                                                   year,
                                                   values[year][month])
                svg += '</rect>\n'
        svg += ' <text x="%s" y="%s" font-family="sans-serif" \
font-size="12">%s</text>\n' %(y+10, 640, year)
        
    svg += '<rect width="50" height="50" x="%s" y="300" \
style="stroke:gray;stroke-width:1;fill:blue;fill-opacity:\
%s"></rect>'%(y+60, min_value/float(max_value))
    svg += '\n <text x="%s" y="330" font-family="sans-serif" \
font-size="14">%s</text>\n' %(y+120, min_value)

    svg += '<rect width="50" height="50" x="%s" y="250" \
style="stroke:gray;stroke-width:1;fill:blue;fill-opacity:\
%s"></rect>'%(y+60, 0.25)
    svg += '\n <text x="%s" y="280" font-family="sans-serif" \
font-size="14">%s</text>\n' %(y+120,int(max_value/4))

    svg += '<rect width="50" height="50" x="%s" y="200" \
style="stroke:gray;stroke-width:1;fill:blue;fill-opacity:\
%s"></rect>'%(y+60, 0.5)
    svg += '\n <text x="%s" y="230" font-family="sans-serif" \
font-size="14">%s</text>\n' %(y+120, int(max_value/2))

    svg += '<rect width="50" height="50" x="%s" y="150" \
style="stroke:gray;stroke-width:1;fill:blue;fill-opacity:\
%s"></rect>'%(y+60, 0.75)
    svg += '\n <text x="%s" y="180" font-family="sans-serif" \
font-size="14">%s</text>\n' %(y+120, int(3*max_value/4))

    svg += '<rect width="50" height="50" x="%s" y="100" \
style="stroke:gray;stroke-width:1;fill:blue"></rect>'%(y+60)
    svg += '\n <text x="%s" y="130" font-family="sans-serif" \
font-size="14">%s</text>\n' %(y+120, max_value)

    svg += '\n <text x="%s" y="380" font-family="sans-serif" \
font-size="14">Q1:%s</text>\n' %(y+60, first_q)   
    svg += '\n <text x="%s" y="400" font-family="sans-serif" \
font-size="14">Q2:%s</text>\n' %(y+60, median)
    svg += '\n <text x="%s" y="420" font-family="sans-serif" \
font-size="14">Q3:%s</text>\n' %(y+60, third_q)
        
    svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="%s">\n'%(y+200) + svg
    svg += "\n</svg>"

    return svg
