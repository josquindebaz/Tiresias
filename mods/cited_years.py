"""Transform a list of temporel references to a table of years
by Josquin Debaz
GPL3
11/12/2019"""

import re

months = [
    "année",
    "janvier",
    "février", "fevrier",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août", "aout",
    "septembre",
    "octobre",
    "novembre",
    "décembre", "decembre",
    ]

def find_years(content):
    years = {}
    year_pattern = re.compile('\s{1,}([12]\d{3})\.?\t(\d{1,})')
    month_pattern = re.compile('(%s)\s{1,}(\d{2})\.?\t(\d{1,})'\
                               %"|".join(months), re.IGNORECASE)
    for index, line in enumerate(re.split("\r?\n", content)):       
        if year_pattern.search(line):
            #take the forms in 1XXX and 20XX
            year, value = year_pattern.findall(line)[0]
            if year in years:
                years[year] += int(value)
            else:
                years[year] = int(value)
        elif month_pattern.search(line):
            #take the forms in année/month XX
            month, year, value = month_pattern.findall(line)[0]
            if int(year[0]) < 50:
                year = "20%s"%year
            else :
                year = "19%s"%year
            if year in years:
                years[year] += int(value)
            else:
                years[year] = int(value)
    #add missing years with a 0 value
    years.update({str(year_index): 0 for year_index
           in range(int(min(years)), int(max(years)))
           if str(year_index) not in years})
    
    return years


if __name__ == "__main__":
    filename = "cited_years.txt"
    with open(filename, 'rb') as page:
        content = page.read().decode('latin1')
    find_years(content)
    
    
