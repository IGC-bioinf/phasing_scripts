import os
from os.path import join 
from tqdm import tqdm 
import pandas as pd 


SNPs_used = '# Phased heterozygous sites in the golden set that used for the evaluation'
SwitchSE = '# Total switch errors (long + 2*switch + undetermined)'
LongSE = '# Long switch errors'
PointSE = '# Point switch errors'
UndeterminedSE = '# Switch errors not determined (not long nor switch)'



root_folder = '/home/roma/comp_f'


file_path = '/home/roma/comp_f/27_comp/27_shapeit_comp/27_eagle_prob_HRC.vcf.gz_folder/27_eagle_prob_HRC.vcf.gz_chr1.out'



def getData(file_path):

    with open(file_path, 'r') as file:
        for line in file: 
            
            if 'BL	' in line and 'QBL	' not in line :
                _,_,NUM_SNP_TOTAL,NUM_SNP_PHASED,_,_,_ = line.rsplit()
                
                SumSNPhased = float(NUM_SNP_PHASED)
                PersPhasedSNPs = float(NUM_SNP_PHASED)/float(NUM_SNP_TOTAL)
                
            if 'SER(%):' in line: 
                Ser = float(line.rsplit()[-1])
            
#            if 'N50(bp):' in line:
#               QAN50 = float(line.rsplit()[-1])
            
            if SwitchSE in line:
                SwitchSE_value = float(line.split('\t')[-2])
            
            if SNPs_used in line:
                SNPs_used_value = float(line.split('\t')[-2])
                
            if LongSE in line:
                LongSE_value = float(line.split('\t')[-2])
        
            if PointSE in line:
                PointSE_value = float(line.split('\t')[-2])
                
            if UndeterminedSE in line:
                UndeterminedSE_value = float(line.split('\t')[-2])
        
    return [SumSNPhased, PersPhasedSNPs, #QAN50,
            SNPs_used_value, SwitchSE_value, LongSE_value, 
            PointSE_value, UndeterminedSE_value, Ser]
    

columns = ['SumSNPhased', 'PersPhasedSNPs', #'QAN50', 
           'SNPs_used_value', 'SwitchSE_value', 'LongSE_value', 
           'PointSE_value', 'UndeterminedSE_value', 'SER']
    

samples_list = os.listdir(root_folder) 

combined_tsv = list()

sample_runs = list()

for sample in tqdm(samples_list): 
    
    sample_path = join(root_folder, sample)
    
    if not sample.endswith('.svg')\
    and not sample.endswith('.csv'):
        
        methods_list = [join(sample_path, file)\
                        for file in os.listdir(sample_path)\
                        if not file.endswith('.svg')\
                        and not file.endswith('.csv')]
        
        merged_runs = list()
        
        for method in methods_list: 
            runs_list  = [join(method, file)\
                         for file in os.listdir(method)\
                         if file.endswith('.vcf.gz_folder')\
                         and not file.endswith('.csv')\
                         and 'reference' not in file]

            all_runs = list()
            
            for run in runs_list:
                out_list = [join(run, file)\
                            for file in os.listdir(run)\
                            if file.endswith('.out')\
                            and not file.endswith('.csv')
                            and 'reference' not in file]
                
                run_name = '_'.join(run.split('/')[-1].split('.')[0].split('_')[1:])
                run_name = run_name.replace('_shapeit','').replace('beagle_','') 
                
                chrs_data = list()
                for out_file in out_list:
                    chrs_data.append(getData(out_file))
                    
                chrs_frame = pd.DataFrame(chrs_data, columns=columns)
                
                chr_out = [run, run_name,
                           chrs_frame['SumSNPhased'].sum(),
                           chrs_frame['PersPhasedSNPs'].mean(),
#                           chrs_frame['QAN50'].mean(),
                           chrs_frame['SNPs_used_value'].sum(),
                           chrs_frame['SwitchSE_value'].sum(),
                           chrs_frame['LongSE_value'].sum(),
                           chrs_frame['PointSE_value'].sum(),
                           chrs_frame['UndeterminedSE_value'].sum(),
                           chrs_frame['SER'].mean()]
                all_runs.append(chr_out)
                
            merged_runs+=all_runs
        sample_runs+=merged_runs
            
sample_runs_frame = pd.DataFrame(sample_runs, 
                                 columns=['Full_info', 'Method']+columns)   
                
beagle_frame = sample_runs_frame[sample_runs_frame['Full_info'].str.contains('beagle')]
beagle_frame = beagle_frame.drop('Full_info',axis=1)

shapeit_frame = sample_runs_frame[sample_runs_frame['Full_info'].str.contains('shapeit')]
shapeit_frame = shapeit_frame.drop('Full_info',axis=1)

result_output = list()
for method in beagle_frame['Method'].drop_duplicates():
    
    method_frame = beagle_frame[beagle_frame['Method'] == method]
    
    method_out = [method, 
               method_frame['SumSNPhased'].mean(),
               method_frame['PersPhasedSNPs'].mean(),
#               method_frame['QAN50'].mean(),
               method_frame['SNPs_used_value'].mean(),
               method_frame['SwitchSE_value'].mean(),
               method_frame['LongSE_value'].mean(),
               method_frame['PointSE_value'].mean(),
               method_frame['UndeterminedSE_value'].mean(),
               method_frame['SER'].mean()]
    
    result_output.append(method_out)

beagle_result_frame = pd.DataFrame(result_output, 
                                 columns=['Method']+columns).T


result_output = list()
for method in shapeit_frame['Method'].drop_duplicates():
    
    method_frame = shapeit_frame[shapeit_frame['Method'] == method]
    
    method_out = [method, 
               method_frame['SumSNPhased'].mean(),
               method_frame['PersPhasedSNPs'].mean(),
#               method_frame['QAN50'].mean(),
               method_frame['SNPs_used_value'].mean(),
               method_frame['SwitchSE_value'].mean(),
               method_frame['LongSE_value'].mean(),
               method_frame['PointSE_value'].mean(),
               method_frame['UndeterminedSE_value'].mean(),
               method_frame['SER'].mean()]
    
    result_output.append(method_out)

shapeit_result_frame = pd.DataFrame(result_output, 
                                 columns=['Method']+columns).T

beagle_result_frame.to_excel(root_folder+'[beagle].xlsx', header=False, index=True)
shapeit_result_frame.to_excel(root_folder+'[shapeit].xlsx', header=False, index=True)

    
                
                
                
