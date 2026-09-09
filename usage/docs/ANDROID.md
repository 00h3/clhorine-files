# Android / Termux

Install Python in Termux, then from the extracted project:

    pkg update
    pkg install python
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .

Use lightweight filesystem/web features:

    chlorine search "how transformers work"
    chlorine ask "find my biggest files"

Neural training requires PyTorch. Android builds of PyTorch vary by device, so the recommended workflow is to train on a PC/cloud GPU and copy a checkpoint to the phone for inference.

Do not give Chlorine unrestricted storage permissions unless you understand what the app can access.
