#!/bin/bash
#$ -cwd
#$ -M marc.corrales@crg.es
#$ -e $PWD
#$ -l virtual_free=32G
python /users/gfilion/mcorrales/HPIP/links/toy_test/hpipline.py /users/gfilion/mcorrales/HPIP/links/toy_test/Toy_iPCR_rep1_fwd.fastq /users/gfilion/mcorrales/HPIP/links/toy_test/Toy_iPCR_rep1_Rev.fastq /users/gfilion/mcorrales/HPIP/links/toy_test/Toy_cDNA_rep1.fastq /users/gfilion/mcorrales/HPIP/links/toy_test/Toy_gDNA_rep1.fastq
