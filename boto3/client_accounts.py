import boto3
import json 

session = boto3.Session()
client = session.client('organizations')


aws_accounts = list()
ou_r = client.list_accounts()
we_accounts = {}
while True:
    for acct in ou_r['Accounts']:
        aws_accounts.append(acct['Name'])
        we_accounts[acct['Id']] = acct['Name']
    if 'NextToken' in ou_r:
        ou_r = client.list_accounts(NextToken=ou_r['NextToken'])
    else:
        break

accounts_json = json.dumps(we_accounts)

print(accounts_json)

