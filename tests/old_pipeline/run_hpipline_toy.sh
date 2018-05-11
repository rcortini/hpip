#!/bin/bash
#$ -cwd
#$ -M marc.corrales@crg.es
#$ -e $PWD
#$ -l virtual_free=32G
genome="/mnt/ant-login/mcorrales/HPIP/dm4R6/dmel-all-chromosome-r6.15.fasta"
python hpipline.py Toy_iPCR_rep1_fwd.fastq Toy_iPCR_rep1_Rev.fastq prom_bcd.p $genome Toy_cDNA_rep1.fastq Toy_gDNA_rep1.fastq
