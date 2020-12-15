#!/bin/bash
cd /home/roma/comp_f
export PATH=/home/roma/Soft/phasing/scripts:$PATH
for i in $(ls /home/roma/comp_f | sed 's/_comp//g')
do
	cd ${i}_comp
	cd ${i}_beagle_comp
	for k in $(ls | grep folder | grep -v reference )
	do
		sample=$(echo $k | sed 's/_folder//g')
		cd $k
		for chr in {1..22}
		do
			pwd
			measure_phasing_performance.pl -i ${sample}_chr${chr}.vcf.gz -r ../${i}_beagle_trio_1000G_reference.vcf.gz_folder/${i}_beagle_trio_1000G_reference.vcf.gz_chr${chr}.vcf.gz -o ${sample}_chr${chr} -a ${sample}_chr${chr}.tsv -e ${sample}_chr${chr}.tmp
		done
		cd ../
	done
	cd ../${i}_shapeit_comp
	for k in $(ls | grep folder | grep -v reference )
	do
		sample=$(echo $k | sed 's/_folder//g')
		cd $k
		for chr in {1..22}
		do	
			pwd
			measure_phasing_performance.pl -i ${sample}_chr${chr}.vcf.gz -r ../${i}_shapeit_trio_1000G_reference.vcf.gz_folder/${i}_shapeit_trio_1000G_reference.vcf.gz_chr${chr}.vcf.gz -o ${sample}_chr${chr} -a ${sample}_chr${chr}.tsv -e ${sample}_chr${chr}.tmp
		done
		cd ../
	done
	cd ../../
	pwd
done 
	
