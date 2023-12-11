""" French departments weighted atlas
Author Josquin Debaz
GPL 3
"""

import re


def harmonize(content):
    """when department name varies"""
    content = re.sub('\nRéunion', "\nLa Réunion", content)
    content = re.sub('\nTerritoire de Belfort',
                     "\nTerritoire-de-Belfort", content)
    content = re.sub('\nSeine-St-Denis', "\nSeine-Saint-Denis", content)
    return content


def quartiles(values):
    """return quartiles of a series"""
    values = sorted(values)
    size = len(values)
    if size % 2:
        first = values[(size // 4)]
        median = values[(size // 2)]
        third = values[(size * 3 // 4)]
    else:
        first = (values[size // 4] + values[(size // 4) + 1]) / 2
        median = (values[size // 2] + values[(size // 2) + 1]) / 2
        third = (values[size * 3 // 4] + values[(size * 3 // 4) + 1]) / 2
    return first, median, third


class Mapper():
    """take a list with department[\t]value[\r\n] to produce a map"""

    def __init__(self, content, pathfile="data/departement_path.tsv"):
        self.dpt_values = {}
        self.department_paths = {}
        self.departement_numbers = {}
        self.departement_prefs = {}
        self.limits = [None, None, None]
        self.legend = [None, None, None, None]

        content = harmonize(content)
        self.get_dpt_values(content)
        self.get_dpt_paths(pathfile)

    def get_dpt_values(self, content):
        """put values in dictionnary"""
        for line in re.split('\r*\n', content):
            splitter = re.split('\t', line)
            if len(splitter) == 2 and splitter[0] != '':
                self.dpt_values[splitter[0]] = int(splitter[1])

    def get_dpt_paths(self, pathfile):
        """fetch svg path from datafile"""
        with open(pathfile, 'rb') as dptpthfile:
            dptpth = dptpthfile.read().decode('utf-8')
            for dpt in re.split("\r*\n", dptpth)[:-1]:
                dpt_number, dpt_name, dpt_path, dpt_pref = re.split("\t", dpt)
                self.department_paths[dpt_name] = dpt_path
                self.departement_numbers[dpt_name] = dpt_number
                self.departement_prefs[dpt_name] = dpt_pref

    def cumulated_fourth(self):
        """return four quarters from cumulated values"""
        unity = sum(self.dpt_values.values()) / 4

        cumul = 0
        steps = [None, None, None]
        sorted_dpt_list = sorted(self.dpt_values,
                                 key=self.dpt_values.__getitem__)
        for dpt in sorted_dpt_list:
            cumul += self.dpt_values[dpt]
            if cumul >= unity and not steps[0]:
                steps[0] = self.dpt_values[dpt]
            if cumul >= unity * 2 and not steps[1]:
                steps[1] = self.dpt_values[dpt]
            if cumul >= unity * 3:
                steps[2] = self.dpt_values[dpt]
                break
        return steps

    def make_legend(self, method="cumulated_fourth"):
        """calculate and prepare the legend"""
        if method == "quartiles":
            self.limits = quartiles(self.dpt_values.values())
        elif method == "fourth":
            unity = max(self.dpt_values.values()) // 4
            self.limits = [unity, unity * 2, unity * 3]
        else:  # cumulated fourth
            self.limits = self.cumulated_fourth()

        sorted_set = sorted(set(self.dpt_values.values()))

        first_quarter = [val for val in sorted_set if val <= self.limits[0]]
        if len(first_quarter) == 1:
            self.legend[0] = "%d" % self.limits[0]
        else:
            self.legend[0] = "%d-%d" % (first_quarter[0], first_quarter[-1])

        second_quarter = [val for val in sorted_set
                          if self.limits[0] < val <= self.limits[1]]
        if len(second_quarter) == 1:
            self.legend[1] = "%d" % self.limits[1]
        else:
            self.legend[1] = "%d-%d" % (second_quarter[0], second_quarter[-1])

        third_quarter = [val for val in sorted_set
                         if self.limits[1] < val <= self.limits[2]]
        if len(third_quarter) == 1:
            self.legend[2] = "%d" % self.limits[2]
        else:
            self.legend[2] = "%d-%d" % (third_quarter[0], third_quarter[-1])

        fourth_quarter = [val for val in sorted_set if val > self.limits[2]]
        if len(fourth_quarter) == 1:
            self.legend[3] = "%d" % fourth_quarter[0]
        else:
            self.legend[3] = "%d-%d" % (fourth_quarter[0],
                                        max(self.dpt_values.values()))

    def draw_map(self):
        """draw svg map"""
        colors = ["rgb(161, 247, 128)",
                  "rgb(115, 255, 0)",
                  "rgb(0, 208, 1)",
                  "rgb(1, 144, 3)"]

        mapcontent = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <svg version="1.1" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="P0" x="0" y="0" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.5" fill= "%s" /></pattern>
    <pattern id="P1" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.5" fill= "%s" /></pattern>
    <pattern id="P2" x="0" y="0" width="2.5" height="2.5" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill= "%s" /></pattern>
    <pattern id="P3" x="0" y="0" width="2" height="2" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill= "%s" /></pattern>
  </defs>
            """ % tuple(colors)

        height = 0
        for item in self.legend:
            mapcontent += """
  <rect width="30" height="20" x="5" y="%d" fill="url(#P%s)"/>
  <text x="40" y="%d" font-family="sans-serif" font-size="12">%s</text>""" % \
                          (height * 20 + 5, height, height * 20 + 20, item)
            height += 1

        mapcontent += "\n\n"

        for dpt, path in self.department_paths.items():
            mapcontent += "  <path style=\"stroke: gray; fill: "
            if dpt in self.dpt_values:
                if self.dpt_values[dpt] <= self.limits[0]:
                    mapcontent += "url(#P0)"
                elif self.dpt_values[dpt] <= self.limits[1]:
                    mapcontent += "url(#P1)"
                elif self.dpt_values[dpt] <= self.limits[2]:
                    mapcontent += "url(#P2)"
                else:
                    mapcontent += "url(#P3)"
            else:
                # mapcontent += "rgb(195, 195, 195);"
                mapcontent += "rgb(237, 237, 237);"
            mapcontent += "\" d=\"%s\">" % path
            mapcontent += "<title>(%s) %s" % (self.departement_numbers[dpt],
                                              dpt)
            if dpt in self.dpt_values:
                mapcontent += ": %d" % self.dpt_values[dpt]

            mapcontent += "</title></path>\n"

        height = 520
        for dpt in set(self.dpt_values.keys()).difference( \
                set(self.department_paths.keys())):
            mapcontent += """
<text x="120" y="%d" font-family="sans-serif" font-size="12">%s:\
%d</text>""" % (height, dpt, self.dpt_values[dpt])
            height += 13

        mapcontent += "\n</svg>"

        return mapcontent

    def draw_map_graduated(self):
        """draw svg graduated square map"""

        color = "rgb(1, 144, 3)"

        max_size = max(self.dpt_values.values())
        s_max_v = max_size ** 2

        if max_size > 64:
            r_max = 64
        elif max_size < 42:
            r_max = 42
        else:
            r_max = max_size
        s_max_d = r_max ** 2

        mapcontent = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
 """

        # Draw legend squares
        for i in [1, 2, 8]:
            a = (s_max_d / i) ** .5
            mapcontent += """
 <rect x="%s" y="%s" width="%d" height="%s"\
 fill="%s" fill-opacity="0.4" />""" % (5,
                                       5,
                                       a,
                                       a,
                                       color)
        # Draw legend digits
        for i in [1, 2, 8]:
            a = (s_max_d / i) ** .5
            mapcontent += """
<text x="%s" y="%d" font-family="sans-serif" font-size="12" >%s\
</text>""" % (a - 9,
              a + 3,
              int(max_size / i))

        mapcontent += "\n\n"

        # Draw paths
        for dpt, path in self.department_paths.items():
            mapcontent += "  <path style=\"stroke: silver; fill: white;"
            mapcontent += "\" d=\"%s\">" % path
            mapcontent += "<title>(%s) %s" % (self.departement_numbers[dpt],
                                              dpt)
            if dpt in self.dpt_values:
                mapcontent += ": %d" % self.dpt_values[dpt]

            mapcontent += "</title></path>\n"

        # Draw squares
        for dpt in self.department_paths:
            if dpt in self.dpt_values:
                x, y = re.split(",", self.departement_prefs[dpt])

                a = (self.dpt_values[dpt] / max_size * s_max_d) ** .5

                mapcontent += """
 <rect x="%s" y="%s" width="%s" height="%s"\
 fill="%s" fill-opacity="0.4" >""" % (float(x) - a / 2,
                                      float(y) - a / 2,
                                      a,
                                      a,
                                      color)
                mapcontent += "<title>(%s) %s" % (self.departement_numbers[dpt],
                                                  dpt)
                mapcontent += ": %d" % self.dpt_values[dpt]
                mapcontent += "</title></rect>"

        # Dpt with no path
        height = 520
        for dpt in set(self.dpt_values.keys()).difference( \
                set(self.department_paths.keys())):
            mapcontent += """
<text x="120" y="%d" font-family="sans-serif" font-size="12">%s:\
%d</text>""" % (height, dpt, self.dpt_values[dpt])
            height += 13

        mapcontent += "\n</svg>"

        return mapcontent
