import argparse
import botocore
import boto3
import json
import datetime
from dateutil.tz import tzlocal

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--client", help = "client name", required=True)
parser.add_argument("-a", "--account", help = "client account number", required=True)
args = parser.parse_args()

client = args.client
account = args.account

assume_role_cache: dict = {}
def assumed_role_session(role_arn: str, base_session: botocore.session.Session = None):
    base_session = base_session or boto3.session.Session()._session
    fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
        client_creator = base_session.create_client,
        source_credentials = base_session.get_credentials(),
        role_arn = role_arn,
        extra_args = {
        #    'RoleSessionName': None # set this if you want something non-default
        }
    )
    creds = botocore.credentials.DeferredRefreshableCredentials(
        method = 'assume-role',
        refresh_using = fetcher.fetch_credentials,
        time_fetcher = lambda: datetime.datetime.now(tzlocal())
    )
    botocore_session = botocore.session.Session()
    botocore_session._credentials = creds
    return boto3.Session(botocore_session = botocore_session)

#session = assumed_role_session('arn:aws:iam::ACCOUNTID:role/ROLE_NAME')
try:
    #session = assumed_role_session('arn:aws:iam::'+ account + ':role/' + client)
    session = assumed_role_session('arn:aws:iam::'+ account + ':role/s3-cross-account')


    s3 = session.client('s3')
    response = s3.list_buckets()

    exclude_buckets = ['waf', 'internal', 'awsconfig', 'datadog', 'cf-templates', 'we-dms', '-dr', '-west-', 'terraform', '-lambda', '-west', '-sql-backups', '-creation-stack']

    use_buckets = []
    databases = []

    for bucket in response['Buckets']:
        if not any(bs in bucket["Name"] for bs in exclude_buckets):
            use_buckets.append(bucket["Name"])

    for use_bucket in use_buckets:
        response = s3.list_objects_v2(Bucket=use_bucket, Delimiter = '/', Prefix = 'SQLBackups/')
        try:
            for prefix in response['CommonPrefixes']:
                if 'cs-Audit' not in prefix['Prefix'][:-1] and 'cs-cognos11' not in prefix['Prefix'][:-1] and 'dba_utils' not in prefix['Prefix'][:-1] and 'master' not in prefix['Prefix'][:-1] and 'master_seed' not in prefix['Prefix'][:-1]:
                    databases.append(prefix['Prefix'][:-1].replace('SQLBackups/', ''))
                    backup_bucket = use_bucket
        except: 
            pass
        
    if databases:
        json = json.dumps({"databases": databases, "bucket": backup_bucket })
        print(json)
except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
    

