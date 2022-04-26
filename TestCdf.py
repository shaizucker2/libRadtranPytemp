import cdflib

cdf_file = cdflib.CDF('//home/shai/Documents/Oracle_Code/libRadtran-2.0.4/examples/fwc.gamma_007.0.mie.cdf')
print(cdf_file.cdf_info())