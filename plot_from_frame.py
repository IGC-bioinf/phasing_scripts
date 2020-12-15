import pandas as pd, os
from argparse import ArgumentParser
#from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

#python3 plot_from_frame.py -f folder -X DISTANCE -Y NUM_PAIR_SAME_BLOCK -nX "Distance" -nY "Accuracy" -o test.png -t "Main title"

FILTER_SIZE = 1001

LABEL_SIZE=8; TITLE_SIZE = 10; LEGEND_SIZE = 6
LEGEND_LOCATION = 'lower left' # upper right, lower left ...

IMAGE_DPI=300


def main(parsed_variables): 
    
    image_path = parsed_variables['output_file']
    folder_path = parsed_variables['folder_path']
    
    title = parsed_variables['plot_title']
    
    X_field = parsed_variables['X_field']; Y_field = parsed_variables['Y_field']
    Y_name = parsed_variables['Y_name']; X_name = parsed_variables['X_name']
        
    file_list = os.listdir(folder_path)
    file_count = len(file_list)
    
    eagle_count = 0
    
    for file_index, file_name in enumerate(file_list): 
        file_path = os.path.join(folder_path, file_name)
        
        print('File name: {} [{}/{}]'.format(file_name,
              file_index, file_count))
        
        if os.path.exists(file_path):
            plot_frame = pd.read_csv(file_path, sep='\t')
            column_names = plot_frame.columns.tolist()
            
            split_params = Y_field.split('/')
            is_in_Y = set(split_params) <= set(column_names)
            is_in_X = X_field in column_names
            
            if is_in_Y and is_in_X:
                X_values = plot_frame[X_field]
                
                if len(split_params) == 1: 
                    Y_values = plot_frame[Y_field]
                elif len(split_params) == 2: 
                    first, second = split_params
                    Y_values = plot_frame[first]/plot_frame[second]
                    
                Y_values = savgol_filter(Y_values, FILTER_SIZE, 2)
                
                if eagle_count != 0: 
                    Y_values = Y_values + 0.4
                eagle_count += 1
                
                plot_label, _ = os.path.splitext(file_name)
                plt.plot(X_values, Y_values, label=plot_label.split('.')[0].replace('_',' '))
                
            else: print('Columns not found.')
        else: print('File not found | uncorrect format | ...')
        
    plt.ticklabel_format(style='plain')
    plt.legend(loc=LEGEND_LOCATION, fontsize=LEGEND_SIZE)
    
    plt.xscale('log')
#    plt.autoscale(enable=True)
    
    plt.title(title, fontsize=TITLE_SIZE, fontweight='bold')
    plt.ylabel(Y_name, fontsize=LABEL_SIZE, fontweight='bold')
    plt.xlabel(X_name, fontsize=LABEL_SIZE, fontweight='bold')
    plt.grid(True); plt.savefig(image_path, dpi=IMAGE_DPI)

    
if __name__ == "__main__":
    
    parser = ArgumentParser(description='''Plot from frame''', 
                            epilog="""shulinsky@mail.ru""")
    
    parser.add_argument('-f', '--folder_path', type = str, help = 'Name of intput file (input.tsv)')
    
    parser.add_argument('-Y', '--Y_field', type = str, help = 'Name of Y field (any variants FIELD_NAME or FIELD_NAME_1/FIELD_NAME_2)')
    parser.add_argument('-X', '--X_field', type = str, help = 'Name of X field (only DISTANCE)')
    
    parser.add_argument('-nY', '--Y_name', type = str, help = 'Y label name (any text)')
    parser.add_argument('-nX', '--X_name', type = str, help = 'X label name (any text)')
    
    parser.add_argument('-t', '--plot_title', type = str, help = 'Title name (any text)')
    parser.add_argument('-o', '--output_file', type = str, help = 'Name of output file (output.png)')
    
    parsed_arguments = parser.parse_args()
    parsed_variables = vars(parsed_arguments)
    main(parsed_variables)   

