---
title: QWR AI Voice Bot
summary: Production AI voice agent with ~350–500ms time to first audio.
order: 1
experience: qwr
tech: [django-channels, gemini-live-api, websockets, postgresql, exotel, telegram-api]
questions:
  - q: "How did you get time to first audio down to ~350–500ms?"
    a: |
      By decoupling the telephony layer (Exotel) from the AI engine (Gemini Live API)
      and streaming audio both ways over WebSockets, instead of processing whole turns.

      TODO: expand with the concrete pieces of the pipeline.
---

## Overview

TODO: what the voice bot does, who calls it, and what a successful call looks like.

## How it works

TODO: the call flow from Exotel through Django Channels to the Gemini Live API and back,
including barge-in (interruption handling).

## Key decisions & trade-offs

TODO: why decouple telephony from the AI engine; why Django Channels; what you gave up.

## Challenges

TODO: caller identity extraction via async function calling, post-call summaries over Telegram.
