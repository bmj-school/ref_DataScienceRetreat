print_imports()
import os

# SEE https://seaborn.pydata.org/tutorial/distributions.html

import pandas as pd # Import again for code completion
import numpy as np # Import again for code completion
import matplotlib as mpl
import matplotlib.pyplot as plt
import sklearn as sk
import sklearn
import sklearn.linear_model
# to make this notebook's output stable across runs
np.random.seed(42)

# Ignore useless warnings (see SciPy issue #5998)
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

# To plot pretty figures

plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


sns.set(style="ticks")

#%% ===========================================================================
#  Data source
# =============================================================================

import tarfile
#from six.moves import urllib
import urllib as urllib
print(urllib)

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = "datasets/housing"
HOUSING_URL = DOWNLOAD_ROOT + HOUSING_PATH + "/housing.tgz"
print(HOUSING_URL)

PATH_DATA_ROOT = r"/home/batman/git/handson-ml/"
path_data = os.path.join(PATH_DATA_ROOT, "datasets", "housing", "")
assert os.path.exists(path_data)

def fetch_housing_data(source_url, path_data):
    tgz_path = os.path.join(path_data, "housing.tgz")
    urllib.request.urlretrieve(source_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path = path_data)
    housing_tgz.close()

#def load_data(path_data):
#    csv_path = 
#    return pd.read_csv(csv_path)

#%% ===========================================================================
#  Load
# =============================================================================
#fetch_housing_data(HOUSING_URL,path_data)
df = pd.read_csv(os.path.join(path_data, "housing.csv"))


#%% Overview data
df_numeric = df._get_numeric_data()
df_numeric_nonan = df_numeric.dropna()
df_info = pd.DataFrame(df.info())
df_counts = pd.DataFrame(df.loc[:,"ocean_proximity"].value_counts())
df_desc = pd.DataFrame(df.describe())
df_grouped = df.groupby("ocean_proximity").mean()
#print(df2)


#%% Density waterfall

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Create the data
rs = np.random.RandomState(1979)
x = rs.randn(500)
g = np.tile(list("ABCDEFGHIJ"), 50)
df = pd.DataFrame(dict(x=x, g=g))
m = df.g.map(ord)
df["x"] += m

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="g", hue="g", aspect=15, size=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "x", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color, 
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "x")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play will with overlap
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)


#%% Pairwise Scatter
#sns.pairplot(df, hue="species")
#sns.pairplot(country_stats)
pairplt = sns.pairplot(df, hue = "ocean_proximity")
path_out = os.path.join(path_data, "pairplot.png")
pairplt.savefig(path_out)


#%% Pairwise Density on ALL
g = sns.PairGrid(df)
g.map_diag(sns.kdeplot)
g.map_offdiag(sns.kdeplot, cmap="Blues_d", n_levels=3);
path_out = os.path.join(path_data, "pairdensity.pdf")
g.savefig(path_out, format='pdf')


#%% Pairwise Density on SUBSET
df_subset=df.loc[:,['median_income','median_house_value']]
g = sns.PairGrid(df_subset)
g.map_diag(sns.kdeplot)
#g.map_offdiag(sns.kdeplot, cmap="Blues_d", n_levels=6);
g.map_offdiag(sns.kdeplot, cmap="Blues_d", n_levels=10);
path_out = os.path.join(path_data, "pairdensity2.pdf")
g.savefig(path_out, format='pdf')

pairplt = sns.pairplot(df_subset)


#%% Testing correlation

import pandas.rpy2.common as com
#import seaborn as sns
import rpy2.common as com

#%matplotlib inline

# load the R package ISLR
infert = com.importr("ISLR")

# load the Auto dataset
auto_df = com.load_data('Auto')

# calculate the correlation matrix
corr = auto_df.corr()

# plot the heatmap
sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)

#%% Boxplot
#sns.set_style('darkgrid')
#sns.boxplot(df_numeric)
plots=list()
num_boxplots = df_numeric_nonan.shape[1]
#num_boxplots = 2

fig, ax = plt.subplots(nrows=num_boxplots, 
                       ncols=1, 
                       figsize=(20,40), 
                       #figsize=(20,10), 
                       sharex=False, 
                       sharey=False)


