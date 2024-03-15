#!/bin/bash

socat -d -d pty,raw,echo=0,link=/tmp/rscp_host pty,raw,echo=0,link=/tmp/rscp_client
