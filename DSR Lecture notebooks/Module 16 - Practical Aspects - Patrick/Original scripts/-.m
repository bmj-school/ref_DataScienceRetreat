base_path = "data/fraud-data/2017-01-"

rowlist = []
for i in range(1,32):
    filename = base_path + "{:02d}".format(i) + ".txt"
    with open(filename) as f:
        for line in f:
            rowlist.append( json.loads(line))
        
df=pd.DataFrame(rowlist)