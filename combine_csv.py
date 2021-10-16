import os
import glob
import pandas as pd
os.chdir("data_v2/final_dataset/")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.to_csv( "total_combined.csv", index=False, encoding='utf-8-sig')