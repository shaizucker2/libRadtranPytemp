import subprocess
import os
import LibRadPy as lrp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


path = '/home/shai/Documents/Oracle_Code/libRadtran-2.0.4'

#settings
wavelength = 350
sza = 48
umu_range = np.arange(-1, 0.5, 0.07)
umu = list(umu_range)
phi = [0, 10]
# code
lrp_obj = lrp.LibRadPy(path)
lrp_obj.setup()

# lrp_obj.generate_uvspec_mie_input(wavelength, sza, umu, phi)
# lrp_obj.run_mie()
lrp_obj.generate_uvspec_aerosol_input(wavelength, sza, umu, phi)
lrp_obj.run_uvspec('UVSPEC_AEROSOL_AUTO.INP')

radiance_mat = lrp_obj.read_output_intensity(umu, phi)
plt.plot(umu, radiance_mat[0, :, 0])
plt.xlabel('umu [cos(theta)]')
plt.ylabel('I')
plt.show()
plt.figure()
plt.plot(umu, radiance_mat[1,:,0])
plt.xlabel('umu [cos(theta)]')
plt.ylabel('Q')
plt.show()
plt.figure()
plt.plot(umu, radiance_mat[2, :,0])
plt.xlabel('umu [cos(theta)]')
plt.ylabel('U')
plt.show()
# abc=3
# lrp_obj.example_mie_uvspec()
# a = np.array([1.1, 2.5, 3, 4])
# print(lrp.array_to_str(a))
# # os.chdir(path)
# # result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
# # if result.stderr is "":
# #     ls_list = result.stdout.split('\n')
# #     ls_list = [line.split(' ')[-1] for line in ls_list]
# #     # for ii in range(1,len(ls_list)) #second index by purpose
# # if 'auto_input' not in ls_list:
# #     os.mkdir('auto_input')
# # if 'auto_output' not in ls_list:
# #     os.mkdir('auto_output')
# # dir_list = subprocess.run('ls')

# Run uvspec
