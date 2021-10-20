#!/bin/bash

for i in `seq 0 7`;
do
    let t=100+i*1
    echo $t
    cat eta_loc_t${t}_* >> eta_loc_t${t}
    rm eta_loc_t${t}_*
    for j in `seq 1 9`
    do
	cat eta_loc_t${t}.${j}_* >> eta_loc_t$t.$j
	rm eta_loc_t${t}.${j}_*
    done
done
