from conftest import CONTRACT
STOPS=['Freeze legacy writes','Copy canonical records','Verify destination indexes']
def setup(vm,deploy,alice,bob):
 vm.warp('2035-01-01T00:00:00+00:00');vm.sender=alice;c=deploy(CONTRACT);c.plan('mig-7','Canonical registry migration','0x'+bob.hex(),STOPS,'https://anchor.example/rollback',3600);return c
def proof(vm,host):
 vm.mock_web(r'anchor\.example',{'status':200,'body':'rollback snapshot digest 55aa'});vm.mock_web(host.replace('.','\\.'),{'status':200,'body':'checkpoint complete; rollback anchor intact'});vm.mock_llm(r'.*MigrationBaton checkpoint inspection.*','{"passes":true,"anchor_intact":true}')
def test_non_skippable_route_completes(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob;c.begin('mig-7')
 for i,h in enumerate(('one.example','two.example','three.example')):proof(direct_vm,h);c.pass_checkpoint('mig-7',i,'https://'+h+'/proof')
 assert c.get_migration('mig-7')['state']=='COMPLETED' and len(c.get_migration('mig-7')['digests'])==3
def test_cannot_skip_station(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob;c.begin('mig-7');proof(direct_vm,'two.example')
 with direct_vm.expect_revert('next checkpoint'):c.pass_checkpoint('mig-7',1,'https://two.example/proof')
def test_validator_rejects_broken_anchor_claim(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob;c.begin('mig-7');proof(direct_vm,'one.example');x=c.migrations['MIG-7'];result=c._verify_stop(x,0,'https://one.example/proof');assert direct_vm.run_validator(leader_result=result) is True;forged=dict(result);forged['anchor_intact']=False;assert direct_vm.run_validator(leader_result=forged) is False
def test_permissionless_expiry(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob);direct_vm.sender=direct_bob;c.begin('mig-7');direct_vm.warp('2035-01-01T01:01:00+00:00');direct_vm.sender=direct_alice;c.expire('mig-7');assert c.get_migration('mig-7')['state']=='EXPIRED'
