#!/bin/bash
cd /home/roma/comp_f
for i in $(ls /home/roma/comp_f | sed 's/_comp//g')
do
	cd ${i}_comp
	cd ${i}_beagle_comp
	for k in $(ls *.vcf.gz)
	do
		tabix -p vcf $k
		mkdir -p ${k}_folder && cd ${k}_folder
		for chr in {1..22}
		do
			bcftools view ../$k -r chr${chr} -s ${i}_proband -Oz -o ${k}_chr${chr}.vcf.gz
		done
		cd ../
	done
	cd ../${i}_shapeit_comp
	for k in $(ls *.vcf.gz)
	do
		tabix -p vcf $k
		mkdir -p ${k}_folder && cd ${k}_folder
		for chr in {1..22}
		do
			bcftools view ../${k} -r chr${chr} -s ${i}_proband -Oz -o ${k}_chr${chr}.vcf.gz
		done
		cd ../
	done
	cd ../../
	pwd
done 
	
