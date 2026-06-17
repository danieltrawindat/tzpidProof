import numpy as np

c=299792.458
MPC_KM=3.0856775814913673e19
SEC_PER_GYR=365.25*24*3600*1e9
MPC_TO_GLY=0.003261563777
rd=147.09; rstar=144.39; zstar=1089.80; zdrag=1059.94
theta_obs=1.04109e-2; theta_sig=0.00030e-2
Og=9.0e-5

BAO=[
 (0.295,'DV', 7.944,0.075),
 (0.510,'DM',13.59,0.17),(0.510,'DH',21.86,0.43),
 (0.706,'DM',17.35,0.18),(0.706,'DH',19.46,0.33),
 (0.934,'DM',21.58,0.15),(0.934,'DH',17.64,0.19),
 (1.321,'DM',27.60,0.32),(1.321,'DH',14.18,0.22),
 (1.484,'DM',30.51,0.76),(1.484,'DH',12.82,0.52),
 (2.330,'DM',38.99,0.53),(2.330,'DH', 8.632,0.101),
]
Om_sn,Om_sn_sig=0.334,0.018

def h0_per_gyr(H0_km_s_mpc):
    return H0_km_s_mpc/MPC_KM*SEC_PER_GYR

def curvature_radius_gly(H0_km_s_mpc, OK):
    if abs(OK) < 1e-12:
        return np.inf
    return (c/H0_km_s_mpc)/np.sqrt(abs(OK))*MPC_TO_GLY

