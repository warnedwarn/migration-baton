from pathlib import Path
TEXT=Path('contracts/contract.py').read_text(encoding='utf-8');PAGE=Path('docs/index.html').read_text(encoding='utf-8')
def test_surface():
 for n in ('plan','begin','pass_checkpoint','roll_back','expire','get_migration'):assert 'def '+n in TEXT and n in PAGE
 assert "status:'FINALIZED'" in PAGE
 assert 'id="metroMap"' in PAGE and 'id="stationDrawer"' in PAGE and 'id="baton"' in PAGE
 assert 'specimenTray' not in PAGE and 'Deployment pending' not in PAGE
 assert 'CONTRACT_ADDRESS' not in PAGE and 'DEMO_ANCHOR_URL' not in PAGE
 assert '0x034E9Eee99952623459016974dD9b97F35369e7D' in PAGE
