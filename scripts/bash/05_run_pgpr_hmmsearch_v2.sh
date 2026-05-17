#!/bin/bash

# INPUT
FAA_DIR="01_downloads/proteomes_faa"
HMM_DB="04_functional_annotation/kofamscan/pgpr_profiles_combined_v2.hmm"

# OUTPUT
OUT_DIR="04_functional_annotation/kofamscan/hmmsearch_results_v2"
mkdir -p $OUT_DIR

# THREADS
CPU=4

for faa in $FAA_DIR/*.faa; do
    base=$(basename $faa .faa)

    echo "Processing $base..."

    hmmsearch --cpu $CPU \
        --tblout $OUT_DIR/${base}.tbl \
        $HMM_DB \
        $faa \
        > $OUT_DIR/${base}.log

done
