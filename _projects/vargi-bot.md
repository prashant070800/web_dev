---
title: Vargi-Bot
summary: Warehouse simulation where a robotic arm sorts packages by medical priority (e-Yantra).
order: 2
tech: [ros, python, opencv, mqtt, javascript]
links:
  demo: https://www.youtube.com/watch?v=Eq9xviyJ1mA
questions:
  - q: "Why use MQTT to sync orders to the dashboard?"
    a: |
      MQTT is a lightweight publish/subscribe protocol: the robot publishes order and
      dispatch events once, and any subscriber (here, Google Apps Script feeding the live
      dashboard) receives them without the robot knowing who is listening.

      TODO: add how the topics were structured.
---

## Overview

TODO: the e-Yantra Robotics Competition task and what the simulated warehouse had to do.

## How it works

TODO: OpenCV package detection → priority → ROS Manipulation pick-and-place → MQTT → dashboard.

## Key decisions & trade-offs

TODO

## Challenges

TODO
