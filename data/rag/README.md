---
viewer: false
license: mit
language:
  - en
  - hi
size_categories:
  - 1K<n<10K
tags:
  - insurance
  - india
  - bfsi
  - rag
---

# insurance-bot-data

Companion dataset for [rohitsar567/InsuranceBot](https://huggingface.co/spaces/rohitsar567/InsuranceBot) — a voice-first AI advisor for Indian health insurance.

## Contents

- `rag/corpus/**.pdf` — 208 policy documents from 19 insurers + IRDAI master circulars.
- `rag/vectors/**` — pre-built Chroma HNSW index (BGE-small-en-v1.5 embeddings).
- `rag/extracted/**.json` — structured fact cards (62 schema fields per policy) produced by the BFSI extraction pipeline.
- `40-data/**` — runtime metadata + per-policy review / premium / facts JSONs.

## Why viewer is disabled

This dataset is a curated multi-format artifact (PDFs, binary Chroma index, heterogeneous JSON schemas), not a tabular dataset. The HF dataset viewer expects a uniform tabular schema and emits `StreamingRowsError: CastError` when trying to auto-parquet our JSONs. Disabling the viewer (`viewer: false`) is the canonical fix for this shape.

## Consumption

The HF Space pulls this dataset at Docker build time via `huggingface_hub.snapshot_download` (`repo_type="dataset"`, no token needed; public). See the Space's Dockerfile.

## License

MIT — same as the companion Space.
