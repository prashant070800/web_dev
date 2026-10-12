---
title: Infosys
summary: RAG API for semantic search over enterprise documents, and LLM data workflows.
order: 3
company: Infosys
role: Software Engineer
period: Aug 2022 — Aug 2024
tech: [python, flask, rag, milvus, angular, gcp]
questions:
  - q: "How did your RAG API work?"
    a: |
      A Flask API over a Milvus vector store: documents were embedded and indexed, and
      each query was embedded, matched against the most similar chunks, and those chunks
      were passed to the LLM as context, which enabled semantic search over large
      enterprise document corpora.

      TODO: add chunking and embedding details.
---

## Role & team

TODO

## What I built

TODO: the RAG API; dataset preparation and fine-tuning workflows (data cleaning, prompt
engineering, evaluation); the Angular Smart City demo; GCP deployments.

## Impact

TODO
