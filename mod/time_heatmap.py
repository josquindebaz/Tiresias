import csv

with open('time.tsv', newline='') as tsvfile:
    test = csv.reader(tsvfile, delimiter='\t')
    values = {}
    max_value = 0
    for row in test:
        _date = row[0].split("/")[1:3]
        _date[1] = int("20%s"%_date[1]) if int(_date[1]) < 50\
                   else int("19%s"%_date[1])
        if int(row[1]) > max_value:
            max_value = int(row[1]) 
        if _date[1] in values:
            values[_date[1]][int(_date[0])] = int(row[1])
        else:
            values[_date[1]] = {int(_date[0]): int(row[1])}

svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
"""

for month in range(12):
    svg += '<text x="%d" y="45" font-family="sans-serif" \
font-size="12">%s</text>\n' %(66+month*50, month+1)

y = 0
for year in range(min(values), max(values)+1):
    y += 50

    svg += '<text x="10" y="%s" font-family="sans-serif" \
font-size="12">%s</text>\n' %(y+25, year)

    for month in range(1, 13):
        if month in values[year]:
            svg += '<rect x="%d" y="%d" width="50" height="50" \
style="fill:blue;stroke:gray;stroke-width:1;fill-opacity:%s" >\
<title>%s/%s: %s</title></rect>\n'% (month*50,
                                     y,
                                     values[year][month]/float(max_value),
                                     month,
                                     year,
                                     values[year][month])

      

svg += "</svg>"

with open('heatmaptest.svg', 'w') as svgfile:
    svgfile.write(svg)
