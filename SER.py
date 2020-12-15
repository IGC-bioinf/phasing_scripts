import os
import pandas as pd 



from argparse import ArgumentParser


def main(parsed_variables):
    
    folder_path = parsed_variables['folder']
        
    output_path_SEP = folder_path + '_[SEP].csv' 
    output_path_PERS = folder_path + '_[PERS].csv' 
    
    file_list = os.listdir(folder_path)
    
    file_list = [file for file in file_list if 'folder' in file and 'reference' not in file]
    
    index = 0
    for folder_name in file_list:
        
        name = ' '.join(folder_name[::-1].split('.')[-1][::-1].split('_')[1:])
        sub_folder_path = os.path.join(folder_path, folder_name)
        
        result_list = list()
        result_list2 = list()
        
        mean_SER = 0; mean_PERS = 0
        
        for sub_name in os.listdir(sub_folder_path):
            
            if '.out' in sub_name:
                chr_value = sub_name.split('_')[-1].split('.')[0]
                file_path = os.path.join(sub_folder_path, sub_name)
                
                new_name = ' '.join(sub_name[::-1].split('.')[-1][::-1].split('_')[1:])
                
                with open(file_path, 'r') as file: 
                    for line in file.readlines(): 
                       rstrip_line = line.rsplit()
                       
                       if 'SER(%):' in rstrip_line:
                           SER = rstrip_line[-1]+'%'
                           mean_SER+=float(rstrip_line[-1])
                       if 'BL' in rstrip_line:
                           PERS = int(rstrip_line[3])/int(rstrip_line[2])*100
                           mean_PERS+=PERS
                           
                           
                       
                result_list.append([int(chr_value.replace('chr','')), SER])        
                result_list2.append([int(chr_value.replace('chr','')), str(PERS)[0:5]+'%'])        
        
        
        sub_frame = pd.DataFrame(result_list)
        sub_frame.columns = ['chr', name.replace('_',' ')]
        sub_frame = sub_frame.sort_values(by=['chr'])
        
        df = pd.DataFrame({'chr':['Mean'], name.replace('_',' '): [str(mean_SER/len(result_list))[0:5]+'%']})
        sub_frame = sub_frame.append(df, ignore_index=True)
        
        sub_frame2 = pd.DataFrame(result_list2)
        sub_frame2.columns = ['chr', name.replace('_',' ')]
        sub_frame2 = sub_frame2.sort_values(by=['chr'])
        
        df2 = pd.DataFrame({'chr':['Mean'], name.replace('_',' '): [str(mean_PERS/len(result_list))[0:5]+'%']})
        sub_frame2 = sub_frame2.append(df2, ignore_index=True)
        
        
        if index == 0: 
            buff_frame = sub_frame
            buff_frame2 = sub_frame2
        else: 
            buff_frame = pd.merge(buff_frame, sub_frame, on=['chr'])
            buff_frame2 = pd.merge(buff_frame2, sub_frame2, on=['chr'])
        
        index += 1
    
    
    buff_frame.to_csv(output_path_SEP, sep='\t', index=False)
    buff_frame2.to_csv(output_path_PERS, sep='\t', index=False)
    
        

    
if __name__ == "__main__":
    
    parser = ArgumentParser(description='''Get rs_index info''', 
                            epilog="""shulinsky@mail.ru""")
    
    parser.add_argument('-f', '--folder', type = str, help = 'Name of intput.xlsx file (input.xlsx)')
    
    parsed_arguments = parser.parse_args()
    parsed_variables = vars(parsed_arguments)
    main(parsed_variables)   
     
