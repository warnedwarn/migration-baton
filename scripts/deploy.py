import json,re
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
ROOT=Path(__file__).parents[1];ENV=(ROOT.parents[3]/'accounts.env').read_text(encoding='utf-8')
def v(n):return re.search(rf'^{n}="?([^"\r\n]+)',ENV,re.M).group(1).strip()
def find(x):
 if isinstance(x,dict):
  if x.get('contract_address'):return x['contract_address']
  for y in x.values():
   z=find(y)
   if z:return z
 if isinstance(x,list):
  for y in x:
   z=find(y)
   if z:return z
assert v('ACCOUNT_2_GITHUB_USERNAME')=='warnedwarn';a=create_account(account_private_key=v('ACCOUNT_2_GENLAYER_PRIVATE_KEY'));c=create_client(chain=studionet,account=a);h=c.deploy_contract(code=(ROOT/'contracts'/'contract.py').read_text(encoding='utf-8'),args=[]);print('deploy_tx='+h,flush=True);r=c.wait_for_transaction_receipt(transaction_hash=h,status='FINALIZED',retries=180,interval=5000);address=find(r);assert address;print(json.dumps({'contract':address,'transaction':h,'wallet':a.address,'status':r.get('status_name')},default=str),flush=True)
