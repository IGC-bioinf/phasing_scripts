import pandas as pd, os
from argparse import ArgumentParser

# python3 get_frame.py -f folder -o mean.tsv

def main(parsed_variables): 
    
    folder_path = parsed_variables['input_folder']
    output_path = parsed_variables['output_file']
    
    files_list = os.listdir(folder_path)
    file_count = len(files_list)
    
    file_index = 0
    for file_name in files_list: 
        file_path = os.path.join(folder_path, file_name)
        
        if '.tsv' in file_name: 
            
            print('File name: {} [{}/{}]'.format(file_name,
                  file_index, file_count)) 
            
            if os.path.exists(file_path):
                file_index  += 1
                
                read_frame = pd.read_csv(file_path, sep='\t')        
                if file_index == 1: combined_frame = read_frame
                else: combined_frame = combined_frame.add(read_frame, fill_value=0).astype(float)
            else: 
                print('File not found | uncorrect format | ...')
        
    mean_frame = combined_frame/file_index
    mean_frame.to_csv(output_path, sep='\t', index=False)
    
             
if __name__ == "__main__":
    
    parser = ArgumentParser(description='''Mean frame''', 
                            epilog="""shulinsky@mail.ru""")
    
    parser.add_argument('-f', '--input_folder', type = str, help = 'Name of root folder (folder)')
    parser.add_argument('-o', '--output_file', type = str, help = 'Name of output file (mean.tsv)')
    
    parsed_arguments = parser.parse_args()
    parsed_variables = vars(parsed_arguments)
    main(parsed_variables)   
