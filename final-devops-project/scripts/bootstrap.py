"""Create only the namespace and external database Secret; credentials use stdin."""
import argparse,json,secrets,subprocess
parser=argparse.ArgumentParser();parser.add_argument('--namespace',default='session21');args=parser.parse_args()
ns=args.namespace
subprocess.run(['kubectl','apply','-f','-'],input=json.dumps({'apiVersion':'v1','kind':'Namespace','metadata':{'name':ns}}),text=True,check=True)
exists=subprocess.run(['kubectl','get','secret','labledger-db','-n',ns],capture_output=True).returncode==0
if not exists:
    password=secrets.token_urlsafe(24)
    data={'POSTGRES_USER':'ledger','POSTGRES_DB':'ledger','POSTGRES_PASSWORD':password,'DATABASE_URL':f'postgresql+psycopg://ledger:{password}@postgres:5432/ledger'}
    secret={'apiVersion':'v1','kind':'Secret','metadata':{'name':'labledger-db','namespace':ns},'type':'Opaque','stringData':data}
    subprocess.run(['kubectl','apply','-f','-'],input=json.dumps(secret),text=True,check=True)
print('Namespace and external database Secret ready; credentials omitted')
