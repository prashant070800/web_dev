---
title: QWR AI Voice Bot
summary: Proof of concept built as the hiring assignment for QWR — an inbound AI voice agent that answers questions about QWR.
order: 1
experience: qwr
experience_label: Hiring assignment for
tech: [django-channels, gemini-live-api, websockets, postgresql, exotel, telegram-api]
questions:
  - q: "Tell me about this project."
    a: |
      It was the hiring assignment QWR gave me before I joined: build an AI voice bot
      that picks up inbound phone calls and answers callers' questions about QWR.
      I built it as a proof of concept, following the assignment brief.

      TODO: one line on the stack and the result (it got me the job).
  - q: "How did you get time to first audio down to ~350–500ms?"
    a: |
      By decoupling the telephony layer (Exotel) from the AI engine (Gemini Live API)
      and streaming audio both ways over WebSockets, instead of processing whole turns.

      TODO: expand with the concrete pieces of the pipeline.
  - q: "How did you measure that latency?"
    a: |
      TODO: logs, timestamps, or test calls?
  - q: "Exotel and Gemini use different audio formats. How did you handle that?"
    a: |
      I converted the audio in between, in both directions.

      TODO: formats and sample rates on each side, the library used, chunk size.
  - q: "What happens if the caller interrupts the bot?"
    a: |
      TODO: barge-in handling, or say it wasn't in scope for the POC.
---

## Overview

A proof of concept I built as the hiring assignment for QWR, before joining. The brief:
when someone calls in, an AI voice bot answers and responds to questions about QWR.
It handles **inbound calls** only.

TODO: how the bot knows about QWR (system prompt or documents), and what a good call sounds like.

## How it works

1. A caller dials the number; **Exotel** answers and streams the call audio over a **WebSocket**.
2. A **Django Channels** consumer receives the audio and **converts it** to the format the
   **Gemini Live API** expects.
3. Gemini's spoken reply is converted back to Exotel's format and streamed to the caller.

TODO: audio formats and sample rates on each side; barge-in (interruption handling).

## Key decisions & trade-offs

- **Stream everything:** audio flows both ways continuously instead of waiting for whole
  turns, which is what keeps time to first audio low (~350–500ms).
- **Decouple telephony from the AI engine:** Exotel and Gemini only meet through the
  conversion layer, so either side could be swapped.

TODO: why Django Channels; what you'd change to take it to production.

## Challenges

TODO: audio conversion, latency, caller identity extraction via async function calling,
post-call summaries over Telegram (confirm which of these were in the assignment).
