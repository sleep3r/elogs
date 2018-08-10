#!/usr/bin/env bash
jade -Pw index.jade &
sass scss/index.scss css/index.css --watch &
