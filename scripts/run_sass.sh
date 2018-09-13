#!/usr/bin/env bash
cd ../static/build/scss
sass index.scss:../css/index.css
echo "styles compiled"
cd -