#print(plots)
#ax[0]
#TODO: Change histogram to second axis!!!
for colnum in range(num_boxplots):
    
    # The data
    data_series = df_numeric_nonan.iloc[:,colnum]
    
    
    this_mean = data_series.describe()['mean']
    this_median = data_series.describe()['50%']
    this_std =  data_series.describe()['std']
    this_min =  data_series.describe()['min']
    this_max =  data_series.describe()['max']


    # Histogram
    #bins = np.arange(np.floor(data_series.min()),np.ceil(data_series.max()))
    values, base = np.histogram(data_series, bins=100, density=1)
    width = base[1]-base[0]
    values2 = values * width
    print(sum(values2))
    #this_hist = np.histogram(data_series,bins=bins,density=True)
    #this_hist = list(this_hist)
    values3=-3*values2 + 0.5
    #values3 = values3*-1
    
    #this_hist = np.histogram(,bins=100,density=True)
    
    ax[colnum].plot(base[:-1],values3,
      '-',
      linewidth=3,
      color='y',
      )
    #ax[colnum].bar(this_hist[1][:-1],this_hist[0])
    #n, bins, rectangles = ax[colnum].hist(data_series, 50, normed=True)
    
    #sum(n)
    #print(np.sum(n * np.diff(bins)))
    
    # Boxplot    
    sns.boxplot(data_series,
                            ax=ax[colnum],
                            width=0.3,
                            fliersize=2,
                            notch=True,
                            #color=b
                            )
    
    
    # NEW Histogram\
    # Let X be the array whose histogram needs to be plotted.
    #nx, xbins, ptchs = plt.hist(data_series, bins=50,density=True)
    #nx = nx * (xbins[1]-xbins[0])
    #xbins
    #plt.clf() # Get rid of this histogram since not the one we want.
    #nx_frac = nx/float(len(nx)) # Each bin divided by total number of objects.
    #width = xbins[1] - xbins[0] # Width of each bin.
    #x = np.ravel(list(zip(xbins[:-1], xbins[:-1]+width)))
    #y = np.ravel(list(zip(nx_frac,nx_frac)))
    #sum(y)
    #plt.plot(x,y,linestyle="dashed",label="MyLabel")

    
    ax[colnum].grid(color='lightgrey', linestyle='dashed', linewidth=1)
    ax[colnum].axes.get_yaxis().set_visible(False)
    #dir(ax[colnum])
    ax[colnum].set_frame_on(False)
    #ax[colnum].set_facecolor('xkcd:salmon')
    
    
    title_str = "{} {:0.2f} +/- {:0.2f}".format(ax[colnum].get_xlabel(),this_mean,this_std)
    ax[colnum].set_xlabel('')
    xlims = ax[colnum].get_xlim()
    midpt = xlims[0] + (xlims[1]-xlims[0])/2
    ylims = ax[colnum].get_ylim()
    ax[colnum].text(midpt,ylims[1]*0.85, title_str,size=10,color='black',horizontalalignment='center')

path_boxplot = os.path.join(path_data, "boxplot.pdf")

fig.savefig(path_boxplot,format='pdf',bbox_inches="tight")


#data_series = df_numeric_nonan.loc[:,'median_income']

#this_hist = np.histogram(,bins=100,density=True)


#np.bincount(df_numeric_nonan.loc[:,'households'])
#sum(values)

#%% MY HIST FUNCTION
def my_hist_frame(data, column=None, by=None, grid=True, xlabelsize=None,
               xrot=None, ylabelsize=None, yrot=None, ax=None, sharex=False,
               sharey=False, figsize=None, layout=None, bins=10, **kwds):
    fig, axes = plt.subplots(naxes=naxes, ax=ax, squeeze=False,
                          sharex=sharex, sharey=sharey, figsize=figsize,
                          layout=layout)
    _axes = _flatten(axes)

    for i, col in enumerate(_try_sort(data.columns)):
        ax = _axes[i]
        ax.hist(data[col].dropna().values, bins=bins, **kwds)
        ax.set_title(col)
        ax.grid(grid)

    _set_ticks_props(axes, xlabelsize=xlabelsize, xrot=xrot,
                     ylabelsize=ylabelsize, yrot=yrot)
    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    return axes

my_hist_frame(df)
    
#%% Histograms
df_numeric = df._get_numeric_data()
df_numeric_n = df_numeric.dropna()
sns.distplot(df_numeric_n)

#%% Histograms
#fig, ax = plt.subplots()
#df.hist('ColumnName', ax=ax)

#fig_hist = df.hist(bins = 50, figsize=(20,15),ax=ax)
res = df.hist(bins = 50, figsize=(20,15))
path_hist = os.path.join(path_data, "histograms.pdf")
print(res)

#print(len(res))
for i in range(len(res)):
    for j in range(len(res[i])):
        print(res[i][j])
fig_hist.savefig(path_hist,format='pdf',bbox_inches="tight")


#%% Normalize, histogram
scaler = sk.preprocessing.StandardScaler().fit(df)
print(scaler)
scaler.mean_
scaler.scale_
df2 = pd.DataFrame(scaler.transform(df),columns=df.columns, index=df.index)

sns.pairplot(df2)

def norm_df(df):
    return pd.DataFrame(scaler.transform(df),columns=df.columns, index=df.index)

country_stats_norm = norm_df(country_stats)


