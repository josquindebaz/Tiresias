import re
with open("../data/departement_path.csv" ) as f:
    lines = f.readlines()
    path_dic = {}
    print(len(lines), lines[0][0:5])
    for line in lines:
        num, name, path = line.split(',')
        #print(num)
        path_dic[name] = [num, path]
    #print(len(path_dic), path_dic['Ain'])
    
    
