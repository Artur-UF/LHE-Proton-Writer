from __future__ import division
from subprocess import call
from math import *
from ROOT import TLorentzVector, TFile, TH1D, TH2D, TMath
from array import array
import numpy as np
import sys

#####################################################################
# GGS (CERN-CMS/UFRGS) ---
# the muons are collected considering the ID codes in the event
# sample produced with SuperCHICv2 in LHE format.
#####################################################################

#####################################################################
# USER INPUT:

rootinput = np.loadtxt(sys.argv[1], unpack=True, dtype=str, delimiter='=')
rootinput = dict(zip(list(i.strip() for i in rootinput[0]), rootinput[1]))

# CROSS SECTION(S) (pb):
xsec    = eval(rootinput['xsec']) #FIXME

# PDF "_"+LABEL FOR OUTPUT FILES:
JOB     = eval(rootinput['JOB'])
PDF     = eval(rootinput['PDF']) #FIXME
scale   = eval(rootinput['scale']) #bug, use False, carefull with Nevts
cuts    = eval(rootinput['cuts'])
setLog  = eval(rootinput['setLog'])
filled  = eval(rootinput['filled'])
stacked = eval(rootinput['stacked'])
data    = eval(rootinput['data'])

# PARTICLES OF INTEREST
IDS     = eval(rootinput['IDS'])


# KINEMATICAL CUTS: #FIXME
INVMCUTUPPER   =eval(rootinput['INVMCUTUPPER'])
INVMCUTLOWER   =eval(rootinput['INVMCUTLOWER'])
                                
PTPAIRCUTUPPER =eval(rootinput['PTPAIRCUTUPPER'])
PTPAIRCUTLOWER =eval(rootinput['PTPAIRCUTLOWER'])
                                
ETACUT         =eval(rootinput['ETACUT'])
ETAPAIRCUT     =eval(rootinput['ETAPAIRCUT'])
INNER          =eval(rootinput['INNER'])
                                
PTCUTUPPER     =eval(rootinput['PTCUTUPPER'])
PTCUTLOWER     =eval(rootinput['PTCUTLOWER'])

# INPUT FILES:

#processo 3
FILES   = eval(rootinput['FILES'])#FIXME


# EVENT SAMPLE INPUT:
Nevt    = eval(rootinput['Nevt']) #FIXME
Nmax    = eval(rootinput['Nmax']) # number of max events to obtain from samples
EVTINPUT= str(int(Nevt/1000))+"k";
SQRTS   = eval(rootinput['SQRTS']) # in GeV

#####################################################################

# LABELS:
STRING	= "";
for m in range(len(PDF)):
	if (PDF[m]==PDF[-1]):
		STRING+=PDF[m]+"_";
	else:
		STRING+=PDF[m]+"-";

LABEL = JOB
if cuts: LABEL+="_CUTS"
if INNER: LABEL+='_INNER'
if scale: LABEL+="_SCALED"
if setLog: LABEL+="_LOG"
if filled: LABEL+="_FILLED"
if stacked: LABEL+="_STACKED"
if data: LABEL+="_DATA"

# IMAGE FORMATS TO BE CREATED:
FILE_TYPES = [LABEL+".png"];
print ("*****");
print ("Os arquivos gravados em %s" % (FILE_TYPES[0]));
print ("*****");
# SAVING HISTOS INTO ROOT FILE:
FILEROOT = TFile(LABEL+".root","RECREATE");

# CREATE INDIVIDUAL DIRS FOR IMAGE TYPES:
#print(len(FILE_TYPES))
for l in range(len(FILE_TYPES)):
	call(["mkdir","-p",FILE_TYPES[l]]);

#####################################################################

# ARRAYS FOR EACH TYPE OF DISTRIBUTIONS:
#
# 1D:
protpz       = []
proten       = []
protxi       = []
protpt       = []
proteta      = []
ivmprot      = []
mupz         = []
muen         = []
mupt         = []
ivmmu        = []
mueta        = []
phopz        = []
phopt        = []
phoen        = []
phoivm       = []
phopsrap2    = []
phopsrap1    = []
phoY         = []

