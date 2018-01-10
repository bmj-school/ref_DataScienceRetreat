#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Standard modules
#===============================================================================

#===============================================================================
#--- SETUP external modules
#===============================================================================

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.util_inspect import get_self

#===============================================================================
#--- MAIN CODE
#===============================================================================

#--- Set Pandas options
pd.set_option('display.height', 500)
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

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

def write_sheet():
    pass

def write_book(excel_path, df, sheet_name):
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    writer.save()
    logging.debug("Wrote df to book at {}".format(excel_path))

def write_pickle(pck_path, df):
    df.to_pickle(pck_path, compression='infer')
    logging.debug("Wrote df to pickle at {}".format(pck_path))

ROOT_PATH = r"C:\EXPORT\\"
EXCEL_PATH = r"C:\EXPORT\titanic.xlsx"

def load_write_data():
    titanic_df = pd.read_csv("./data/train.csv")
    titanic_df.name = 'Titanic data'
    logging.debug("Loaded {}, {} rows".format(titanic_df.name, titanic_df.shape))
    write_pickle(ROOT_PATH+"titanic_df.pck", titanic_df)
    
    test_df    = pd.read_csv("./data/test.csv")
    test_df.name = 'Titanic test data'
    logging.debug("Loaded {}, {}".format(test_df.name, test_df.shape))
    write_pickle(ROOT_PATH+"test_df.pck", titanic_df)
  
def reload_data():
    dfs = dict()
    dfs['titan_df'] = pd.read_pickle(ROOT_PATH+"titanic_df.pck")
    logging.debug("Loaded {}".format('titan_df'))

    dfs['test_df'] = pd.read_pickle(ROOT_PATH+"test_df.pck")
    logging.debug("Loaded {}, {}".format('test_df',dfs['test_df'].shape))
    
    return dfs

def display_df(df):
    print("\n*** DATAFRAME ***".format(df.name))
    print(df)
    print("\n")

def run():
    #--- Get DFs, full and test
    #load_write_data()
    
    #--- Reload & rename data
    dfs = reload_data()
    titanic_df = dfs['titan_df']
    titanic_df.name = 'titanic_df'
    test_df = dfs['test_df']
    test_df.name = 'test_df'
    
    # Display
    #display_df(titanic_df)
    print(titanic_df.info())

    # Some 'age' elements are missing
    # Many 'cabin' elements are MISSING
    # A couple 'embarked' are missing

    #--- STEP 1: Discard 
    
    raise


    
    print(titanic_df['Embarked'])
    
    # Select Embarked = 
    #new = this_df['Embarked'] == None
    #print(new)
    
    raise
    # In[74]:
    
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
    
    
    book = openpyxl.load_workbook(excel_path)
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
    
    df2 = pd.DataFrame(df.row.str.split(' ',1).tolist(),
                                       columns = ['flips','row'])
    

if __name__ == "__main__":
    run()
