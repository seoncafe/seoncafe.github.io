dir   = '../figs/'
fname = [file_search(dir,'MW??.sav'), file_search(dir,'MW??_dPAH.sav'),$
         dir+'MW10_all.sav',dir+'MW10_witt.sav',dir+'LMC_all.sav',dir+'SMC_all.sav',dir+'SMC_witt.sav']
n = n_elements(fname)

for i=0,n-1 do begin
   restore,fname[i]
   outfile = (strsplit(fname[i],'/',/extract))[-1]

;--- 'MW10.sav' will be ignored'
;--- 'MW10_all.sav' include data for mach = 0, but not in 'MW10.sav'
if (outfile ne 'MW10.sav') then begin
   if (outfile eq 'MW10_all.sav') then begin
      outfile='MW.sav'
   endif else if (outfile eq 'LMC_all.sav') then begin
      outfile='LMC.sav'
   endif else if (outfile eq 'SMC_all.sav') then begin
      outfile='SMC.sav'
   endif else if (outfile eq 'MW10_witt.sav') then begin
      outfile='MW_witt.sav'
   endif else if (strmid(outfile,0,1) eq 'M') then begin
      r = strmid(outfile,2,2)
      w = strmid(outfile,4,5)
      if (w eq '_dPAH') then begin
          outfile = 'MW_PAH'+r+'.sav'
      endif else begin
          outfile = 'MW_BUMP'+r+'.sav'
      endelse
   endif
   out_fits = (strsplit(outfile,'.',/extract))[0]+'.fits'

   print, fname[i],' --> ',outfile
   att = {nwavl:a.nwavl,ntauv_h:a.ntauv,nradius:a.nradius,nmach:a.nmach,$
          wavl:a.wavl,tauv_h:a.tauv,radius:a.radius,mach:a.mach,$
          Av:a.Av,ebv:a.ebv,Alambda:a.Alambda,Taueff:a.Tau_eff}
   save,file=outfile,att,/compress
   mwrfits,att,out_fits
   spawn,'gzip '+out_fits
endif

endfor

end
