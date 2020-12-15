cd /home/roma/comp_f
for i in $(ls /home/roma/comp_f)
do 
	cd $i
	for k in $(ls)
	do
	cd $k
	for r in $(ls *.vcf.gz)
		do 
			sample=$(echo $r | sed 's/.vcf.gz//g')
			gzip -d $r && bgzip -c ${sample}.vcf > $r
			rm ${sample}.vcf
		done
		cd ../
	done
	cd ../
done
