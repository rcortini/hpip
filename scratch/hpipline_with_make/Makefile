# input files
prom_bcd_dict=prom_bcd.txt
genome=genome.txt
iPCR_fwd=iPCR_fwd.fastq
iPCR_rev=iPCR_Rev.fastq
cDNA_fastq=cDNA.fastq
gDNA_fastq=gDNA.fastq

# intermediate files
iPCR_fasta=iPCR.fasta
iPCR_starcode=iPCR_starcode.txt
iPCR_filtered=iPCR_filtered.txt
iPCR_sam=iPCR_sam.txt
cDNA_starcode=cDNA_starcode.txt
cDNA_spikes_starcode=cDNA_spikes_starcode.txt
gDNA_starcode=gDNA_starcode.txt
gDNA_spikes_starcode=gDNA_spikes_starcode.txt

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
iPCR_insertions=iPCR_insertions.txt

# program names
hpipline=echo
starcode=echo

.PHONY : all clean

all : $(iPCR_insertions)

clean :
	rm -rf \
	  $(INTERMEDIATE_IPCR)\
	  $(INTERMEDIATE_CDNA)\
	  $(INTERMEDIATE_GDNA)

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
