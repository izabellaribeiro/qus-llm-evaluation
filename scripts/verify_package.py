"""Verify distributed file hashes and optional reproduced CSV contents."""
import argparse,csv,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def table(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);return reader.fieldnames,Counter(tuple(sorted(r.items())) for r in reader)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--reproduced-root',type=Path);args=parser.parse_args()
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for name,expected in manifest['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    compared=0
    if args.reproduced_root:
        for original in (ROOT/'results').rglob('*.csv'):
            reproduced=args.reproduced_root/original.relative_to(ROOT)
            assert reproduced.exists() and table(original)==table(reproduced),str(original)
            compared+=1
    print('PASS:',len(manifest['sha256']),'file hashes;',compared,'result CSV comparisons')
if __name__=='__main__':main()
