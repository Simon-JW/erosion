#-------------------------------------------------------------------------------
# Name:        Creating accurate custom k factor equations
# Purpose:
#
# Author:      walkers
#
# Created:     18/07/2017
# Copyright:   (c) walkers 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import required modules
import time; t0 = time.time()
from fractions import Fraction
import time
import sympy as sy
import arcpy
from arcpy import env
import numpy as np

################################################################################
#Point to target excel file and provide name for output file to be created.

in_excel = "D:\PhD\USLE\\second_order.xlsx" # Set absolute path of input excel file.

out_tble = "D:\\PhD\\USLE\\arc_tables\\test_t_e.dbf" #Must end in .dbf

################################################################################

#That's it! no more inputs required.

#Once the script has run, the table will be available to pull into ArcGIS.

################################################################################

#Specify first order or second order estimation.

#Enter 1 for first order

#Enter 2 for second order.

estimation = 2

################################################################################


#Defining a function to convert the output to float values.
def convert(s):
    try:
        return float(s)
    except ValueError:
        num, denom = s.split('/')
        return float(num) / float(denom)

output_decimals = 2 #Set the desired number of decimal places for the output vales.

for item in range(1,2):
    if item == estimation:
        #First order variables
        Zone = 'Zone';
        var_1 = 'Silt';
        var_2 = 'Sand';
        var_3 = 'Organic';
        result = 'k_factor';
        coef_1 = 'coef_silt';
        coef_2 = 'coef_sand';
        coef_3 = 'coef_org'
    else:
        #Second order variables.
        Zone = 'Zone';
        var_1 = 'First';
        var_2 = 'Struct';
        var_3 = 'Perm';
        result = 'Second';
        coef_1 = 'coef_fir';
        coef_2 = 'coef_stru';
        coef_3 = 'coef_per'

# ExcelToTable_conversion (Input_Excel_File, Output_Table, {Sheet})
arcpy.ExcelToTable_conversion(in_excel, out_tble)

#Note: for column names there seems to be a character limit around 10 characters.

cursor = arcpy.da.SearchCursor(out_tble, [Zone, var_1, var_2, var_3, result, coef_1, coef_2, coef_3])
table_rows = []

#Create a list of table rows (just so I'm not dealing with an arcpy object anymore).
for row in cursor:
    table_rows.append(row)

#From here down needs to be in a loop to allow multiple 3 x 3 arrays to be constructed.

array_size = len(table_rows)

array_shell = (array_size, 4)

data_array = np.zeros((array_shell), dtype = np.float64)

for idx, val in enumerate(table_rows):
    print(idx, val)
    ind = int(idx)
    data_array[ind] = table_rows[ind][1:5]
    print data_array

def get_every_n(a, n=3):
    for i in range(a.shape[0] // 3):
        yield a[3*i:3*(i+1)]

iteration = -1
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

    print(full_system)

    #First scale top row to give initial pivot.
    pivot_1 = full_system[0][0]; # Identifies value of leading coefficient to become first pivot.
    print pivot_1;
    scale_r1 = full_system[0]/pivot_1; # Divides x1 by leading coefficient to create a pivot value of 1.
    full_system[0] = scale_r1;

    #Now use pivot_1 to knock out two rows below.
    r2_l = full_system[1][0]; # Identifies value of leading coefficient in x2.
    print r2_l;
    r2_o1 = full_system[1] - (scale_r1 * r2_l); # Row two minus x times row one where x will be the value of the leading coefficient for x2.
    print r2_o1;
    full_system[1] = r2_o1;# Update system with new r2.
    print full_system;
    r3_l = full_system[2][0];
    r3_o1 = full_system[2] - (scale_r1 * r3_l); # Row three minus x times row one where x will be the value of the leading coefficient for x3.
    full_system[2] = r3_o1;# Update system with new r3.
    print full_system;

    #Now create a central pivot.
    pivot_2 = full_system[1][1];
    print pivot_2;
    scale_r2 = full_system[1]/pivot_2; # Repeating the same process from the first row. Divides x2 by the coefficient of the central term of x2 to create a pivot value of 1.
    full_system[1] = scale_r2;

    #Now use pivot_2 to knock out rows above and below.
    r1_c = full_system[0][1] # Find the coefficient value for middle term of row one.
    r1_o2 = full_system[0] - (full_system[1] * r1_c) # Row two minus x times row one where x will be the value of the leading coefficient for x2.
    full_system[0] = r1_o2;
    print full_system

    #Repeat above step for row three.
    r3_c = full_system[2][1] # Find the coefficient value for middle term of row three.
    r3_o2 = full_system[2] - (full_system[1] * r3_c)
    full_system[2] = r3_o2
    print full_system

    # Now finally create the last pivot in row three.
    pivot_3 = full_system[2][2]
    print pivot_3
    scale_r3 = full_system[2]/pivot_3
    full_system[2] = scale_r3
    print full_system

    #Now use pivot_3 to knock out rows above.
    r2_e = full_system[1][2]
    r2_o3 = full_system[1] - (full_system[2] * r2_e)
    full_system[1] = r2_o3
    print full_system
    r1_e = full_system[0][2]
    r1_o3 = full_system[0] - (full_system[2] * r1_e)
    full_system[0] = r1_o3;

    print '--------------------------------------'

    print 'Full system in pure rational form:'

    print full_system

    print '--------------------------------------'

    silt_frac = full_system[0][3]; sand_frac = full_system[1][3]; organic_frac = full_system[2][3];

    silt = convert(silt_frac); sand = convert(sand_frac); organic = convert(organic_frac)

    decimals_print =('%.' + str(output_decimals) + 'f');

    print ('silt = ' + str(decimals_print % round(silt, output_decimals))), "|", ('sand = ' + str(decimals_print % round(sand, output_decimals))),"|", ('organic = ' + str(decimals_print % round(organic, output_decimals)))


    with arcpy.da.UpdateCursor(out_tble, [Zone, var_1, var_2, var_3, result, coef_1, coef_2, coef_3]) as cursor:
        for row in cursor:
            count += 1
            print ('iteration', iteration)
            print ('count', count)
            if count == iteration * 3:
                print 'yes'
                print row
                row[5] = silt
                row[6] = sand
                row[7] = organic
                cursor.updateRow(row)

for row in cursor:
    print row

print ""
print "Time taken: " "hours: %i, minutes: %i, seconds: %i" %(int((time.time()-t0)/3600), int(((time.time()-t0)%3600)/60), int((time.time()-t0)%60))
