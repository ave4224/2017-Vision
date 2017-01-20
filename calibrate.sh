#!/bin/bash
v4l2-ctl
-c exposure_auto=1 \
-c exposure_auto_priority=1 \
-c exposure_absolute=6 \
-c saturation=42
