#!/bin/bash
#$ -cwd
#$ -M marc.corrales@crg.es
#$ -e $PWD
#$ -l virtual_free=32G
python hpipline.py Toy_iPCR_rep1_fwd.fastq Toy_iPCR_rep1_Rev.fastq Toy_cDNA_rep1.fastq Toy_gDNA_rep1.fastq
