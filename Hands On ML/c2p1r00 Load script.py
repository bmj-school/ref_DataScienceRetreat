# =============================================================================
# Standard imports
# =============================================================================
import tarfile
import urllib as urllib
import os
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info('Started logging')

# =============================================================================
# External imports - reimported for code completion! 
# =============================================================================
print_imports()
import pandas as pd # Import again for code completion
import numpy as np # Import again for code completion
import matplotlib as mpl
import matplotlib.pyplot as plt
#sns.set(style="ticks")
import sklearn as sk
import sklearn
import sklearn.linear_model
# to make this notebook's output stable across runs
np.random.seed(42)
from sklearn_pandas import DataFrameMapper
from sklearn_features.transformers import DataFrameSelector

# Ignore useless warnings (see SciPy issue #5998)
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

# Plotly
import plotly.plotly as py
py.plotly.tools.set_credentials_file(username='notbatman', api_key='1hy2cho61mYO4ly5R9Za')
import plotly.graph_objs as go

#%% ===========================================================================
#  Data source and paths
# =============================================================================
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

#%% ===========================================================================
#  Load
# =============================================================================
#fetch_housing_data(HOUSING_URL,path_data)
df = pd.read_csv(os.path.join(path_data, "housing.csv"))
logger.info("Loaded")

#%% ===========================================================================
#  Data Preparation
# =============================================================================

# Add some attributes
df['rooms_per_house'] = df['total_rooms']/df['households']
df['bedrooms_per_room'] = df['total_bedrooms']/df['total_rooms']
df['population_per_household'] = df['population']/df['households']

# Create income code column for classifying income for a STRATIFIED split
df['income'] = np.ceil(df['median_income']/1.5)
df['income'].where(df['income'] < 5, 5.0, inplace = True)

# Sklearn Split object over this category to ensure representative sampling
split = sk.model_selection.StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

# Perform stratified split
for train_i, test_i in split.split(df, df['income']):
    df_train = df.loc[train_i]
    df_test = df.loc[test_i]
original_split_percent = df['income'].value_counts() / len(df)*100
train_split_percent = df_train['income'].value_counts() / len(df_train)*100
compare = pd.DataFrame([original_split_percent, train_split_percent]).transpose()
compare.columns = ['original','split']
compare['diff'] = compare['original'] - compare['split']

# Drop this stratification category
df_train.drop(["income"],axis=1,inplace=True)
df_test.drop(["income"],axis=1,inplace=True)

logger.info(f"Test: {len(df_test)} records")
logger.info(f"Train: {len(df_train)} records")

y_tr = df_train["median_house_value"].copy()
X_tr = df_train.drop("median_house_value", axis=1) # drop labels for training set

y_test = df_test["median_house_value"].copy()
X_test = df_test.drop("median_house_value", axis=1) # drop labels for training set

#df_numeric = df._get_numeric_data()
#num_attribs= list(df_numeric)
#cat_attribs = ['ocean_proximity']





#%% CLEAN: Imputation
def my_impute(df):
    imputer = sk.preprocessing.Imputer(strategy="median")
    df_numeric = df._get_numeric_data() # Only works on numeric data
    imputer.fit(df_numeric) # Fit the object
    imputer.statistics_ # Print to see the results
    X = imputer.transform(df_numeric) 
    return pd.DataFrame(X,columns=df_numeric.columns)
df_tr = my_impute(df)

#%% CLEAN: Text label numeric encoding
def my_encode_numerical(df, colname):
    # Given a column with a text label, encode it to numerical
    encoder = sk.preprocessing.LabelEncoder()
    categories = df[colname]
    res = encoder.fit_transform(categories)
    print(encoder.classes_)
    return res

numeric_cats = my_encode_numerical(df, "ocean_proximity")
print(numeric_cats)

