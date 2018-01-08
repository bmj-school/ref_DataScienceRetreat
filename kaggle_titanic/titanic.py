
# coding: utf-8

# In[45]:

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib inline')


# In[48]:

# get titanic & test csv files as a DataFrame
titanic_df = pd.read_csv("./data/train.csv")
test_df    = pd.read_csv("./data/test.csv")

# preview the data
titanic_df.head()


# Variable	Definition	Key
# survival	Survival	0 = No, 1 = Yes
# pclass	Ticket class	1 = 1st, 2 = 2nd, 3 = 3rd
# sex	Sex	
# Age	Age in years	
# sibsp	# of siblings / spouses aboard the Titanic	
# parch	# of parents / children aboard the Titanic	
# ticket	Ticket number	
# fare	Passenger fare	
# cabin	Cabin number	
# embarked	Port of Embarkation	C = Cherbourg, Q = Queenstown, S = Southampton

# In[26]:

summary_df = pd.DataFrame(titanic_df.describe())
summary_df
#print(titanic_df.describe())


# In[36]:

info_df = pd.DataFrame(titanic_df.info())


# In[38]:

def get_title(name):
    # Split the title from the name 
    if '.' in name:
        return name.split(',')[1].split('.')[0].strip()
    else:
        return 'Unknown'

def title_map(title):
    # Map the title to a number
    if title in ['Mr']:
        return 1
    elif title in ['Master']:
        return 3
    elif title in ['Ms','Mlle','Miss']:
        return 4
    elif title in ['Mme','Mrs']:
        return 5
    else:
        return 2


# **Apply the mappings**

# In[46]:

titanic_df['title'] = titanic_df['Name'].apply(get_title).apply(title_map)   
test_df['title'] = test_df['Name'].apply(get_title).apply(title_map)
title_xt = pd.crosstab(titanic_df['title'], titanic_df['Survived'])
title_xt_pct = title_xt.div(title_xt.sum(1).astype(float), axis=0)

title_xt_pct.plot(kind='bar', 
                  stacked=True, 
                  title='Survival Rate by title')
plt.xlabel('title2')
plt.ylabel('Survival Rate')

