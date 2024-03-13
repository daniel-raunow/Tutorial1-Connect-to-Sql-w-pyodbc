import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

#Retrieve password from Azure Key Vault
keyVaultName ='kv-tutorial-d'
KVUri = f"https://{keyVaultName}.vault.azure.net"
secretName = "sqladmin-pass"

credential = DefaultAzureCredential(exclude_environment_credential = True, exclude_managed_identity_credential = True, exclude_shared_token_cache_credential = True, exclude_visual_studio_code_credential = False)
client = SecretClient(vault_url=KVUri, credential=credential)

retrieved_secret = client.get_secret(secretName)


#Connect to SQL Database
driver = "{ODBC Driver 17 for SQL Server}" 
server = "tcp:pythonsqlconn.database.windows.net,1433"
database = "tutorialdb"
username = "sqlconnadmin"
password = retrieved_secret.value
conn_string = f"Driver={driver};Server={server};Database={database};UID={username};PWD={password}"

connection: pyodbc.Connection = pyodbc.connect(conn_string)

#Execute query        
query = "SELECT * FROM dbo.python_data;"
cursor_object : pyodbc.Cursor = connection.cursor()
cursor_object.execute(query)
result = cursor_object.fetchall()

for item in result: print(item)
