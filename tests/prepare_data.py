from pathlib import Path
import argparse

p=argparse.ArgumentParser()
p.add_argument("--input",default="data")
p.add_argument("--output",default="data/lplus_corpus.txt")
a=p.parse_args()

root=Path(a.input); out=Path(a.output)
parts=[]
for f in root.rglob("*.txt"):
    if f.resolve()==out.resolve(): continue
    try:
        text=f.read_text(encoding="utf-8",errors="ignore")
        if text.strip(): parts.append(text)
    except OSError: pass
if not parts:
    raise SystemExit("No text files found.")
text="\n\n".join(parts)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(text,encoding="utf-8")
print(f"prepared {len(text):,} characters -> {out}")
