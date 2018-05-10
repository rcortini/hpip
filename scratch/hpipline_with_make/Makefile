# input files
prom_bcd_dict=prom_bcd.p
genome=/mnt/ant-login/mcorrales/HPIP/dm4R6/dmel-all-chromosome-r6.15.fasta
iPCR_basename=Toy_iPCR_rep1
cDNA_basename=Toy_cDNA_rep1
gDNA_basename=Toy_gDNA_rep1

# build file names based on base names
iPCR_fwd=$(iPCR_basename)_fwd.fastq
iPCR_rev=$(iPCR_basename)_Rev.fastq
cDNA_fastq=$(cDNA_basename).fastq
gDNA_fastq=$(gDNA_basename).fastq

# intermediate files
iPCR_fasta=$(iPCR_basename).fasta
iPCR_starcode=$(iPCR_basename)_starcode.txt
iPCR_filtered=$(iPCR_basename)_filtered.txt
iPCR_sam=$(iPCR_basename).sam
cDNA_starcode=$(cDNA_basename)_starcode.txt
cDNA_spikes_starcode=$(cDNA_basename)_spikes_starcode.txt
cDNA_starcode=$(cDNA_basename)_starcode.txt
cDNA_spikes_starcode=$(cDNA_basename)_spikes_starcode.txt

# groups of files
INTERMEDIATE_IPCR=\
	     $(iPCR_fasta)\
	     $(iPCR_sam)\
	     $(iPCR_filtered)\
	     $(iPCR_starcode)

INTERMEDIATE_CDNA=\
	     $(cDNA_starcode)\
	     $(cDNA_spikes_starcode)

INTERMEDIATE_GDNA=\
	     $(gDNA_starcode)\
	     $(gDNA_spikes_starcode)

# final target
iPCR_insertions=$(iPCR_basename)_insertions.txt

# program names
hpipline=echo
starcode=echo

.PHONY : all clean cleanall

all : $(iPCR_insertions)

clean :
	rm -rf \
	  $(INTERMEDIATE_IPCR)\
	  $(INTERMEDIATE_CDNA)\
	  $(INTERMEDIATE_GDNA)

cleanall : clean
	rm -rf $(iPCR_insertions)

####################################
# EXTRACT READS FROM PAIRED-END SEQ
####################################
$(iPCR_fasta) : $(iPCR_fwd) $(iPCR_rev)
	$(hpipline) "extract_reads_from_PE_fastq $^" > $@

####################################
# MAP AND FILTER READS
####################################
$(iPCR_sam) : $(iPCR_fasta) $(genome)
	$(hpipline) "call_bwa_mapper_on_fasta_file $<" > $@

$(iPCR_filtered) : $(iPCR_sam)
	$(hpipline) "filter_mapped_reads $<" > $@

####################################
# STARCODE ON FILTERED
####################################
$(iPCR_starcode) : $(iPCR_filtered)
	$(hpipline) "call_starcode_on_filtered_file $<" > $@

####################################
# STARCODE ON FASTQ
####################################
$(gDNA_starcode) $(gDNA_spikes_starcode) : $(gDNA_fastq)
	$(hpipline) "call_starcode_on_fastq_file $<" > $@

$(cDNA_starcode) $(cDNA_spikes_starcode) : $(cDNA_fastq)
	$(hpipline) "call_starcode_on_fastq_file $<" > $@

####################################
# COLLECT INTEGRATIONS
####################################
$(iPCR_insertions) : $(iPCR_starcode) $(iPCR_sam) $(prom_bcd_dict) $(cDNA_starcode) $(cDNA_spikes_starcode) $(gDNA_starcode) $(gDNA_spikes_starcode)
	$(hpipline) "collect_integrations $^" > $(iPCR_insertions)
