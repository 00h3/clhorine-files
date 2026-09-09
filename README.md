# chlorine

Chlorine is a local-first filesystem intelligence assistant with its own L+ language layer.

This update moves L+ from the old statistical prototype toward a real decoder-only Transformer architecture while keeping the old lightweight model available as a fallback.

The project now has four layers:

    user
      |
      v
    Chlorine chat/UI
      |
      +---- L+ language model
      |
      +---- live web search / page retrieval
      |
      +---- filesystem tools
      |
      v
    safety + quarantine

L+ can generate text, but Chlorine does not blindly execute generated text. Tool calls go through an explicit intent and safety layer.

## What changed

- L+ tiny GPT-style decoder-only Transformer
- byte-level tokenizer with special tokens
- causal self-attention
- feed-forward blocks
- residual connections
- layer normalization
- AdamW training
- gradient clipping
- checkpoints
- validation split
- temperature / top-k / top-p generation
- live web search command
- web page text retrieval
- source-aware answers
- filesystem scan, duplicates, large files, old files
- quarantine and restore
- digital terminal interface
- old trigram model kept as `chlorine.lplus.legacy`
- 52,000 original training lines
- scripts for adding public-domain/local data
- no model weights are pretended to be "ChatGPT quality"

## Important reality check

A small Transformer trained on a phone or normal laptop will not become ChatGPT by itself. Real LLM pretraining needs vastly more data and compute. Hugging Face's own from-scratch course demonstrates the full pipeline but notes that pretraining from scratch requires considerably more compute than fine-tuning. PyTorch provides the core Transformer building blocks.

This repository gives Chlorine a real, runnable learning architecture so it can be trained and improved rather than pretending a trigram model is a modern LLM.

## Install

    python -m venv .venv
    source .venv/bin/activate
    pip install -e .

For the neural model:

    pip install -e ".[train]"

On Android, use Termux. The lightweight tools work there; neural training is better done on a PC/cloud GPU.

## Train the real L+

First prepare data:

    python scripts/prepare_data.py

Train a tiny model:

    python scripts/train_lplus.py \
      --data data/lplus_corpus.txt \
      --out checkpoints/lplus \
      --steps 2000

Then chat:

    chlorine chat --model checkpoints/lplus

The default configuration is deliberately small enough for experimentation.

## Live web search

Chlorine can search the public web from the command line:

    chlorine search "how does a transformer language model work"

It returns titles, URLs, and snippets.

To retrieve readable page text:

    chlorine fetch "https://example.com"

The search layer is intentionally separate from L+. This means live facts do not have to be baked into model weights.

## Natural language filesystem commands

    chlorine

Examples:

    please find my biggest files
    find duplicate downloads
    show me old project files
    scan this folder
    please delete this

For destructive requests Chlorine creates a proposal and asks for confirmation. Approved files are moved to quarantine instead of being permanently unlinked.

## Data

The included 52,000-line corpus is original generated training material. It is included so the project works immediately without redistributing a copyrighted scraped corpus.

For better training, add data you have the right to use. The data preparation script can combine local text files and public-domain material you download yourself.

## Real LLM path

The practical path is:

1. collect legally usable text
2. clean and deduplicate it
3. train a tokenizer
4. tokenize into fixed context windows
5. train a decoder-only Transformer with next-token prediction
6. validate loss/perplexity
7. checkpoint frequently
8. instruction-tune on instruction/response data
9. evaluate on held-out prompts
10. quantize for mobile inference
11. add retrieval and tool calling

This is the same broad family of steps used in modern LLM development. A tiny model is a learning and engineering target, not a claim of frontier capability.

## Sources

The design was checked against current PyTorch and Hugging Face documentation:

- PyTorch Transformer API: https://docs.pytorch.org/docs/stable/generated/torch.nn.Transformer.html
- Hugging Face training guide: https://huggingface.co/docs/transformers/en/training
- Hugging Face from-scratch causal LM course: https://huggingface.co/docs/course/chapter7/6
- Hugging Face tokenizer course: https://huggingface.co/learn/llm-course/en/chapter6/1

## License

MIT. See LICENSE.