#%% CLEAN: Text label one-hot encoding FROM NUMERIC!
def my_encode_onehot(df, colname):
    # Given a column with a text label convert to 1 HOT
    encoder = sk.preprocessing.OneHotEncoder()
    #categories = df[colname]
    encoder.fit_transform(categories)
    print(encoder.classes_)

my_encode_onehot(numeric_cats, "ocean_proximity")

#%% CLEAN: Text to one hot directly LabelBinarizer
def my_encode_labelonehot(df, colname):
    # Given a column with a text label, encode it to numerical
    encoder = sk.preprocessing.LabelBinarizer()
    #categories = df[colname]
    res = encoder.fit_transform(df[colname])
    #print(encoder.classes_)
    return res

oneH = my_encode_labelonehot(df, "ocean_proximity")
#print(numeric_cats)



#%% Custom Transformer Classes
#asdf
rooms_ix, bedrooms_ix, population_ix, household_ix = 3,4,5,6

class CombinedAttributesAdder(sk.base.BaseEstimator, sk.base.TransformerMixin):
    def __init__(self, add_bed_per_room=True):
        self.add_bed_per_room = add_bed_per_room
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix] / X[:,household_ix]
        population_per_household = X[:, rooms_ix] / X[:, household_ix]
        if self.add_bed_per_room:
            bedrooms_per_room = X[:,bedrooms_ix] / X[:,rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        else: 
            return np.c_[X, rooms_per_household, population_per_household]
attr_adder = CombinedAttributesAdder(add_bed_per_room=False)
housing_extra_attribs=attr_adder.transform(df.values)


#%% Numerical pipeline

num_pipeline = sk.pipeline.Pipeline([
        ('imputer', sk.preprocessing.Imputer(strategy="median")),
        ('attribs_adder', CombinedAttributesAdder()),
        ('std_scaler', sk.preprocessing.StandardScaler()),
        ])
print(num_pipeline)

housing_numeric_piped = num_pipeline.fit_transform(df_numeric)

#%% Total joined pipeline

import importlib.util
spec = importlib.util.spec_from_file_location("future_encoders", 
                                              "/home/batman/git/handson-ml/future_encoders.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
foo.OneHotEncoder()




num_pipeline = sk.pipeline.Pipeline([
        ('selector',DataFrameSelector(num_attribs)),
        ('imputer', sk.preprocessing.Imputer(strategy="median")),
        ('attribs_adder', CombinedAttributesAdder()),
        ('std_scaler', sk.preprocessing.StandardScaler()),
        ])

cat_pipeline = sk.pipeline.Pipeline([
        ('selector',DataFrameSelector(cat_attribs)),
        ('label_binarizer', foo.OneHotEncoder()),
        #('label_binarizer', sk.preprocessing.CategoricalEncoder()),
        #('cat_encoder', OneHotEncoder(sparse=False)),


        ])
#CategoricalEncoder 
full_pipeline = sk.pipeline.FeatureUnion(
        transformer_list = [
                ("num_pipeline",num_pipeline),
                ("cat_pipeline",cat_pipeline),
                ])

housing_prepared = full_pipeline.fit_transform(df).toarray()
#np.array(housing_prepared)

#%% TRAIN: Linear Reg
lin_reg = sk.linear_model.LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

#%% EVALUATE: Linear Reg
housing_predictions = linreg.predict(housing_prepared)
lin_mse = sk.metrics.mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)
print(lin_rmse)

#%% TRAIN: Decision tree
from sklearn import tree
tree_reg = sk.tree.DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)
housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = sk.metrics.mean_squared_error(housing_labels, housing_predictions)
tree_rmse = np.sqrt(tree_mse)
print(tree_rmse)

#%% TRAIN: Random Forest
from sklearn import ensemble
forest_reg = sk.ensemble.RandomForestRegressor()
forest_reg.fit(housing_prepared, housing_labels)
housing_predictions = tree_reg.predict(housing_prepared)
forest_mse = sk.metrics.mean_squared_error(housing_labels, housing_predictions)
forest_rmse = np.sqrt(forest_mse)
print(forest_rmse)


