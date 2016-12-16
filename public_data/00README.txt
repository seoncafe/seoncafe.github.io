<<RADIATIVE TRANSFER MODEL OF DUST ATTENUATION CURVES IN CLUMPY, GALACTIC ENVIRONMENTS>>

If you use the data, please acknowledge the following paper:
Seon & Draine (2016, ApJ, in press; http://arxiv.org/abs/106.02030)

The data include the attenuaction curves calculated using the MW, LMC, and SMC dust models
of Weingartner & Draine (2001) and of Witt & Gordon (2000).
Please let me know if you need more data that are not included in this database.

--- How to read the data
   The data are provided in two file formats, IDL save files (*.sav) and FITS files (*.fits.gz).
   The data can be read using IDL, as follows:
      restore,'MW.sav' & help,att
      or
      att = mrdfits('MW.fits.gz',1)
   An example IDL file (plot_att.pro) is provided to demonstrate how to use the data.
      (type plot_att,/usage)

--- Definitions:
   att.nwavl   = number of wavelengths
   att.ntauv_h = number of the homogeneous optical depth at V-band
   att.nradius = number of radius of the soure distribution (defined as R_s/R_d in the paper)
   att.nmach   = number of mach numbers
   att.wavl    = 1D array of wavelength in micron
   att.tauv_h  = 1D array of the homogeneous optical depth at V-band
   att.radius  = 1D array of radius of the source distribution
   att.mach    = 1D array of mach number
   att.av      = 3D array of A_V                  : att.av[it,ir,im]
   att.ebv     = 3D array of E(B-V)               : att.ebv[it,ir,im]
   att.alambda = 4D array of A_{\lambda}          : att.alambda[iw,it,ir,im]
   att.taueff  = 4D array of \tau_{\lambda}^{eff} : att.taueff[iw,it,ir,im]

   iw = index for wavelength
   it = index for tauv_h
   ir = index for radius
   im = index for mach number
   i.e., att.taueff[iw,it,ir,im] is the effective optical depth for att.wavl[iw], att.tauv_h[it], att.radius[ir], and att.mach[im]

--- files:
1. MW.sav, LMC.sav, SMC.sav (or MW.fits.gz, LMC.fits.gz, SMC.fits.gz):
   attenuation curves for MW, LMC, and SMC dust models of Weingartner & Draine (2001)
   1/wavl = 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, ..., 8.9 [micron^-1] in steps of 0.2 micron^-1
   tauv_h = 0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0
   radius = 0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0
   mach   = 0, 1, 2, 4, 6, 8, 10, 12, 16, 20 (mach = 0 corresponds to the uniform medium)

2. MW_BUMPff.sav (or MW_BUMPff.fits.gz)
   These data were obtained for the MW dust model of Weingartner & Draine (2000) with the UV bump strength
       reduced by a factor of ff.
   ff     = 00, 01, ..., 09, corresponding to the reduction factor of 0.0, 0.1, ..., 0.9.
   1/wavl = 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, ..., 8.9 [micron^-1] in steps of 0.2 micron^-1
   tauv_h = 0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0
   radius = 0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0
   mach   = 1, 2, 4, 6, 8, 10, 12, 16, 20 (please note that no data is available for mach = 0, uniform medium)

3. MW_PAHff.sav (or MW_PAHff.fits.gz)
   These data were obtained for the MW dust model of Weingartner & Draine (2000) with the PAH (UV bump + FUV extinction rise)
       component reduced by a factor of ff.
   ff     = 00, 01, ..., 09, corresponding to the reduction factor of 0.0, 0.1, ..., 0.9.
   1/wavl = 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, ..., 8.9 [micron^-1] in steps of 0.2 micron^-1
   tauv_h = 0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0
   radius = 0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0
   mach   = 1, 2, 4, 6, 8, 10, 12, 16, 20 (please note that no data is available for mach = 0, uniform medium)

4. MW_witt.sav, SMC_witt.sav (or MW_witt.fits.gz, SMC_witt.fits.gz)
   attenuation curves for MW, and SMC dust models of Witt & Gordon (2000)
   wavl   = 0.1, 0.11429, ..., 3.0001  [micron], as defined in Table 1 of Witt & Gordon (2000)
   tauv_h = 0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0
   radius = 0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0
   mach   = 0, 1, 2, 4, 6, 8, 10, 12, 16, 20 (mach = 0 corresponds to the uniform medium)
