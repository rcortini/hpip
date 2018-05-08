#!/bin/bash

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
  cp $hpipline_dir/hpipline.py $rep
done
