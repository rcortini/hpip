#!/bin/bash

# general stuff
datadir="/users/gfilion/mcorrales/HPIP"
linksdir="$datadir/links"
source ~/work/tools/my_env.sh

# get the forcing parameter
if [ $# -lt 1 ]; then
  force=0
else
  force=$1
fi

# init generate log
generate_log="jobs_generate.log"
rm -rf $generate_log

# first, check that the hpipline repository is clean
hpipline_dir=$HOME/work/CRG/projects/hpip/hpipline
check_git_clean_workdir $hpipline_dir
if [ $? -ne 0 ]; then
  error_message "hpipline dir not clean!"
  exit 1
fi
 
# get the ID of the last commit
hpipline_commit=$(get_last_git_commit $hpipline_dir)
log_message "Running against hpipline commit $hpipline_commit" >> $generate_log

# now we can create the jobs
repnames="rep1 rep2"
pbs_in="hpipline.pbs.in"
for rep in $repnames; do
  # security first: don't do anything if the directories already exist, and the
  # user is not willingly forcing creating the directories again
  if test -e $rep && [ $force -ne "1" ] ; then
    echo "Directories exist, exiting" 1>&2
    exit 1
  fi

  # now we can create the directories and create the scripts
  rm -rf $rep
  mkdir -p $rep
  pbs_out=$rep/hpipline.pbs
  cat $pbs_in |\
    sed -e s,@REP@,$rep,g |\
  tee > $pbs_out

  # copy the pipeline file to the directory
  cp $hpipline_dir/hpipline.py $rep

  # copy the links to the input files to the current directory
  iPCR_fwd="$linksdir/HPIP_iPCR_"$rep"_fwd.fastq"
  iPCR_rev="$linksdir/HPIP_iPCR_"$rep"_Rev.fastq"
  cDNA="$linksdir/HPIP_cDNA_"$rep".fastq"
  gDNA="$linksdir/HPIP_gDNA_"$rep".fastq"
  cp -d $iPCR_fwd $rep
  cp -d $iPCR_rev $rep
  cp -d $cDNA $rep
  cp -d $gDNA $rep
done
