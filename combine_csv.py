import os
import glob
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True,
                help="give the folder name")

args = vars(ap.parse_args())

os.chdir("data_testing/csv/" + args["folder"])

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.to_csv( "total_" + args['folder'].split('/')[1] + "_combined.csv", index=False, encoding='utf-8-sig')