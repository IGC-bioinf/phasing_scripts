import os
from os.path import join 
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from tqdm import tqdm 
import numpy  as np
import pandas as pd 


root_folder = '/home/roma/comp_f'

FILTER_SIZE = 1001
X_column = 'DISTANCE'
 
Y_column = 'YIELD'
#Y_column = 'ACCURACY'

#Y_LABEL = 'SNPs phased and sharing phasing block (%)'
Y_LABEL = 'SNVs in correct phase (%)'


beagle_list = ['eagle_prob_1000G.vcf.gz_folder',
'eagle_prob_HRC.vcf.gz_folder', 
'proband_beagle_1000G.vcf.gz_folder', 
'proband_beagle_belref1000G.vcf.gz_folder']


shapeit_list = ['eagle_prob_1000G.vcf.gz_folder',
'eagle_prob_HRC.vcf.gz_folder',
'proband_shapeit_1000G.vcf.gz_folder',
'proband_shapeit_belref1000G.vcf.gz_folder']



samples_list = os.listdir(root_folder) 

combined_tsv = list()

for sample in tqdm(samples_list): 
    
    sample_path = join(root_folder, sample)
    
    if not sample.endswith('.svg')\
    and not sample.endswith('.csv'):
        
        methods_list = [join(sample_path, file)\
                        for file in os.listdir(sample_path)\
                        if not file.endswith('.svg')\
                        and not file.endswith('.csv')]
        
        for method in methods_list: 
            runs_list  = [join(method, file)\
                         for file in os.listdir(method)\
                         if file.endswith('.vcf.gz_folder')\
                         and not file.endswith('.csv')\
                         and 'reference' not in file]
            
            for run in runs_list:
                tsv_list = [join(run, file)\
                            for file in os.listdir(run)\
                            if file.endswith('.tsv')\
                            and not file.endswith('.csv')
                            and 'reference' not in file]
                
                for tsv_file in tsv_list:
                    plot_frame = pd.read_csv(tsv_file, sep='\t')
                    plot_frame = plot_frame.fillna(0)
                    
                    sub_data = savgol_filter(plot_frame[Y_column], FILTER_SIZE, 2)
                    combined_tsv.append([tsv_file, sub_data])
                    
                                    
combined_frame = pd.DataFrame(combined_tsv, columns=['Info', 'Data'])       
del combined_tsv


plt.subplots(figsize=(20,10))
plt.title('Beagle', fontsize=20)

for index, beagle_item in enumerate(beagle_list): 
    
    beagle_item_frame = combined_frame[(combined_frame.Info.str.contains(beagle_item)) & 
                                       (combined_frame.Info.str.contains('beagle'))]
    
    label_info = beagle_item.split('.')[0].replace('_',' ')
    
    beagle_item_frame = pd.DataFrame(beagle_item_frame.Data.tolist()).T
    
    _, size = beagle_item_frame.shape 
    
    beagle_mean = beagle_item_frame.mean(axis=1)
    beagle_std = beagle_item_frame.std(axis=1)
        
    plt.plot(plot_frame.DISTANCE, 
             beagle_mean, '-')

    plt.fill_between(plot_frame.DISTANCE, 
                     beagle_mean - beagle_std/np.sqrt(size),
                     beagle_mean + beagle_std/np.sqrt(size),
                     alpha=0.3, interpolate=True, step='pre',
                     label=label_info)
    
    plt.xlabel('Pairwise SNV distance (dp)', fontsize=20)
    plt.ylabel(Y_LABEL, fontsize=20)
    
    plt.grid(True, which='both')
    plt.xscale('log')
        
plt.legend(loc='lower left', fontsize=16)  
plt.savefig(f"{root_folder}/Beagle[{Y_column}].svg", format='svg', dpi=400)
plt.close()
    


plt.subplots(figsize=(20,10))
plt.title('Shapeit', fontsize=20)

for index, shapeit_item in enumerate(shapeit_list): 
    
    shapeit_item_frame = combined_frame[(combined_frame.Info.str.contains(shapeit_item)) & 
                                       (combined_frame.Info.str.contains('shapeit'))]
    
    label_info = shapeit_item.split('.')[0].replace('_',' ')
    
    shapeit_item_frame = pd.DataFrame(shapeit_item_frame.Data.tolist()).T
    
    _, size = shapeit_item_frame.shape 
    
    shapeit_mean = shapeit_item_frame.mean(axis=1)
    shapeit_std = shapeit_item_frame.std(axis=1)
        
    plt.plot(plot_frame.DISTANCE, 
             shapeit_mean, '-')

    plt.fill_between(plot_frame.DISTANCE, 
                     shapeit_mean - shapeit_std/np.sqrt(size),
                     shapeit_mean + shapeit_std/np.sqrt(size),
                     alpha=0.3, interpolate=True, step='pre',
                     label=label_info)
    
    plt.xlabel('Pairwise SNV distance (dp)', fontsize=20)
    plt.ylabel(Y_LABEL, fontsize=20)
    
    plt.grid(True, which='both')
    plt.xscale('log')
        
plt.legend(loc='lower left', fontsize=16)  
plt.savefig(f"{root_folder}/Shapeit[{Y_column}].svg", format='svg', dpi=400)
plt.close()
    
