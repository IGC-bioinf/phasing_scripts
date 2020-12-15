cd /home/roma/comp_f
for i in $(ls /home/roma/comp_f |  sed 's/_comp//g')
do 
	cd ${i}_comp
	cd ${i}_shapeit_comp
			gzip -d ${i}_proband_shapeit_belref1000G.vcf.gz  && sed -i "s/proband/${i}_proband/g" ${i}_proband_shapeit_belref1000G.vcf && bgzip -c ${i}_proband_shapeit_belref1000G.vcf > ${i}_proband_shapeit_belref1000G.vcf.gz
			rm ${i}_proband_shapeit_belref1000G.vcf
			gzip -d ${i}_proband_shapeit_1000G.vcf.gz && sed -i "s/proband/${i}_proband/g" ${i}_proband_shapeit_1000G.vcf && bgzip -c ${i}_proband_shapeit_1000G.vcf > ${i}_proband_shapeit_1000G.vcf.gz
			rm ${i}_proband_shapeit_1000G.vcf
	cd ../
	cd ../
done
