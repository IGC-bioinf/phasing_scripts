#!/bin/bash
cd /home/roma/comp
export PATH=/home/roma/Soft/phasing/scripts:$PATH
for i in $(ls /home/roma/comp | sed 's/_comp//g')
do
	cd ${i}_comp
	cd ${i}_beagle_comp
	for k in $(ls | grep folder | grep -v reference )
	do
		sample=$(echo $k | sed 's/_folder//g')
		cd $k
		mkdir -p ../graph_folder
		pwd
		python3 ~/get_frame.py -f $(pwd) -o ../graph_folder/${sample}.tsv
		cd ../ 
	done
	name_of_plot=$(echo Beagle_1000G_trio [${i}])
	python3 ~/plot_from_frame.py -f $(pwd)/graph_folder -X DISTANCE -Y ACCURACY -nX "Pairwise SNV distanse (bp)" -nY "SNVs in correct phase (%)" -o "${name_of_plot}_ACCURACY.png" -t "${name_of_plot}"
	cd ../${i}_shapeit_comp
	for k in $(ls | grep folder | grep -v reference )
	do
		sample=$(echo $k | sed 's/_folder//g')
		cd $k
		mkdir -p ../graph_folder
		pwd
		python3 ~/get_frame.py -f $(pwd) -o ../graph_folder/${sample}.tsv
		cd ../
	done
	name_of_plot=$(echo Shapeit_1000G_trio [${i}])
	python3 ~/plot_from_frame.py -f $(pwd)/graph_folder -X DISTANCE -Y ACCURACY -nX "Pairwise SNV distanse (bp)" -nY "SNVs in correct phase (%)" -o "${name_of_plot}_ACCURACY.png" -t "${name_of_plot}"
	cd ../../
	pwd
done 
	
