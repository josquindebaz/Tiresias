import re

def fetch_date(given_date):
    months = {
        "janvier": "01",
        'février': "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12",
        "January": "01",
        'February': "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    day_first_date_format = re.compile(r"(\d+) (\S*) (\d{4})")
    month_first_date_format = re.compile(r"(\S*)\s+(\d+)[,\s]{2,}(\d{4})")

    day, month, year = "", "", ""
    if not day_first_date_format.search(given_date) and not month_first_date_format.search(given_date):
        print("Problem reading date [%s]" % given_date)
        return False

    if day_first_date_format.search(given_date):
        day, month, year = day_first_date_format.search(given_date).group(1, 2, 3)
        if month not in months:
            print("I don't know this month %s" % month)
            return False

    elif month_first_date_format.search(given_date):
        month, day, year = month_first_date_format.search(given_date).group(1, 2, 3)
        if month not in months:
            print("I don't know this month %s" % month)
            return False

    return "%s/%s/%s" % (f"{int(day):02d}", months[month], year)