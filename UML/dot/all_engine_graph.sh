#!/bin/bash
list="circo dot fdp neato nop nop1 nop2 osage patchwork sfdp twopi"; 
for i in ${list}
do
    dot -Tpng -o ${i}.png -K${i} class_sample_demo.dot;
done
