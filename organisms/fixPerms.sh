#!/bin/bash
for d in `find ./ -type d`
do
    chmod a+rx $d
done
chmod -R a+r *
