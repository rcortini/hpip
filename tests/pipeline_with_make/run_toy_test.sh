#!/bin/bash

# file names
make_in="Makefile.in"
make_out="Makefile"

# variables
iPCR_basename="Toy_iPCR_rep1"
cDNA_basename="Toy_cDNA_rep1"
gDNA_basename="Toy_gDNA_rep1"

cat $make_in |\
  sed -e s,/users/gfilion,/mnt/ant-login,g |\
  sed -e s,@iPCR_basename@,$iPCR_basename,g |\
  sed -e s,@cDNA_basename@,$cDNA_basename,g |\
  sed -e s,@gDNA_basename@,$gDNA_basename,g |\
tee > $make_out

make
