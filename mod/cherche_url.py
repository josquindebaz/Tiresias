import os
import re


url_list = set([])
m = re.compile("[htps:/]*www\S*")
for a, b, c in os.walk('.'):
    for f in c:
        if os.path.splitext(f)[1] in ['.txt', '.TXT']:
            with open(os.path.join(a, f), 'r') as p:
                d =  p.read()

            if m.search(d):
                #print(os.path.join(a, f), set(m.findall(d)))
                url_list = url_list.union( set(m.findall(d)))
                
with open('log.txt', 'w') as p2:
    p2.write("\r\n".join(url_list))