# 2D:
DDivmprotmmumu   = []
DDxipximu        = []


# SORTING THE DISTRIBUTIONS WITHIN THE SETS:

# 1D
histoslog  = [protpz,proten,protxi,protpt,proteta,ivmprot,mupz,muen,mupt,ivmmu,mueta,phopz,phopt,phoen,phoivm,phopsrap2,phopsrap1,phoY]

# 2D
DDlog      = [DDivmprotmmumu,DDxipximu] 

#------------ Lists for KS test ----------------------

KS_ivm_pp = list([] for i in range(len(FILES)))
KS_ivm_mu = list([] for i in range(len(FILES)))
KS_protxi = list([] for i in range(len(FILES)))

#-----------------------------------------------------

def fill(tlvs, histoslog, DDlog, first, mode):
    IDS = tlvs[1::2]
    if first:
        # 1D
        # Proton
        protpz.append(TH1D("1D_"+mode+"_protpz"+"_"+PDF[i]       , "", 50,4000., 7000.))
        proten.append(TH1D("1D_"+mode+"_proten"+"_"+PDF[i]       , "", 50,0., 10000.))
        protxi.append(TH1D("1D_"+mode+"_protxi"+"_"+PDF[i]       , "", 50,-0.003,0.4))
        protpt.append(TH1D("1D_"+mode+"_protpt"+"_"+PDF[i]       , "", 50,-0.1, 1.))
        proteta.append(TH1D("1D_"+mode+"_proteta"+"_"+PDF[i]       , "", 50,-20., 20.))
        ivmprot.append(TH1D("1D_"+mode+"_ivmprot"+"_"+PDF[i]       , "", 50,-10., 12000.))
        # Muon
        mupz.append(TH1D("1D_"+mode+"_mupz"+"_"+PDF[i]       , "", 50,-2500.,2500.))
        muen.append(TH1D("1D_"+mode+"_muen"+"_"+PDF[i]       , "", 50,-100., 900.))
        mupt.append(TH1D("1D_"+mode+"_mupt"+"_"+PDF[i]       , "", 50,-5., 40.0))
        ivmmu.append(TH1D("1D_"+mode+"_ivmmu"+"_"+PDF[i]       , "", 50,0., 120.0))
        mueta.append(TH1D("1D_"+mode+"_mueta"+"_"+PDF[i]       , "", 50,-15., 15.))
        # Photon
        phopz.append(TH1D("1D_"+mode+"_phopz"+"_"+PDF[i]       , "", 50,-10., 100.))
        phopt.append(TH1D("1D_"+mode+"_phopt"+"_"+PDF[i]       , "", 50,0., 50.))
        phoen.append(TH1D("1D_"+mode+"_phoen"+"_"+PDF[i]       , "", 50,-100., 500.))
        phoivm.append(TH1D("1D_"+mode+"_phoivm"+"_"+PDF[i]     , "", 50, 0, 350))
        phopsrap2.append(TH1D('1D_'+mode+'_phopsrap2'+'_'+PDF[i] , '', 50, -1, 1))
        phopsrap1.append(TH1D('1D_'+mode+'_phopsrap1'+'_'+PDF[i] , '', 50, -10, 10))
        phoY.append(TH1D('1D_'+mode+'_phoY'+'_'+PDF[i]         , '', 50, -10000, 100))
        # Monopole
        #mopz.append(TH1D("1D_"+mode+"_mupz"+"_"+PDF[i]       , "", 50,-2500.,2500.))
        #moen.append(TH1D("1D_"+mode+"_muen"+"_"+PDF[i]       , "", 50,-100., 900.))
        #mopt.append(TH1D("1D_"+mode+"_mupt"+"_"+PDF[i]       , "", 50,-5., 40.0))

        # 2D
        DDivmprotmmumu.append(TH2D('2D_'+mode+'_DDivmprotmmumu_'+PDF[i]       , '', 50, 0., 1400., 50, 0., 1400.))
        DDxipximu.append(TH2D('2D_'+mode+'_DDxipximu_'+PDF[i]     , '', 50, 0., 1., 50, 0., 1.))

    # 1D:
    #-------------------------Proton mesurements
    if 2212 in IDS:
        index = tlvs.index(2212)
        dpp = tlvs[index-1]
        tlvs.pop(index)
        tlvs.pop(index-1)
        index = tlvs.index(2212)
        dpm = tlvs[index-1]
        tlvs.pop(index)
        tlvs.pop(index-1)
        protpz[i].Fill(dpp.Pz());
        protpz[i].Fill(dpm.Pz());
        proten[i].Fill(dpp.E())
        proten[i].Fill(dpm.E())
        protxi[i].Fill(1-(dpp.Pz()/(SQRTS/2)))
        protxi[i].Fill(1-(dpm.Pz()/(-(SQRTS/2))))
        ivmprot[i].Fill(sqrt((1-(dpp.Pz()/(SQRTS/2)))*(1-(dpm.Pz()/(-(SQRTS/2)))))*SQRTS)
        protpt[i].Fill(dpp.Pt())
        protpt[i].Fill(dpm.Pt())
        proteta[i].Fill(dpp.Eta())
        proteta[i].Fill(dpm.Eta())
    #-------------------------Múon mesurements
    if 13 in IDS or -13 in IDS:
        index = tlvs.index(13)
        dmu = tlvs[index-1]
        tlvs.pop(index)
        tlvs.pop(index-1)
        index = tlvs.index(-13)
        damu = tlvs[index-1]
        tlvs.pop(index)
        tlvs.pop(index-1)
        mupz[i].Fill(dmu.Pz())
        muen[i].Fill(dmu.E())
        muen[i].Fill(damu.E())
        mupt[i].Fill(dmu.Pt())
        mupt[i].Fill(damu.Pt())
        ivmmu[i].Fill((dmu+damu).M())
        mueta[i].Fill(dmu.Eta())
        mueta[i].Fill(damu.Eta())
    #-------------------------Photon mesurements
    if 22 in IDS:
        index = tlvs.index(22)
        dp = tlvs[index-1]
        tlvs.pop(index)
        tlvs.pop(index-1)
        index = tlvs.index(22)
        dm = tlvs[index-1]
        tlvs.pop(index)
        tlvs.pop(index-1)
        phopt[i].Fill(dp.Pt())
        phopt[i].Fill(dm.Pt())
        phopz[i].Fill(dp.Pz())
        phopz[i].Fill(dm.Pz())
        phoen[i].Fill(dm.E())
        phoen[i].Fill(dp.E())
        phoivm[i].Fill((dp+dm).M())
        phopsrap2[i].Fill((dp+dm).Eta())
        phopsrap1[i].Fill(dp.Eta())
        phopsrap1[i].Fill(dm.Eta())               
        phoY[i].Fill(dp.Y())
        phoY[i].Fill(dm.Y())
    #-------------------------Monopole mesurements
    if 90 in IDS: # Monopole not coded to have cuts yet 
        index = tlvs.index(22)
        dmo = tlvs[index-1]
        tlvs.pop(index)
        tlvs.pop(index-1)
        mopz[i].Fill(dmo.Pz())
        moen[i].Fill(dmo.E())
        mopt[i].Fill(dmo.Pt())
    #-------------------------Mesurements for the KS test
    if 13 in IDS and -13 in IDS:
        KS_ivm_pp[i].append(sqrt((1-(dpp.Pz()/(SQRTS/2)))*(1-(dpm.Pz()/(-(SQRTS/2)))))*SQRTS)
        KS_protxi[i].append(1-(dpp.Pz()/(SQRTS/2)))
        KS_protxi[i].append(1-(dpm.Pz()/(-(SQRTS/2))))
        KS_ivm_mu[i].append((dmu+damu).M())
    # 2D:
    if 13 in IDS and -13 in IDS and 2212 in IDS:
        DDivmprotmmumu[i].Fill(sqrt((1-(dpp.Pz()/(SQRTS/2)))*(1-(dpm.Pz()/(-(SQRTS//2)))))*SQRTS, (dmu+damu).M())
        DDxipximu[i].Fill(1-(dpp.Pz()/(SQRTS/2)), (1/SQRTS)*(dmu.Pt()*exp(dmu.Eta())+damu.Pt()*exp(damu.Eta())))




# STARTING THE LOOP OVER FILES:
for i in range(len(FILES)):
    f = open(FILES[i],'r');
    print (f"Opening file {i}: {FILES[i]}");

    # SORTING THE DISTRIBUTIONS IN THE ARRAYS FOR EACH FILE:
    # EACH ARRAYS IS FORMATTED LIKE: array[] = [plots_file1, plots_file2, plots_file3, ...

    # LOOP OVER LINES IN LHE SAMPLE:

    # Flags for differentiating particles
    first_photon = False
    first_muon   = False
    first_proton = False

    # Flag to create histograms
    first = 1

    # RESET EVENT COUNTING:
    event  = 0;
    evPASS = 0;
    # START LOOP: <<<<<<<<<<<<<<<<!!! REMMEMBER TO COUNT CORRECTLY HERE
    if (i == 0):
        for j in range(344): # skip first 434 lines to avoid comments
            f.readline()
    elif (i == 1):
        for j in range(344): # skip first 431 lines to avoid comments
            f.readline()
    elif (i == 2):
        for j in range(7): # skip first 430 lines to avoid comments
            f.readline()
    elif (i == 3):
        for j in range(8): # skip first 440 lines to avoid comments
            f.readline();
    for line in f:
        # SKIP BLANK LINES:
        line = line.strip();
        if not line: continue;
        # STORE LINES INTO ARRAY:
        coll = line.split();
        # READ EVENT CONTENT:
        if coll[0] == "<event>":
            # CREATING LIST OF TLORETZVECTORS
            TLVS = []
            event += 1;
            # SET A SCREEN OUTPUT FOR CONTROL:
            if Nevt < 10000: evtsplit = 1000;
            else: evtsplit = 10000;
            perct = event / Nevt * 100.;
            if event%evtsplit==0: print ("Event %i [%.2f%%]" % (event,perct));
            elif event>Nevt: break;
        # 4-VECTORS FOR DECAY PRODUCTS:
        elif coll[0] == '22' and coll[1] == '1' and first_photon == False:
            dp = TLorentzVector();
            px = float(coll[6]);
            py = float(coll[7]);
            pz = float(coll[8]);
            en = float(coll[9]);
            dp.SetPxPyPzE(px,py,pz,en)
            first_photon = True
            TLVS.append(dp)
            TLVS.append(22)
        elif coll[0] == '22' and coll[1] == '1' and first_photon:
            dm = TLorentzVector();
            px = float(coll[6]);
            py = float(coll[7]);
            pz = float(coll[8]);
            en = float(coll[9]);
            dm.SetPxPyPzE(px,py,pz,en);
            first_photon = False
            TLVS.append(dm)
            TLVS.append(22)
        elif coll[0] == '13' and coll[1] == '1' and first_muon == False:
            dmu = TLorentzVector();
            px = float(coll[6]);
            py = float(coll[7]);
            pz = float(coll[8]);
            en = float(coll[9]);
            dmu.SetPxPyPzE(px,py,pz,en);
            first_muon = True
            TLVS.append(dmu)
            TLVS.append(13)
        elif coll[0] == '-13' and coll[1] == '1' and first_muon:
            damu = TLorentzVector();
            px = float(coll[6]);
            py = float(coll[7]);
            pz = float(coll[8]);
            en = float(coll[9]);
            damu.SetPxPyPzE(px,py,pz,en);
            first_muon = False
            TLVS.append(damu)
            TLVS.append(-13)
        elif coll[0] == '90':
            dmo = TLorentzVector();
            px = float(coll[6]);
            py = float(coll[7]);
            pz = float(coll[8]);
            en = float(coll[9]);
            dmo.SetPxPyPzE(px,py,pz,en)
            TLVS.append(dmo)
            TLVS.append(90)
        elif coll[0] == '2212' and coll[1] == '1' and first_proton == False and abs(eval(coll[8])) < (SQRTS/2):
            dpp = TLorentzVector();
            px = float(coll[6]);
            py = float(coll[7]);
            pz = float(coll[8]);
            en = float(coll[9]);
            dpp.SetPxPyPzE(px,py,pz,en)
            first_proton = True
            TLVS.append(dpp)
            TLVS.append(2212)
        elif coll[0] == '2212' and coll[1] == '1' and first_proton and abs(eval(coll[8])) < (SQRTS/2):
            dpm = TLorentzVector();
            px = float(coll[6]);
            py = float(coll[7]);
            pz = float(coll[8]);
            en = float(coll[9]);
            dpm.SetPxPyPzE(px,py,pz,en)
            first_proton = False
            TLVS.append(dpm)
            TLVS.append(2212)
        #CLOSE EVENT AND FILL HISTOGRAMS:
        elif coll[0] == "</event>":
            # KINEMATICS OF DECAY PRODUCTS:
            if cuts and INNER:
                fill(TLVS, histoslog, DDlog, first, 'CUTS-INNER')
                first = 0

                evPASS += 1
            elif cuts and not INNER:
                fill(TLVS, histoslog, DDlog, first, 'CUTS')
                first = 0

                evPASS += 1;
            elif not cuts:
                fill(TLVS, histoslog, DDlog, first, 'NO-CUTS')
                first = 0

                evPASS += 1
        # End of loop over lines
        if evPASS >= Nmax: break   
    #print(phoivm[i].Integral())
    if cuts: print ("Events passing acceptance: %i/%i" % (evPASS,event));
        #print ("Integral of %s: %.6f nb" % (PDF[i],evPASS*xsec[i]/event));
# End of loop over files

#############################################################
#
#-----------------------KS TEST------------------------------
#
#############################################################

#with open(f'ks-test.txt', 'w') as f:
#    f.write('>>>>>>>KOLMOGOROV-SMIRNOV TEST<<<<<<<\n\n')
#    f.write(f'Invariant-Mass protons\n')
#    for i in range(4):
#        for j in range(i+1, 4):
#            ks = TMath.KolmogorovTest(len(KS_ivm_pp[i]), array('d', sorted(KS_ivm_pp[i])), len(KS_ivm_pp[j]), array('d', sorted(KS_ivm_pp[j])), 'D') 
#            f.write(f'{PDF[i]:>10} X {PDF[j]:<10}: {ks}\n')
#    f.write(f'\nInvariant-Mass leptons\n')
#    for i in range(4):
#        for j in range(i+1, 4):
#            ks = TMath.KolmogorovTest(len(KS_ivm_mu[i]), array('d', sorted(KS_ivm_mu[i])), len(KS_ivm_mu[j]), array('d', sorted(KS_ivm_mu[j])), 'D')
#            f.write(f'{PDF[i]:>10} X {PDF[j]:<10}: {ks}\n')
#    f.write(f'\n\u03A7 of protons\n')
#    for i in range(4):
#        for j in range(i+1, 4):
#            ks = TMath.KolmogorovTest(len(KS_protxi[i]), array('d', sorted(KS_protxi[i])), len(KS_protxi[j]), array('d', sorted(KS_protxi[j])), 'D')
#            f.write(f'{PDF[i]:>10} X {PDF[j]:<10}: {ks}\n')

#############################################################
#
#-----------------------END OF KS TEST-----------------------
#
#############################################################
FILEROOT.Write()

#####################################################################
#
# C'ESTI FINI
#
#####################################################################
