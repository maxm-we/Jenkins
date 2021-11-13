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
        we_accounts[acct['Id']] = acct['Name'].replace("AWS-", "")
    if 'NextToken' in ou_r:
        ou_r = client.list_accounts(NextToken=ou_r['NextToken'])
    else:
        break

account_list = list(we_accounts.values())
accounts_json = json.dumps(account_list)
print(accounts_json)

