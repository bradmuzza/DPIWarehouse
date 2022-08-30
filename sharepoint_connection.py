
#%%
import json ,os
from importlib_metadata import version 
import pandas 
from shareplum import Site, Office365
from shareplum.site import Version 
from requests_ntlm import HttpNtlmAuth
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
import sharepy

# %% 
with open("Sharepoint_settings.json","r") as j:
    config =  json.load(j)

client_creds= ClientCredential(config["ClientID"], config["ClientSecert"])
ctx = ClientContext(config['Site']).with_credentials(client_creds)
# .with_user_credentials(config['UserName'], password=config['Password'])

file_url =  os.path.join(config['url'], r"/sites/MST_DPI_RBE_BusinessStrategyPerformance/Shared 20Documents/Strategic Planning/Team tasks 20May June.xlsx")

ctx.web.get().execute_query()

# with open(r'C:\Users\murrab01\OneDrive - DPIE\Documents\Python Scripts\Database ETL\Sharepoint_files') as local:
#ctx.web.get_file_by_server_relative_path(file_url).download(r'C:\Users\murrab01\OneDrive - DPIE\Documents\Python Scripts\Database ETL\Sharepoint_files').execute_query()
#%%
print(ctx.web._properties)

# with open()
# def auth(): 
#      authcookie = Office365(config['url'], username= config['UserName'], password=config['Password']).GetCookies()

#      return Site(config['Site'],authcookie= authcookie,version=Version.v2019)
# auth()  
# %%


# %%
pandas.read_excel("https://environmentnswgov.sharepoint.com/sites/MST_DPI_RBE_BusinessStrategyPerformance/Shared%20Documents/Strategic%20Planning/Team%20tasks%20-%20May&June.xlsx?web=1")

# %%
s = sharepy.connect(config['url'], username=config['UserName'], password=config['Password'])
file_url =  os.path.join(config['url'], r"sites/MST_DPI_RBE_BusinessStrategyPerformance/Shared 20Documents/Strategic Planning/Team tasks May&June June.xlsx")
r = s.get(file_url)
# %%
