print_imports()
import os

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

#plt.rcParams['axes.labelsize'] = 14
#plt.rcParams['xtick.labelsize'] = 12
#plt.rcParams['ytick.labelsize'] = 12

sns.set(style="ticks")


#%% ===========================================================================
#  Paths
# =============================================================================
PATH_DATA_ROOT = r"/home/batman/git/handson-ml/"
path_data = os.path.join(PATH_DATA_ROOT, "datasets", "lifesat", "")
assert os.path.exists(path_data)

# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "fundamentals"

#%% ===========================================================================
# Functions
# =============================================================================
def save_fig(fig_id, tight_layout=True):
    path = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID, fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)

def prepare_country_stats(oecd_bli, gdp_per_capita):
    oecd_bli = oecd_bli[oecd_bli["INEQUALITY"]=="TOT"]
    oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
    gdp_per_capita.rename(columns={"2015": "GDP per capita"}, inplace=True)
    gdp_per_capita["GDP per capita"] = gdp_per_capita["GDP per capita"].astype('float')
    gdp_per_capita.set_index("Country", inplace=True)
    full_country_stats = pd.merge(left=oecd_bli, right=gdp_per_capita,
                                  left_index=True, right_index=True)
    full_country_stats.sort_values(by="GDP per capita", inplace=True)
    remove_indices = [0, 1, 6, 8, 33, 34, 35]
    keep_indices = list(set(range(36)) - set(remove_indices))
    return full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]

#%% ===========================================================================
# MAIN
# =============================================================================
    
# Load data
oecd_bli = pd.read_csv(path_data+"oecd_bli_2015.csv", thousands = ',')
gdp_fname = path_data + "gdp_per_capita.csv"
gdp_per_capita = pd.read_csv(gdp_fname,
                             #thousands = '.',
                             thousands = ',',
                             delimiter='\t',
                             encoding='latin1',
                             na_values=r"n/a")

country_stats = prepare_country_stats(oecd_bli, gdp_per_capita)
#country_stats.dtypes

#%% Scatter

#sns.pairplot(df, hue="species")
sns.pairplot(country_stats)

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

#%% Scatter plot

X = np.c_[country_stats["GDP per capita"]]
y = np.c_[country_stats["Life satisfaction"]]
# Plot
country_stats.plot(kind='scatter',x="GDP per capita",y="Life satisfaction")

#%% Linear model
lin_reg_model = sk.linear_model.LinearRegression()
lin_reg_model.fit(X,y)

X_new = [[22587]]
lin_reg_model.predict(X_new)

#%% k Nearest Neighbours
y_1D = np.ravel(y,order='C')
y_class = country_stats.index

clf = sk.neighbors.KNeighborsClassifier(n_neighbors=3)
clf = sk.neighbors.KNeighborsClassifier(n_neighbors=2)
clf = sk.neighbors.KNeighborsClassifier(n_neighbors=1)
clf.fit(X,y_class)
X_new = [[22587]]
clf.predict(X_new)

