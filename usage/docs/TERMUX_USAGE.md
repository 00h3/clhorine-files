# Chlorine on Termux

Chlorine's filesystem scanner is local and read-only.

Start:
    chlorine

Examples:
    find old files
    find duplicate files
    find my biggest files
    scan my Download folder

Direct:
    chlorine scan /storage/emulated/0/Download
    chlorine stale /storage/emulated/0/Download
    chlorine large /storage/emulated/0/Download
    chlorine duplicates /storage/emulated/0/Download