#%% EVALUATEL: K-Folds
scores = sk.model_selection.cross_val_score(tree_reg,housing_prepared,housing_labels,
                                            scoring="neg_mean_squared_error",cv=10)
rmse_scores = np.sqrt(-scores)
print("Linear", np.mean(rmse_scores), np.std(rmse_scores))

scores = sk.model_selection.cross_val_score(lin_reg,housing_prepared,housing_labels,
                                            scoring="neg_mean_squared_error",cv=10)
rmse_scores = np.sqrt(-scores)
print("Tree", np.mean(rmse_scores), np.std(rmse_scores))

scores = sk.model_selection.cross_val_score(forest_reg,housing_prepared,housing_labels,
                                            scoring="neg_mean_squared_error",cv=10)
rmse_scores = np.sqrt(-scores)
print("Forest", np.mean(rmse_scores), np.std(rmse_scores))

#%% Grid Search
param_grid = [
        {'n_estimators': [3,10,20,30,40,50,60,70,80,90,100],'max_features':[2,4,6,8,10,12,14,16]},
        {'bootstrap':[False], 'n_estimators':[3,10],'max_features':[2,3,4]},
        ]
forest_reg = sk.ensemble.RandomForestRegressor()
grid_search = sk.model_selection.GridSearchCV(forest_reg, param_grid, cv=5,
                                              scoring='neg_mean_squared_error')
grid_search.fit(housing_prepared,housing_labels)
#%% 
grid_search.best_params_
grid_search.best_estimator_

#%% EVALUATE: Grid search results
res = zip(grid_search.cv_results_["mean_test_score"], grid_search.cv_results_["params"])
res = list(res)
res.sort(key=lambda tup: tup[0])
for mean_score,params in res:
    print("{:0.0f} {}".format(np.sqrt(-mean_score), params))

best_model = grid_search.best_estimator_
ranked_feats = best_model.feature_importances_
#sk.ensemble.RandomForestRegressor?
extra_attribs=['','','']
cat_one_hot_attribs = [0,1,2,3,4]
all_attribs = num_attribs + extra_attribs + cat_one_hot_attribs
sorted(zip(ranked_feats,all_attribs),reverse=True)
#.best_estimator_.feature_importances_


#%% EVALUATE: Test
final_model = grid_search.best_estimator_
X_test = df_test.drop("median_house_value",axis=1)
y_test = df_test["median_house_value"].copy()
X_test_prepared = full_pipeline.transform(X_test).toarray()

final_pred = final_model.predict(X_test_prepared)

final_mse = sk.metrics.mean_squared_error(y_test,final_pred)
final_rmse = np.sqrt(final_mse)

#%% EXPLORE: Overview data
df_numeric_nonan = df_numeric.dropna()
df_info = pd.DataFrame(df.info())
df_counts = pd.DataFrame(df.loc[:,"ocean_proximity"].value_counts())
df_desc = pd.DataFrame(df.describe())
df_grouped = df.groupby("ocean_proximity").mean()
#print(df2)


#%% EXPLORE: Correlation
corr_matrix = df.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)

#%% VISUALIZE: Box plot - Plotly
data = list()

for col in df_numeric_nonan.columns:
    data.append(  go.Box( y=df[col], name=col, showlegend=False ) )

data.append( go.Scatter( x = df.columns, y = df.mean(), mode='lines', name='mean' ) )

# IPython notebook
# py.iplot(data, filename='pandas-box-plot')

url = py.plot(data, filename='pandas-box-plot')

#%% VISUALIZE: With real map
import matplotlib.image as mpimg
california_img=mpimg.imread(PROJECT_ROOT_DIR + '/images/end_to_end_project/california.png')
ax = housing.plot(kind="scatter", x="longitude", y="latitude", figsize=(10,7),
                       s=housing['population']/100, label="Population",
                       c="median_house_value", cmap=plt.get_cmap("jet"),
                       colorbar=False, alpha=0.4,
                      )
