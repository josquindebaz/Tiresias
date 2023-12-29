from mod.heatmap import quartiles, create_svg, parse_data, write_svg_legend, write_y_axis_legend


def test_quartiles_returns_3_quartiles():
    testing_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = quartiles(testing_values)

    assert len(result) == 3
    assert result == (3, 5, 7)


def test_heatmap_e2e():
    copy_pasted_data = """sans date	0
janvier/2020	3
février/2020	0
mars/2020	0
avril/2020	0
mai/2020	30
juin/2020	30
juillet/2020	23
août/2020	13
septembre/2020	0
octobre/2020	0
novembre/2020	0
décembre/2020	0
janvier/2021	10"""

    expected = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="300">
<style>
    .norm { font:14px sans-serif; }
    .small { font:12px sans-serif; }
    .vert { font:14px sans-serif; writing-mode: tb; }
    .rect { stroke:gray; stroke-width:1; fill:blue; }
</style>
<text x="35" y="45" class="norm">d</text>
<text x="35" y="95" class="norm">n</text>
<text x="35" y="145" class="norm">o</text>
<text x="35" y="195" class="norm">s</text>
<text x="35" y="245" class="norm">a</text>
<text x="35" y="295" class="norm">j</text>
<text x="35" y="345" class="norm">j</text>
<text x="35" y="395" class="norm">m</text>
<text x="35" y="445" class="norm">a</text>
<text x="35" y="495" class="norm">m</text>
<text x="35" y="545" class="norm">f</text>
<text x="35" y="595" class="norm">j</text>
 <rect width="50" height="50" x="50" y="20" class="rect" style="fill-opacity:0.0"><title>12/2020: 0</title></rect>
 <rect width="50" height="50" x="50" y="70" class="rect" style="fill-opacity:0.0"><title>11/2020: 0</title></rect>
 <rect width="50" height="50" x="50" y="120" class="rect" style="fill-opacity:0.0"><title>10/2020: 0</title></rect>
 <rect width="50" height="50" x="50" y="170" class="rect" style="fill-opacity:0.0"><title>9/2020: 0</title></rect>
 <rect width="50" height="50" x="50" y="220" class="rect" style="fill-opacity:0.43333333333333335"><title>8/2020: 13</title></rect>
 <rect width="50" height="50" x="50" y="270" class="rect" style="fill-opacity:0.7666666666666667"><title>7/2020: 23</title></rect>
 <rect width="50" height="50" x="50" y="320" class="rect" style="fill-opacity:1.0"><title>6/2020: 30</title></rect>
 <rect width="50" height="50" x="50" y="370" class="rect" style="fill-opacity:1.0"><title>5/2020: 30</title></rect>
 <rect width="50" height="50" x="50" y="420" class="rect" style="fill-opacity:0.0"><title>4/2020: 0</title></rect>
 <rect width="50" height="50" x="50" y="470" class="rect" style="fill-opacity:0.0"><title>3/2020: 0</title></rect>
 <rect width="50" height="50" x="50" y="520" class="rect" style="fill-opacity:0.0"><title>2/2020: 0</title></rect>
 <rect width="50" height="50" x="50" y="570" class="rect" style="fill-opacity:0.1"><title>1/2020: 3</title></rect>
<text x="75.0" y="630" class="vert">2020</text>
 <rect width="50" height="50" x="100" y="570" class="rect" style="fill-opacity:0.3333333333333333"><title>1/2021: 10</title></rect>
<text x="125.0" y="630" class="vert">2021</text>
   <rect width="50" height="100.0" x="50" y="670" class="rect"><title>2020: 198</title></rect>
   <text x="50" y="785.0" class="small">198</text>
   <rect width="50" height="10.1010101010101" x="100" y="670" class="rect"><title>2021: 20</title></rect>
   <text x="100" y="695.10101010101" class="small">20</text>
<rect width="50" height="50" x="160" y="300" class="rect" style="fill-opacity:0.0"></rect>
 <text x="215" y="330" class="norm">0</text>
<rect width="50" height="50" x="160" y="250" class="rect" style="fill-opacity:0.25"></rect>
 <text x="215" y="280" class="norm">7</text>
<rect width="50" height="50" x="160" y="200" class="rect" style="fill-opacity:0.5"></rect>
 <text x="215" y="230" class="norm">15</text>
<rect width="50" height="50" x="160" y="150" class="rect" style="fill-opacity:0.75"></rect>
 <text x="215" y="180" class="norm">22</text>
<rect width="50" height="50" x="160" y="100" class="rect" style="fill-opacity:30"></rect>
 <text x="215" y="130" class="norm">30</text>

</svg>"""

    values = parse_data(copy_pasted_data)
    result = create_svg(values)

    assert result == expected


def test_write_y_axis_legend():
    expected = """<text x="85" y="45" class="norm">d</text>
<text x="85" y="95" class="norm">n</text>
<text x="85" y="145" class="norm">o</text>
<text x="85" y="195" class="norm">s</text>
<text x="85" y="245" class="norm">a</text>
<text x="85" y="295" class="norm">j</text>
<text x="85" y="345" class="norm">j</text>
<text x="85" y="395" class="norm">m</text>
<text x="85" y="445" class="norm">a</text>
<text x="85" y="495" class="norm">m</text>
<text x="85" y="545" class="norm">f</text>
<text x="85" y="595" class="norm">j</text>
"""

    result = write_y_axis_legend(100)
    assert result == expected


def test_write_svg_legend():
    expected = """<rect width="50" height="50" x="160" y="300" class="rect" style="fill-opacity:0.0"></rect>
 <text x="215" y="330" class="norm">0</text>
<rect width="50" height="50" x="160" y="250" class="rect" style="fill-opacity:0.25"></rect>
 <text x="215" y="280" class="norm">7</text>
<rect width="50" height="50" x="160" y="200" class="rect" style="fill-opacity:0.5"></rect>
 <text x="215" y="230" class="norm">15</text>
<rect width="50" height="50" x="160" y="150" class="rect" style="fill-opacity:0.75"></rect>
 <text x="215" y="180" class="norm">22</text>
<rect width="50" height="50" x="160" y="100" class="rect" style="fill-opacity:30"></rect>
 <text x="215" y="130" class="norm">30</text>
"""

    legend_list = [[0, 0.0], [7, 0.25], [15, 0.5], [22, 0.75], [30, 30]]
    y = 100
    step = 50

    result = write_svg_legend(legend_list, y, step)

    assert result == expected
