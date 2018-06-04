#!/bash

basename="Toy_iPCR_rep1"

fwd="$basename"_fwd.fastq
rev="$basename"_Rev.fastq
genome=/mnt/ant-login/mcorrales/HPIP/dm4R6/dmel-all-chromosome-r6.15.fasta

paste -d"\n" \
  <(sed -n '2~4p' $fwd | grep -o '^.\{20\}' | sed 's/^/>/') \
  <(sed -n '2~4p' $rev) > $basename.fasta # |\
  # bwa mem -t4 -L0,0 $genome - > $basename.sam
