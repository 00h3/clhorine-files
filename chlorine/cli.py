from __future__ import annotations
import sys
from pathlib import Path
from .core.scanner import scan, find_stale, find_large, find_duplicates

def size(n):
    x=float(n)
    for u in ("B","KB","MB","GB","TB"):
        if x<1024 or u=="TB": return f"{x:.1f} {u}" if u!="B" else f"{int(x)} B"
        x/=1024

def default_path():
    for p in (Path("/storage/emulated/0/Download"), Path.home()/"storage"/"downloads", Path.cwd()):
        if p.exists(): return p
    return Path.cwd()

def path_from(q):
    p=Path(q).expanduser()
    return p if p.is_absolute() else Path.cwd()/p

def stale(p, days=90):
    rows=sorted(find_stale(p,days), key=lambda r:r.size, reverse=True)
    print(f"\nScanning {p} ...")
    if not rows: print(f"No files older than {days} days found."); return
    print(f"\nFOUND {len(rows)} stale files\n")
    for r in rows[:50]: print(f"{size(r.size):>10}  {r.age_days:>6.0f} days  {r.path}")
    if len(rows)>50: print(f"\n...and {len(rows)-50} more.")

def large(p):
    rows=sorted(find_large(p), key=lambda r:r.size, reverse=True)
    print(f"\nScanning {p} ...")
    if not rows: print("No files >= 100 MB found."); return
    print("\nLARGEST FILES\n")
    for r in rows[:50]: print(f"{size(r.size):>10}  {r.path}")

def dupes(p):
    groups=find_duplicates(p)
    print(f"\nChecking duplicates in {p} ...")
    if not groups: print("No duplicate files found."); return
    print(f"\nFOUND {len(groups)} duplicate groups\n")
    for i,g in enumerate(groups[:30],1):
        print(f"Group {i}: {size(g[0].size)} each; recoverable: {size(sum(r.size for r in g[1:]))}")
        for r in g: print(f"  {r.path}")
        print()

def natural(q):
    low=q.lower()
    p=default_path()
    if " in " in low:
        cand=q[low.rfind(" in ")+4:].strip().strip("\"'")
        cp=path_from(cand)
        if cp.exists(): p=cp
    if " duplicate" in low or "duplicates" in low: return dupes(p)
    if any(x in low for x in ("biggest","largest","taking up","space")): return large(p)
    if any(x in low for x in ("old","stale","unused","unnecessary","not used")): return stale(p)
    if any(x in low for x in ("scan","analyze","analyse","inspect")):
        rows=scan(p); print(f"\nScanned {p}\nFiles: {len(rows)}\nTotal size: {size(sum(r.size for r in rows))}\nNothing was modified."); return
    print("\nI understood the request, but no safe filesystem action is mapped yet.")
    print("Try: find old files, find duplicate files, find biggest files, or scan Download.")

def main():
    if len(sys.argv)>1:
        if sys.argv[1] in {"-h","--help","help"}:
            print("Chlorine filesystem intelligence\n\nchlorine\nchlorine scan PATH\nchlorine stale PATH\nchlorine large PATH\nchlorine duplicates PATH"); return
        cmd=sys.argv[1].lower(); p=path_from(sys.argv[2]) if len(sys.argv)>2 else default_path()
        if cmd=="scan": rows=scan(p); print(f"Scanned {p}: {len(rows)} files, {size(sum(r.size for r in rows))}")
        elif cmd in {"stale","old"}: stale(p)
        elif cmd in {"large","biggest"}: large(p)
        elif cmd in {"duplicates","dupes"}: dupes(p)
        else: natural(" ".join(sys.argv[1:]))
        return
    print("\nCHLORINE\nNEW FILESYSTEM INTELLIGENCE SYSTEM\nL+ LANGUAGE     ONLINE\nFS INTELLIGENCE ONLINE\nCHLORINE GUARD ACTIVE\nQUARANTINE      READY\n")
    while True:
        try: q=input("chlorine> ").strip()
        except (EOFError,KeyboardInterrupt): print("\nbye."); break
        if not q: continue
        if q.lower() in {"exit","quit"}: break
        if q.lower() in {"help","?"}:
            print("Try: find old files | find duplicate files | find my biggest files | scan my Download folder"); continue
        if q.lower().startswith("ask "): q=q[4:].strip()
        try: natural(q)
        except Exception as e: print(f"\nScan failed: {e}")

if __name__=="__main__": main()
