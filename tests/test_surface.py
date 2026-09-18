from pathlib import Path
TEXT=Path('contracts/contract.py').read_text(encoding='utf-8');PAGE=Path('docs/index.html').read_text(encoding='utf-8')
def test_surface():
 for n in ('plan','begin','pass_checkpoint','roll_back','expire','get_migration'):assert 'def '+n in TEXT and n in PAGE
 assert "status:'FINALIZED'" in PAGE
 assert 'id="metroMap"' in PAGE and 'id="stationDrawer"' in PAGE and 'id="baton"' in PAGE
 assert 'specimenTray' not in PAGE and 'Deployment pending' not in PAGE
