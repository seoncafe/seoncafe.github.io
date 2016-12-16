pro plot_att, LMC=LMC,SMC=SMC,bump=bump,PAH=PAH,WG=WG,Witt=Witt,radius=radius,mach=mach,usage=usage
;+ 
; The IDL procedure is provided to demostrate how to use the attenuation curve data.
; If you use the data, please acknowledge the following paper:
;     Seon & Draine (2016, ApJ, in press; http://arxiv.org/abs/106.02030)
; If you have any questions regarding the data, please email me at kiseon@kasi.re.kr.
;-

if keyword_set(usage) then begin
   print, "plot_att [,/LMC] [,/SMC] [,/witt], [,bump = bump_strength] [,PAH = PAH_strength] [,radius=radius] [,mach=mach]"
   print, "Here, bump_strength = UV bump strength       (0.0, 0.1, ..., 0.9 in steps of 0.1)."
   print, "      PAH_strength  = PAH component strength (0.0, 0.1, ..., 0.9 in steps of 0.1)."
   print, "      radius        = radius of source distribution (R_s/R_d) (0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0)."
   print, "      mach          = Mach number of the medium (0, 1, 2, 4, 6, 8, 10, 12, 16, 20)."
   print, "                      mach = 0 indicates the uniform medium."
   return
endif

if n_elements(radius) eq 0 then radius = 0.8d0
if n_elements(mach)   eq 0 then mach   = 6d0

if keyword_set(LMC) then begin
   fname = 'LMC'
endif else if keyword_set(SMC) then begin
   fname = 'SMC'
endif else begin
   fname = 'MW'
endelse

if keyword_set(WG) or keyword_set(Witt) then begin
   if fname eq 'LMC' then begin
      print,'Sorry, but the LMC dust model of Witt & Gordon is not available'
      print,'  Doing noting....'
      return
   endif
   fname = fname+'_witt'
endif

if n_elements(bump) ne 1 then bump =  1.0d0
if n_elements(PAH)  ne 1 then PAH  =  1.0d0

if (bump lt 1d0 and bump ge 0d0) then fname = fname + '_BUMP0'+string(bump*10d0, format='(i1)')
if (PAH  lt 1d0 and PAH  ge 0d0) then fname = fname + '_PAH0'+string(PAH*10d0, format='(i1)')

;fname = fname + '.sav'
;restore,fname
fname = fname + '.fits.gz'
att = mrdfits(fname,1)
print,' restored ',fname,'...'

;ir = where(att.radius eq radius, nr)
;im = where(att.mach   eq mach,   nm)
ir = where(abs(att.radius-radius) eq min(abs(att.radius-radius)), nr)
im = where(abs(att.mach  -mach)   eq min(abs(att.mach  -mach)),   nm)
print,' plotting for radius = ', att.radius[ir],', mach = ',att.mach[im], format='(a,f4.2,a,i2)'

!p.charsize=2.0
if (!d.name eq 'PS') then begin
   !p.thick=2.0
   !x.thick=!p.thick
   !y.thick=!p.thick
   !p.charthick=!p.thick
endif

!p.multi=[0,3,2]
plot,att.tauv_h,att.ebv[*,ir,im],psym=-4,/yst,xtit='Tau_V (homogenous)',ytit='E(B-V)'
plot,att.tauv_h,att.av[*,ir,im], psym=-4,/yst,xtit='Tau_V (homogenous)',ytit='A_V'

xtit = '1/lambda [1/micron]'
xx = 1d0/att.wavl

plot,xx,att.alambda[*,-1,ir,im],/xlog,/ylog,/xst,/nodata,yr=minmax(att.alambda[*,*,ir,im]),/yst,$
     xtit=xtit,ytit='A_lambda'
for it=0,n_elements(att.tauv_h)-1 do begin
   oplot,xx,att.alambda[*,it,ir,im]
endfor

plot,xx,att.alambda[*,0,ir,im]/(att.av[0,ir,im])[0],/xlog,/xst,/nodata,/yst,/ylog,$
     xtit=xtit,ytit='A_lambda/A_V'
for it=0,n_elements(att.tauv_h)-1 do begin
   av = (att.av[it,ir,im])[0]
   oplot,xx,att.alambda[*,it,ir,im]/av
endfor

plot,xx,att.alambda[*,0,ir,im]/(att.ebv[0,ir,im])[0],/xlog,/xst,/nodata,/yst,/ylog,$
     xtit=xtit,ytit='A_lambda/E(B-V)'
for it=0,n_elements(att.tauv_h)-1 do begin
   ebv = (att.ebv[it,ir,im])[0]
   oplot,xx,att.alambda[*,it,ir,im]/ebv
endfor

plot,xx,att.taueff[*,-1,ir,im],/xlog,/ylog,/xst,/nodata,yr=minmax(att.taueff[*,*,ir,im]),/yst,$
     xtit=xtit,ytit='tau_lambda'
for it=0,n_elements(att.tauv_h)-1 do begin
   oplot,xx,att.taueff[*,it,ir,im]
endfor

end
