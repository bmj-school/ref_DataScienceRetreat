import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib inline')

from openpyxl import load_workbook

import seaborn as sb

excel_path = r"C:\EXPORT\titanic.xlsx"


# In[69]:


# get titanic & test csv files as a DataFrame
titanic_df = pd.read_csv("./data/train.csv")
test_df    = pd.read_csv("./data/test.csv")

small_df = titanic_df.iloc[:5]
# preview the data
titanic_df.head()


# **Write the original data**

# In[70]:


writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
#with writer: 
titanic_df.to_excel(writer, sheet_name='original')
writer.save()


# In[71]:


small_df


# Variable|Definition|Key
# -		|-|-
# Survived|Survival|0 = No, 1 = Yes
# Pclass	|Ticket class|1 = 1st, 2 = 2nd, 3 = 3rd
# Name	| 
# Sex		|Sex
# Age		|Age in years
# SibSp	|# of siblings / spouses aboard the Titanic
# Parch	|# of parents / children aboard the Titanic
# Ticket	|Ticket number	
# Fare	|Passenger fare
# Cabin	|Cabin number
# Embarked|Port of Embarkation|C = Cherbourg, Q = Queenstown, S = Southampton

# In[72]:


summary_df = pd.DataFrame(titanic_df.describe())
summary_df
#print(titanic_df.describe())


# In[73]:


info_df = pd.DataFrame(titanic_df.info())


# In[74]:


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
    elif title in ['Rev']:
        return 6    
    else:
        return 2


# **Split the TITLE Mr / Master / Ms / Mlle / Miss **

# In[75]:


# Get the Name column. 
# For each element, get the title by checking for '.' then SPLIT on ','
# Return the series to a new column called 'title' in the DF
titanic_df['title'] = titanic_df['Name'].apply(get_title)
titanic_df[['PassengerId','Name','title']].head()


# In[76]:


# Use a case/swtich function to map class to an integer 1-5
titanic_df['title_int'] = titanic_df['title'].apply(title_map)
titanic_df.head()


# In[77]:


book = load_workbook(excel_path)
writer = pd.ExcelWriter(excel_path, engine = 'openpyxl')
writer.book = book
titanic_df.to_excel(writer, sheet_name='Split title')
writer.save()
writer.close()


# In[ ]:


#title_xt = pd.crosstab(titanic_df['title'], titanic_df['Survived'])
#title_xt_pct = title_xt.div(title_xt.sum(1).astype(float), axis=0)
#
#title_xt_pct.plot(kind='bar', 
#                  stacked=True, 
#                  title='Survival Rate by title')
#plt.xlabel('title')
#plt.ylabel('Survival Rate')


# In[ ]:


# We have to temporarily drop the rows with 'NA' values
# because the Seaborn plotting function does not know
# what to do with them
#fig = sb.pairplot(titanic_df.dropna());


# In[15]:


#fig.savefig(r"C:\EXPORT\titanic pair plot.png")


# In[20]:





# Original data

# In[23]:


writer = pd.ExcelWriter(r"C:\EXPORT\titanic.xlsx")
titanic_df.to_excel(writer,'Sheet5')
writer.save()


# Split names

# In[31]:


df = small_df
df


# In[35]:


# Get the name col
df['Name']
# OR: 
df.Name


# In[55]:


#Get the split names as a 2D table
split_names = df.Name.str.split(',',n=1,expand=False).tolist()
#Put this into a new DF
new = [row[1] for row in split_names]
new


# In[57]:


df2 = pd.DataFrame(df.row.str.split(' ',1).tolist(),
                                   columns = ['flips','row'])


# In[ ]:


# See regex help: 
# https://regexr.com/

