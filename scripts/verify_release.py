"""Verify public release contents without third-party data."""
from pathlib import Path
import hashlib,json,csv
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST.json').read_text())
for name,digest in manifest['files'].items():
    p=Path(name)
    assert not p.is_absolute() and '..' not in p.parts
    assert hashlib.sha256((root/p).read_bytes()).hexdigest()==digest,name
required=['register/AECS_final_27_corpus_register.csv','coding/codebook.md',
'review/closeout_20261104/human_coding/FIRST_PASS_FROZEN.csv',
'data/coding/independent_coding.csv','scripts/verified_analysis.py',
'scripts/crossed_rating_reml.py','scripts/consensus_transfer.py',
'results/rating_input_manifest_20261108.json','DATA.md']
assert all((root/name).is_file() for name in required)
for name in [required[0],required[2],required[3]]:
    with (root/name).open(encoding='utf-8-sig',newline='') as f:
        assert len(list(csv.DictReader(f)))==27,name
assert not list(root.glob('cache/*')),'Restricted input included'
secondary=json.loads((root/'research_quality_audit_20261113/intercoder_agreement/pre_adjudication_agreement.json').read_text(encoding='utf-8'))['secondary_field']['release_description']
assert secondary['total_comparisons']==21 and secondary['agreements']==6
assert secondary['raw_agreement_rate']==0.2857 and secondary['kappa']==0.1463
assert secondary['sensitivity_both_definite']['retained']==5
assert secondary['sensitivity_both_definite']['raw_agreement_rate']==0.8
print('Manifest and coding denominator verified:',len(manifest['files']),'files')
