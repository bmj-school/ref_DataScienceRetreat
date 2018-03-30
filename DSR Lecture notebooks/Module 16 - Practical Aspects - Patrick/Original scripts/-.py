root_path = r"/home/batman/git/ref_DataScienceRetreat/DSR Lecture notebooks/Module X - Practical Aspects - Patrick/data/fraud-data"
files = []
dfs=list()
for fname in os.listdir(root_path):

    data = []
    with open(os.path.join(root_path,fname),'r') as f:
        for line in f:
            data.append(json.loads(line))
        
    files.append(data)
    dfs.append(pd.DataFrame(data))