def Ez(z,Om,OK,w0,wa):
    ODE=1-Om-OK-Og
    fz=(1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
    return np.sqrt(Og*(1+z)**4+Om*(1+z)**3+OK*(1+z)**2+ODE*fz)

def simpson(f,a,b,n=400):
    if n%2: n+=1
    x=np.linspace(a,b,n+1); y=f(x)
    h=(b-a)/n
    return h/3*(y[0]+y[-1]+4*np.sum(y[1:-1:2])+2*np.sum(y[2:-1:2]))

def DC(z,H0,Om,OK,w0,wa):
    return (c/H0)*simpson(lambda zz:1.0/Ez(zz,Om,OK,w0,wa),0,z, n=(600 if z>10 else 200))
def DM(z,H0,Om,OK,w0,wa):
    d=DC(z,H0,Om,OK,w0,wa); k=np.sqrt(abs(OK))*H0*d/c
    if OK<-1e-9: return (c/H0)/np.sqrt(abs(OK))*np.sin(k)
    if OK> 1e-9: return (c/H0)/np.sqrt(OK)*np.sinh(k)
    return d
def DH(z,H0,Om,OK,w0,wa): return c/(H0*Ez(z,Om,OK,w0,wa))
def DV(z,H0,Om,OK,w0,wa):
    dm=DM(z,H0,Om,OK,w0,wa); return (z*dm*dm*DH(z,H0,Om,OK,w0,wa))**(1/3)

def chi2(H0,Om,OK,w0,wa):
    if Om<=0.05 or Om>=0.8 or H0<40 or H0>90: return 1e9
    s=0.0
    for z,o,v,sg in BAO:
        p=DM(z,H0,Om,OK,w0,wa)/rd if o=='DM' else DH(z,H0,Om,OK,w0,wa)/rd if o=='DH' else DV(z,H0,Om,OK,w0,wa)/rd
        s+=((p-v)/sg)**2
    th=rstar/DM(zstar,H0,Om,OK,w0,wa)
    s+=((th-theta_obs)/theta_sig)**2
    s+=((Om-Om_sn)/Om_sn_sig)**2
    return s

# simple robust Nelder-Mead (pure python)
def nelder(f,x0,step=0.05,it=3000,tol=1e-6):
    x0=np.array(x0,float); n=len(x0)
    sim=[x0]+[x0+step*(np.abs(x0)+0.1)*(np.arange(n)==i) for i in range(n)]
    sim=np.array(sim); fv=np.array([f(s) for s in sim])
    for _ in range(it):
        idx=np.argsort(fv); sim=sim[idx]; fv=fv[idx]
        if abs(fv[-1]-fv[0])<tol: break
        cen=sim[:-1].mean(0)
        xr=cen+(cen-sim[-1]); fr=f(xr)
        if fr<fv[0]:
            xe=cen+2*(cen-sim[-1]); fe=f(xe)
            sim[-1],fv[-1]=(xe,fe) if fe<fr else (xr,fr)
        elif fr<fv[-2]:
            sim[-1],fv[-1]=xr,fr
        else:
            xc=cen+0.5*(sim[-1]-cen); fc=f(xc)
            if fc<fv[-1]: sim[-1],fv[-1]=xc,fc
            else:
                for i in range(1,n+1):
                    sim[i]=sim[0]+0.5*(sim[i]-sim[0]); fv[i]=f(sim[i])
    idx=np.argsort(fv); return sim[idx][0],fv[idx][0]

models={
 'A_flatLCDM'      :(2,lambda x:(x[0],x[1],0.0,-1.0,0.0),       [67,0.31]),
 'B_closedLCDM'    :(3,lambda x:(x[0],x[1],x[2],-1.0,0.0),      [67,0.31,-0.01]),
 'C_flat_w0waCDM'  :(4,lambda x:(x[0],x[1],0.0,x[2],x[3]),      [67,0.31,-0.8,-0.97]),
 'D_closed_breathe':(5,lambda x:(x[0],x[1],x[2],x[3],x[4]),     [67,0.31,-0.005,-0.8,-0.97]),
}
N=len(BAO)+2
print(f"data points N = {N}  ({len(BAO)} BAO + CMB theta* + SNe Om prior)\n")
res={}
for name,(k,unpack,x0) in models.items():
    f=lambda x: chi2(*unpack(x))
    xb,cb=nelder(f,x0)
    # multi-start refine
    for s in (0.02,0.1):
        xb2,cb2=nelder(f,xb,step=s)
        if cb2<cb: xb,cb=xb2,cb2
    H0,Om,OK,w0,wa=unpack(xb)
    res[name]=(cb,k,(H0,Om,OK,w0,wa))
    print(f"{name:18s} chi2={cb:6.2f} k={k} AIC={cb+2*k:6.2f} | H0={H0:.2f} Om={Om:.3f} OK={OK:+.4f} w0={w0:.3f} wa={wa:.3f}")

base=res['A_flatLCDM'][0]; baseA=base+2*2
print("\nDelta-chi2 vs flat LCDM (neg=better) ; dAIC:")
for name,(chi,k,x) in res.items():
    print(f"  {name:18s} dChi2={chi-base:+6.2f}  dAIC={(chi+2*k)-baseA:+6.2f}")

print("\nHUBBLE-AS-BREATHING: H0 = Rdot/R ; Vdot/V = 3H0")
for label,H0_value in [
    ("Planck-like",67.4),
    ("Local-distance-network-like",73.50),
    ("Best flat LCDM fit",res['A_flatLCDM'][2][0]),
    ("Best closed breathing fit",res['D_closed_breathe'][2][0]),
]:
    h=h0_per_gyr(H0_value)
    print(f"  {label:28s} H0={H0_value:6.2f} km/s/Mpc -> H0={h:.4f}/Gyr, Vdot/V={3*h:.4f}/Gyr")

OKd=res['D_closed_breathe'][2][2]
H0d=res['D_closed_breathe'][2][0]
print("\nCURVATURE RADIUS: Rc = c/(H0 sqrt(|Omega_K|))")
print(f"  Best closed breathing fit: OK={OKd:+.4f}, Rc={curvature_radius_gly(H0d,OKd):.1f} Gly")
for OKref in (0.0018,0.002,0.004):
    print(f"  Reference |OK|={OKref:.4f} at H0=67.4 -> Rc={curvature_radius_gly(67.4,OKref):.1f} Gly")

# sound horizon with neutrino-corrected radiation.
# H(z) uses Omega_r = Omega_gamma * (1 + 0.2271*N_eff), while the
# baryon-photon sound speed uses the photon density in R_b(z).
Ob=0.0493; Ogam=5.4e-5; Neff=3.046; Orad=Ogam*(1+0.2271*Neff)
H0_sound=67.36; Om_sound=0.3153
def Hz(z): return H0_sound*np.sqrt(Orad*(1+z)**4+Om_sound*(1+z)**3+(1-Om_sound-Orad))
def cs(z):
    R=(3*Ob)/(4*Ogam)/(1+z); return c/np.sqrt(3*(1+R))

def rs_scale_factor(z):
    amax=1/(1+z)
    def integrand(a):
        R=(3*Ob)/(4*Ogam)*a
        E=np.sqrt(Orad/a**4+Om_sound/a**3+(1-Om_sound-Orad))
        return (c/np.sqrt(3*(1+R)))/(amax*0+H0_sound*E*a*a)
    eps=1e-9
    return simpson(integrand, eps, amax, n=12000)

rs_star=rs_scale_factor(zstar)
rs_drag=rs_scale_factor(zdrag)
print(f"\nSOUND-FIRST: r_s(z*) = INT_z*^inf c_s/H dz = {rs_star:.1f} Mpc  (Planck {rstar}); ruler is frozen SOUND at z*={zstar}.")
print(f"SOUND-FIRST: r_s(drag) = INT_zd^inf c_s/H dz = {rs_drag:.1f} Mpc  (Planck/Bao ruler {rd}); drag epoch zd={zdrag}.")

import json
json.dump({
          "data_points": N,
          "bao_points": len(BAO),
          "cmb_points": 1,
          "sne_priors": 1,
          "models": {k:[v[0],v[1],list(v[2])] for k,v in res.items()},
          "hubble_breathing": {
            "planck_like_h0_km_s_mpc": 67.4,
            "planck_like_h0_per_gyr": h0_per_gyr(67.4),
            "planck_like_volume_rate_per_gyr": 3*h0_per_gyr(67.4),
            "local_distance_network_like_h0_km_s_mpc": 73.50,
            "local_distance_network_like_h0_per_gyr": h0_per_gyr(73.50),
            "local_distance_network_like_volume_rate_per_gyr": 3*h0_per_gyr(73.50),
            "best_closed_breathing_h0_per_gyr": h0_per_gyr(H0d),
            "best_closed_breathing_volume_rate_per_gyr": 3*h0_per_gyr(H0d),
            "best_closed_breathing_curvature_radius_gly": curvature_radius_gly(H0d, OKd),
            "reference_curvature_radius_gly": {
              "abs_OK_0.0018_H0_67.4": curvature_radius_gly(67.4,0.0018),
              "abs_OK_0.002_H0_67.4": curvature_radius_gly(67.4,0.002),
              "abs_OK_0.004_H0_67.4": curvature_radius_gly(67.4,0.004)
            }
          },
          "sound_horizon": {
            "zstar": zstar,
            "zdrag": zdrag,
            "rs_zstar_mpc": rs_star,
            "rs_drag_mpc": rs_drag,
            "planck_rs_zstar_mpc": rstar,
            "bao_rd_mpc": rd,
            "neff": Neff,
            "omega_gamma": Ogam,
            "omega_radiation_neutrino_corrected": Orad
          }
        },
          open("spartan_fit.json","w"),indent=2)
print("\nsaved spartan_fit.json")
