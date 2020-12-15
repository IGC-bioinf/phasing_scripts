import os
import pandas as pd
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from tqdm import tqdm


def main(parsed_variables): 
      
    root_folder = parsed_variables['input_folder']
    global_beagle = list(); global_shapeit = list()
    
    l1_folders = os.listdir(root_folder)
    
    for folder1 in tqdm(l1_folders):
        if '.' not in folder1: 
                
            l1_folder = os.path.join(root_folder, folder1)
            
            beagle = list(); shapeit = list()
            local_beagle = list(); local_shapeit = list()
            
            for folder2 in os.listdir(l1_folder):
                if '.' not in folder2: 
                    
                    l2_folder = os.path.join(l1_folder, folder2)           
                    fig, ax = plt.subplots(figsize=(30,10))
                    
                    for folder3 in os.listdir(l2_folder):
                        
                        if 'vcf.gz_folder' in folder3 \
                        and 'reference' not in folder3:
                            
                            l3_folder = os.path.join(l2_folder, folder3)
                            
                            l3_files_err_pos = [name for name in os.listdir(l3_folder) \
                                                if name.endswith('err_pos')]; l3_files_err_pos.sort()
                            
                            l3_files_err_pos_more = [name for name in os.listdir(l3_folder) \
                                                if name.endswith('err_pos.more')]; l3_files_err_pos_more.sort()
                            
                            chrXY = list()
                            
                            for err_file, more_file in zip(l3_files_err_pos, l3_files_err_pos_more): 
                                
                                more_file_path = os.path.join(l3_folder, more_file)
                                err_file_path = os.path.join(l3_folder, err_file)
                                
                                more_frame = pd.read_csv(more_file_path, sep='\t', names=['more_index', 'None'], header=None)
                                err_frame = pd.read_csv(err_file_path, sep='\t', names=['err_index', 'X'], header=None)
                                                        
                                for row_index, row_values in err_frame.iterrows(): 
                                    find_frame = more_frame[more_frame.more_index == int(row_values.err_index)]
                                    
                                    if row_values.X < 50000:
                                        chrXY.append([row_values.X/1000, 
                                                      (row_index+1)/find_frame.index[0]*100])
                            
                            chrXY_frame = pd.DataFrame(chrXY, columns=['X','Y'])
                            chrXY_frame = chrXY_frame.sort_values(by=['X'])
                            
                            label_name = folder3.split('.')[0].replace('_',' ')
                            global_label_name = ' '.join(label_name.split(' ')[1:])
                            
                            if 'shapeit' in folder2: 
                                shapeit += chrXY
                                local_shapeit.append([label_name, chrXY_frame])
                                global_shapeit.append([global_label_name, chrXY_frame])
                                
                            else: 
                                beagle += chrXY
                                local_beagle.append([label_name, chrXY_frame])
                                global_beagle.append([global_label_name, chrXY_frame])
                                                
                            Y_values = savgol_filter(chrXY_frame.Y, 15, 2)
                            
                            ax.plot(chrXY_frame.X, Y_values, '-*', label=label_name)
                                                
                            ax.set_ylabel('SER (%)', fontsize=28)
                            ax.set_xlabel('Distance to upstream phased site (kbp)', fontsize=28)
                            
                            ax.legend(loc='upper right', fontsize=20); ax.grid()
                    
                            fig.savefig(f"{l2_folder}/{folder2}[SG].svg", format='svg', dpi=400)
                            plt.close()   
        
            #%% beagle и shapeit среднее на одном графике
                     
            beagle_frame = pd.DataFrame(beagle, columns=['X','Y'])
            
            beagle = list()
            for item in beagle_frame.X.drop_duplicates():
                beagle.append([item, 
                               beagle_frame[beagle_frame.X == item].Y.mean()])
            
            beagle_frame = pd.DataFrame(beagle, columns=['X','Y'])
            beagle_frame = beagle_frame.sort_values(by=['X'])
               
            shapeit_frame = pd.DataFrame(shapeit, columns=['X','Y'])
            
            shapeit = list()
            for item in shapeit_frame.X.drop_duplicates():
                shapeit.append([item, 
                               shapeit_frame[shapeit_frame.X == item].Y.mean()])
            
            shapeit_frame = pd.DataFrame(shapeit, columns=['X','Y'])
            shapeit_frame = shapeit_frame.sort_values(by=['X'])
            
            fig, ax = plt.subplots(figsize=(40,10))
            ax.plot(beagle_frame.X, savgol_filter(beagle_frame.Y, 201, 2), '-*', label='beagle')
            ax.plot(shapeit_frame.X, savgol_filter(shapeit_frame.Y, 201, 2), '-*', label='shapeit')
            
            ax.legend(loc='upper right', fontsize=20); ax.grid()
            
            ax.set_ylabel('SER (%)', fontsize=28)
            ax.set_xlabel('Distance to upstream phased site (kbp)', fontsize=28)
            
            fig.savefig(f"{l1_folder}/{folder1}[SG].svg", format='svg', dpi=400)
            plt.close()
    
    
            #%% beagle и shapeit 4 для каждой папки 
            
            fig, ax = plt.subplots(figsize=(40,10))
            for item_name, item_frame in local_beagle: 
                ax.plot(item_frame.X, savgol_filter(item_frame.Y, 71, 2), '-*', label=item_name)
            
            ax.legend(loc='upper right', fontsize=20); ax.grid()   
            ax.set_ylabel('SER (%)', fontsize=28)
            ax.set_xlabel('Distance to upstream phased site (kbp)', fontsize=28)
            
            fig.savefig(f"{l1_folder}/beagle[SG].svg", format='svg', dpi=400)
            plt.close()
        
            fig, ax = plt.subplots(figsize=(40,10))
            for item_name, item_frame in local_shapeit: 
                ax.plot(item_frame.X, savgol_filter(item_frame.Y, 71, 2), '-*', label=item_name)
            
            ax.legend(loc='upper right', fontsize=20); ax.grid()   
            ax.set_ylabel('SER (%)', fontsize=28)
            ax.set_xlabel('Distance to upstream phased site (kbp)', fontsize=28)
            
            fig.savefig(f"{l1_folder}/shapeit[SG].svg", format='svg', dpi=400)
            plt.close()
        
    
    
    #%% beagle и shapeit для всех семплов
    
    global_beagle_frame = pd.DataFrame(global_beagle, columns=['method','frame'])
    
    fig, ax = plt.subplots(figsize=(40,10))
    
    for method in global_beagle_frame.method.drop_duplicates(): 
        
        frames = global_beagle_frame[global_beagle_frame.method == method].frame.tolist()
        combined_frame = pd.concat(frames)
        
        combined_list = list()
        for item in combined_frame.X.drop_duplicates():
            combined_list.append([item, 
                           combined_frame[combined_frame.X == item].Y.mean()])
        
        combined_frame = pd.DataFrame(combined_list, columns=['X','Y'])
        combined_frame = combined_frame.sort_values(by=['X'])
        
        ax.plot(combined_frame.X, savgol_filter(combined_frame.Y, 71, 2), '-*', label=method)
    
    ax.legend(loc='upper right', fontsize=20); ax.grid()   
    ax.set_ylabel('SER (%)', fontsize=28)
    ax.set_xlabel('Distance to upstream phased site (kbp)', fontsize=28)
    
    fig.savefig(f"{root_folder}/global_beagle[SG].svg", format='svg', dpi=400)
    plt.close()
    
    ###
    
    global_shapeit_frame = pd.DataFrame(global_shapeit, columns=['method','frame'])
    
    fig, ax = plt.subplots(figsize=(40,10))
    
    for method in global_shapeit_frame.method.drop_duplicates(): 
        
        frames = global_shapeit_frame[global_shapeit_frame.method == method].frame.tolist()
        combined_frame = pd.concat(frames)
        
        combined_list = list()
        for item in combined_frame.X.drop_duplicates():
            combined_list.append([item, 
                           combined_frame[combined_frame.X == item].Y.mean()])
        
        combined_frame = pd.DataFrame(combined_list, columns=['X','Y'])
        combined_frame = combined_frame.sort_values(by=['X'])
        
        ax.plot(combined_frame.X, savgol_filter(combined_frame.Y, 71, 2), '-*', label=method)
    
    ax.legend(loc='upper right', fontsize=20); ax.grid()
    ax.set_ylabel('SER (%)', fontsize=28)
    ax.set_xlabel('Distance to upstream phased site (kbp)', fontsize=28)
    
    fig.savefig(f"{root_folder}/global_shapeit[SG].svg", format='svg', dpi=400)
    plt.close()



if __name__ == "__main__":
    
    parser = ArgumentParser(description='''Shapeit and Beagle''', 
                            epilog="""shulinsky@mail.ru""")
    
    parser.add_argument('-i', '--input_folder', type = str, help = 'Name of intput folder (input)')
    
    parsed_arguments = parser.parse_args()
    parsed_variables = vars(parsed_arguments)
    main(parsed_variables)
