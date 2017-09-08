#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Simon Walker
#
# Created:     27/05/2017
# Copyright:   (c) Simon Walker 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time; t0 = time.time()

from fractions import Fraction

import numpy as np; import time

import sympy as sy

#_____________________________________________________________________________________

#Setup a 3 x 3 system by entering values into the array below.

input_system = np.array([[0.03, 1, 6, 0.14],#Enter fraction silt, fraction sand, fraction organic matter and the first approximation from the nomograph.
                         [0.06, 4, 1, 0.07],#Enter fraction silt, fraction sand, fraction organic matter and the first approximation from the nomograph.
                         [0.09, 2, 2, 0.07]]);#Enter fraction silt, fraction sand, fraction organic matter and the first approximation from the nomograph.

output_decimals = 4 #Set the desired number of decimal places for the output vales.

#Nothing else needs to be changed.

#_____________________________________________________________________________________

#Defining a function to convert the output to float values.
def convert(s):
    try:
        return float(s)
    except ValueError:
        num, denom = s.split('/')
        return float(num) / float(denom)

#System x1.
x1_silt = sy.Rational(input_system[0,0],1);
x1_sand = sy.Rational(input_system[0,1],1);
x1_organic = sy.Rational(input_system[0,2],1);
x1_k_value = sy.Rational(input_system[0,3] * 1000, 1000);

print x1_silt

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

#If result == 0, swap rows. Do this always if pivot will become 0.

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

print ""
print "Time taken: " "hours: %i, minutes: %i, seconds: %i" %(int((time.time()-t0)/3600), int(((time.time()-t0)%3600)/60), int((time.time()-t0)%60))

