# L+ architecture

L+ is a decoder-only Transformer.

Core path:

tokens -> token embeddings + positional embeddings -> repeated Transformer blocks -> vocabulary logits

Each block:

LayerNorm
  |
causal self-attention
  |
residual
  |
LayerNorm
  |
GELU feed-forward network
  |
residual

Training target:

input:  "hello worl"
target: "ello world"

The loss is cross-entropy over the next token.

The included implementation is intentionally small. It demonstrates the real mechanics of a GPT-style causal language model without pretending that a tiny model is equivalent to a production frontier model.

For production scale, the project would need a stronger tokenizer, much larger and legally sourced corpus, distributed training, mixed precision, checkpoint sharding, evaluation, instruction tuning, preference optimization, safety evaluation, and optimized inference.