plt.imshow(california_img, extent=[-124.55, -113.80, 32.45, 42.05], alpha=0.5,
           cmap=plt.get_cmap("jet"))
plt.ylabel("Latitude", fontsize=14)
plt.xlabel("Longitude", fontsize=14)

prices = housing["median_house_value"]
tick_values = np.linspace(prices.min(), prices.max(), 11)
cbar = plt.colorbar()
cbar.ax.set_yticklabels(["$%dk"%(round(v/1000)) for v in tick_values], fontsize=14)
cbar.set_label('Median House Value', fontsize=16)

plt.legend(fontsize=16)
save_fig("california_housing_prices_plot")
plt.show()


#%% VISUALIZE: Density waterfall - EXAMPLE

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

#%% VISUALIZE: Density waterfall - Housing

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Create the data
#rs = np.random.RandomState(1979)
#x = rs.randn(500)
#g = np.tile(list("ABCDEFGHIJ"), 50)
#df = pd.DataFrame(dict(x=x, g=g))
#m = df.g.map(ord)
#df["x"] += m

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
#g = sns.FacetGrid(df, row="g", hue="g", aspect=15, size=.5, palette=pal)

# Draw the densities in a few steps
df.map(sns.kdeplot, "x", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
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

#%% VISUALIZE: Pairwise Scatter
#sns.pairplot(df, hue="species")
#sns.pairplot(country_stats)
pairplt = sns.pairplot(df, hue = "ocean_proximity")
path_out = os.path.join(path_data, "pairplot.png")
pairplt.savefig(path_out)


#%% VISUALIZE: Pairwise Density on ALL
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

#%% VISUALIZE: Lat long
#ax = plt.figure(figsize=(20,20))
#df.plot(kind='scatter',x='longitude',y='latitude',alpha=0.1)

df.plot(kind='scatter',x='longitude',y='latitude',alpha=0.4,s=df['population']*0.1,
        c='median_house_value', cmap=plt.get_cmap('jet'), colorbar=True,
        figsize=(20,20))
plt.legend()
path_out = os.path.join(path_data, "colormap.pdf")
plt.savefig(path_out, format='pdf',dpi=600)


#%% OLD CODE BELOW
raise










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

#%% Boxplots
plots=list()
num_boxplots = df_numeric_nonan.shape[1]
#num_boxplots = 2

fig, ax = plt.subplots(nrows=num_boxplots, 
                       ncols=1, 
                       figsize=(20,40), 
                       #figsize=(20,10), 
                       sharex=False, 
                       sharey=False)

for colnum in range(num_boxplots):
    
    # The data
    data_series = df_numeric_nonan.iloc[:,colnum]
    this_mean = data_series.describe()['mean']
    this_median = data_series.describe()['50%']
    this_std =  data_series.describe()['std']
    this_min =  data_series.describe()['min']
    this_max =  data_series.describe()['max']

    # Boxplot    
    sns.boxplot(data_series,
                            ax=ax[colnum],
                            width=0.3,
                            fliersize=2,
                            notch=True,
                            #color=b
                            )

    # Histogram on secondary axis
    second_ax = ax[colnum].twinx()
    #values, base = np.histogram(data_series, bins=100, density=1)
    
    #R(n^(1/3))/(3.49σ)
    num_bins = int(abs(this_max - this_min)*len(data_series)**(1/3)/(3.49*this_std))
    values, base = np.histogram(data_series, bins = num_bins, density=1)
    second_ax.plot(base[:-1], values, '-', linewidth=3, color='blue', alpha=0.5)
    
    # Style
    ax[colnum].grid(color='lightgrey', linestyle='dashed', linewidth=1)
    ax[colnum].axes.get_yaxis().set_visible(False)
    ax[colnum].set_frame_on(False)
    
    # Move title
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


