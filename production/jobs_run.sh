#!/bin/bash

source ~/work/tools/my_env.sh

# init run log
run_log="jobs_run.log"
rm -f $run_log

# run the scripts
root_dir=$(pwd)
repnames="rep1 rep2"
for rep in $repnames; do
  cd $rep
  jid=$(qsub -terse hpipline.pbs)
  log_message "$rep: $jid" >> $run_log
  cd $root_dir
done
