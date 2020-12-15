#!/bin/bash
cd /home/roma/comp_f
for i in $(ls /home/roma/comp_f)
do
	sample=$(echo $i | sed 's/_comp//g')
	cd $i
	cd ${sample}_beagle_comp
	gzip -d ${sample}_eagle_prob_HRC.vcf.gz && awk '{if($0 !~ /^#/ ) print "chr"$0; else print $0}' ${sample}_eagle_prob_HRC.vcf | sed 's/chrchr/chr/g' | bgzip -c > ${sample}_eagle_prob_HRC.vcf.gz && rm ${sample}_eagle_prob_HRC.vcf
	gzip -d ${sample}_eagle_prob_1000G.vcf.gz && awk '{if($0 !~ /^#/ ) print "chr"$0; else print $0}' ${sample}_eagle_prob_1000G.vcf | sed 's/chrchr/chr/g' | bgzip -c > ${sample}_eagle_prob_1000G.vcf.gz && rm ${sample}_eagle_prob_1000G.vcf
	cd ../${sample}_shapeit_comp
	gzip -d ${sample}_eagle_prob_HRC.vcf.gz && awk '{if($0 !~ /^#/ ) print "chr"$0; else print $0}' ${sample}_eagle_prob_HRC.vcf | sed 's/chrchr/chr/g' | bgzip -c > ${sample}_eagle_prob_HRC.vcf.gz && rm ${sample}_eagle_prob_HRC.vcf
	gzip -d ${sample}_eagle_prob_1000G.vcf.gz && awk '{if($0 !~ /^#/ ) print "chr"$0; else print $0}' ${sample}_eagle_prob_1000G.vcf | sed 's/chrchr/chr/g' | bgzip -c > ${sample}_eagle_prob_1000G.vcf.gz && rm ${sample}_eagle_prob_1000G.vcf
	gzip -d ${sample}_proband_shapeit_1000G.vcf.gz && awk '{if($0 !~ /^#/ ) print "chr"$0; else print $0}' ${sample}_proband_shapeit_1000G.vcf | sed 's/chrchr/chr/g' | bgzip -c > ${sample}_proband_shapeit_1000G.vcf.gz && rm ${sample}_proband_shapeit_1000G.vcf
	gzip -d ${sample}_shapeit_trio_1000G_reference.vcf.gz && awk '{if($0 !~ /^#/ ) print "chr"$0; else print $0}' ${sample}_shapeit_trio_1000G_reference.vcf| sed 's/chrchr/chr/g' | bgzip -c > ${sample}_shapeit_trio_1000G_reference.vcf.gz && rm ${sample}_shapeit_trio_1000G_reference.vcf
	cd ../../
	done
	cd 
	
