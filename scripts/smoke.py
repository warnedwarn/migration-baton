import json,re,secrets,time
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
ROOT=Path(__file__).parents[1];ENV=(ROOT.parents[3]/'accounts.env').read_text(encoding='utf-8');DEP=json.loads((ROOT/'deployment.json').read_text())
def v(n):return re.search(rf'^{n}="?([^"\r\n]+)',ENV,re.M).group(1).strip()
def wait(c,h):
 r=c.wait_for_transaction_receipt(transaction_hash=h,status='FINALIZED',retries=180,interval=5000);assert r.get('status_name')=='FINALIZED';return r
owner=create_account(account_private_key=v('ACCOUNT_2_GENLAYER_PRIVATE_KEY'));operator=create_account(account_private_key='0x'+secrets.token_hex(32));co=create_client(chain=studionet,account=owner);cop=create_client(chain=studionet,account=operator);address=DEP['contractAddress'];commit=DEP['sourceCommit'];item='LIVE-'+str(int(time.time()));anchor=f'https://github.com/warnedwarn/migration-baton/raw/{commit}/evidence/rollback-anchor.txt';proofs=[f'https://raw.githubusercontent.com/warnedwarn/migration-baton/{commit}/evidence/checkpoint-one.txt',f'https://cdn.jsdelivr.net/gh/warnedwarn/migration-baton@{commit}/evidence/checkpoint-two.txt',f'https://rawcdn.githack.com/warnedwarn/migration-baton/{commit}/evidence/checkpoint-three.txt'];tx=[];h=co.write_contract(address=address,function_name='plan',args=[item,'Canonical registry migration',operator.address,['Freeze legacy writes','Copy canonical records','Verify destination indexes'],anchor,3600]);wait(co,h);tx.append(h);h=cop.write_contract(address=address,function_name='begin',args=[item]);wait(cop,h);tx.append(h)
for i,url in enumerate(proofs):h=cop.write_contract(address=address,function_name='pass_checkpoint',args=[item,i,url]);wait(cop,h);tx.append(h)
print(json.dumps({'id':item,'state':'COMPLETED','transactions':tx,'operator':operator.address}),flush=True)
