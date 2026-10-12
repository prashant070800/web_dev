---
title: JAXL
summary: Call Campaign Engine, telephony integrations, and PostgreSQL performance work.
order: 2
company: JAXL
role: Software Engineer
period: Aug 2024 — Jun 2026
tech: [python, django, django-rest-framework, postgresql, twilio, plivo, elasticsearch, gcp, shopify]
questions:
  - q: "Walk me through how you fixed the PostgreSQL index bloat on latest_activity."
    a: |
      Every call activity updated the indexed `latest_activity` field, which churned the
      index. I traced the bloat to those per-activity updates and redesigned the update
      strategy to restore query performance.

      TODO: add the before/after numbers and the exact new strategy.
---

## Role & team

TODO

## What I built

TODO: the Call Campaign Engine (Manual, IVR, AI-driven calling with decoupled agent execution),
Plivo and Twilio integrations, call tags with full-text search, the Shopify integration flow.

## Impact

TODO
