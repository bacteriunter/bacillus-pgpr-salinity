# Comparative genomics of PGPR traits in Bacillus

This repository contains the workflow and data used for the analysis of plant growth-promoting (PGPR) traits in Bacillus genomes from saline and non-saline environments.

## Overview

The study evaluates whether PGPR-associated genes are structured by environmental salinity using a targeted comparative genomics approach.

## Workflow

1. Genome retrieval (NCBI RefSeq)
2. Metadata curation and environmental classification
3. Quality filtering and taxonomic matching
4. Proteome extraction
5. Selection of 22 PGPR-related KEGG orthologs
6. HMM-based annotation (HMMER)
7. Construction of presence–absence matrix
8. Statistical analysis (Fisher, PCA, PERMANOVA, module analysis)

## Requirements

- Python 3.x
- HMMER
- pandas, matplotlib, numpy, scipy

## Reproducibility

All scripts are located in `scripts/` and can be executed sequentially following the workflow described in the manuscript.

## Data availability

Processed datasets and results are available in this repository. Raw genome data can be retrieved from NCBI using the provided accession lists.
