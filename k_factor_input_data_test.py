#-------------------------------------------------------------------------------
# Name:        File compatibility test.
# Purpose:
#
# Author:      Simon Walker
#
# Created:     23/07/2017
# Copyright:   (c) Simon Walker 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#This script looks at an intended input excel file and etermines whether it is
# in the correct format for the program. If not it will print a list of required
# changes.

# Imports
import time; t0 = time.time()
from fractions import Fraction
import time
import sympy as sy
import arcpy
from arcpy import env
import numpy as np

################################################################################
#Point to target excel file and provide name for output file to be created.

in_excel = "D:\\PhD\\junk\\all_zones.xlsx" # Absolute path to input excel file.

out_tble = "D:\\PhD\\junk\\test_t_v.dbf" #Name for ArcGIS table to be created.
# Must end in .dbf

################################################################################

#Defining a function to convert the output to float values.
def convert(s):
    try:
        return float(s)
    except ValueError:
        num, denom = s.split('/')
        return float(num) / float(denom)

output_decimals = 2 #Set the desired number of decimal places for the output vales.

Zone = 'Zone'; Silt = 'Silt'; Sand = 'Sand'; Organic = 'Organic'; k_factor = 'k_factor'; coef_silt = 'coef_silt'; coef_sand = 'coef_sand'; coef_org = 'coef_org';

# ExcelToTable_conversion (Input_Excel_File, Output_Table, {Sheet})
arcpy.ExcelToTable_conversion(in_excel, out_tble)

#Note: for column names there seems to be a character limit around 10 characters.
cursor = arcpy.da.SearchCursor(out_tble, [Zone, Silt, Sand, Organic, k_factor, coef_silt, coef_sand, coef_org])
table_rows = []

#Create a list of table rows (just so I'm not dealing with an arcpy object anymore).
for row in cursor:
    table_rows.append(row)

#From here down needs to be in a loop to allow multiple 3 x 3 arrays to be constructed.

array_size = len(table_rows); array_shell = (array_size, 4)

data_array = np.zeros((array_shell), dtype = np.float64)

for idx, val in enumerate(table_rows):
    ind = int(idx)
    data_array[ind] = table_rows[ind][1:5]

def get_every_n(a, n=3):
    for i in range(a.shape[0] // 3):
        yield a[3*i:3*(i+1)]

iteration = -1
print 'Make any requires changes as below and then run again unless no changes required:'
for input_system in get_every_n(data_array):
    iteration += 1
    count = -1
    #System x1.
    x1_silt = sy.Rational(input_system[0,0],1);
    x1_sand = sy.Rational(input_system[0,1],1);
    x1_organic = sy.Rational(input_system[0,2],1);
    x1_k_value = sy.Rational(input_system[0,3] * 1000, 1000);

    #System x2.
    x2_silt = sy.Rational(input_system[1,0],1);
    x2_sand = sy.Rational(input_system[1,1],1);
    x2_organic = sy.Rational(input_system[1,2],1);
    x2_k_value = sy.Rational(input_system[1,3] * 1000, 1000);

    #System x3.
    x3_silt = sy.Rational(input_system[2,0],1);
    x3_sand = sy.Rational(input_system[2,1],1);
    x3_organic = sy.Rational(input_system[2,2],1);
    x3_k_value = sy.Rational(input_system[2,3] * 1000, 1000);

    full_system = np.array([[0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0]]);
    full_system = full_system.astype('object');

    full_system[0, 0] = x1_silt; full_system[0, 1] = x1_sand; full_system[0, 2] = x1_organic; full_system[0, 3] = x1_k_value;
    full_system[1, 0] = x2_silt; full_system[1, 1] = x2_sand; full_system[1, 2] = x2_organic; full_system[1, 3] = x2_k_value;
    full_system[2, 0] = x3_silt; full_system[2, 1] = x3_sand; full_system[2, 2] = x3_organic; full_system[2, 3] = x3_k_value;

    if full_system[0][0] == 0:
        print 'System ', iteration + 1, ':', 'First value in first row cannot be 0. Switch first row with second or third row.'
    else:
        pivot_1 = full_system[0][0]; # Identifies value of leading coefficient to become first pivot.
        scale_r1 = full_system[0]/pivot_1; # Divides x1 by leading coefficient to create a pivot value of 1.
        full_system[0] = scale_r1;
        #Now use pivot_1 to knock out two rows below.
        r2_l = full_system[1][0]; # Identifies value of leading coefficient in x2.
        r2_o1 = full_system[1] - (scale_r1 * r2_l); # Row two minus x times row one where x will be the value of the leading coefficient for x2.
        full_system[1] = r2_o1;# Update system with new r2.
        if full_system[1][1] == 0:
            print 'System ', iteration + 1, ':', 'Adjust sand fraction by 0.01 for first row.'
        else:
            print 'System ', iteration + 1, ':', 'No changes required'







