#!/usr/bin/env python3
"""Detect spectral bands in SIGPROC .fil data; export per-band time-series Greek numerals.

Outputs: bands.csv, streams.csv, metadata.json. No REDSigma assembly is executed.
"""
import argparse, csv, json, math, struct
from pathlib import Path
import numpy as np
from scipy.ndimage import median_filter, gaussian_filter1d
from scipy.signal import find_peaks

STRINGS={'source_name','rawdatafile','project_id','observer'}
INTS={'machine_id','telescope_id','data_type','nchans','nbeams','ibeam','nbits','nifs','barycentric','pulsarcentric','signed','nsamples','sumifs','npol','nbins'}
DOUBLES={'az_start','za_start','src_raj','src_dej','tstart','tsamp','fch1','foff','refdm','period','fchannel','dm','accel'}
VALUES=[(900,'Ϡ'),(800,'Ω'),(700,'Ψ'),(600,'Χ'),(500,'Φ'),(400,'Υ'),(300,'Τ'),(200,'Σ'),(100,'Ρ'),(90,'Ϟ'),(80,'Π'),(70,'Ο'),(60,'Ξ'),(50,'Ν'),(40,'Μ'),(30,'Λ'),(20,'Κ'),(10,'Ι'),(9,'Θ'),(8,'Η'),(7,'Ζ'),(6,'Ϛ'),(5,'Ε'),(4,'Δ'),(3,'Γ'),(2,'Β'),(1,'Α')]

def greek(n):
    n=int(n)
    if n<0:return '-'+greek(-n)
    if n==0:return '0'
    chunks=[]
    while n:
        v=n%1000;n//=1000
        s='';
        for amount,letter in VALUES:
            while v>=amount:
                s+=letter;v-=amount
        chunks.append(s or '0')
    return ' | '.join(reversed(chunks))

def read_header(f):
    def key():
        raw=f.read(4)
        if len(raw)!=4:raise ValueError('Incomplete SIGPROC header')
        n=struct.unpack('<i',raw)[0]
        if not 1<=n<=128:raise ValueError('Invalid SIGPROC header field length')
        return f.read(n).decode('ascii')
    if key()!='HEADER_START':raise ValueError('Not a SIGPROC filterbank (.fil) file')
    hdr={}
    while True:
        k=key()
        if k=='HEADER_END':break
        if k in STRINGS:hdr[k]=key()
        elif k in INTS:hdr[k]=struct.unpack('<i',f.read(4))[0]
        elif k in DOUBLES:hdr[k]=struct.unpack('<d',f.read(8))[0]
        else:raise ValueError(f'Unknown header key {k!r}; add its type to parser')
    return hdr,f.tell()

def detect(spec, max_bands, threshold, min_separation):
    # Robust, locally normalized residual: find peaks even with tilted bandpass.
    smooth=gaussian_filter1d(spec.astype('float64'),1.5)
    baseline=median_filter(smooth,size=max(51,(len(spec)//100)|1),mode='nearest')
    resid=smooth-baseline
    noise=1.4826*np.median(np.abs(resid-np.median(resid)))+1e-12
    peaks,props=find_peaks(resid,prominence=threshold*noise,distance=min_separation)
    ranked=sorted(peaks,key=lambda p:resid[p],reverse=True)[:max_bands]
    return sorted(int(p) for p in ranked),noise

def extract(args):
    src=Path(args.input);dest=Path(args.output or (src.stem+'_bands'));dest.mkdir(parents=True,exist_ok=True)
    with src.open('rb') as f:hdr,offset=read_header(f)
    nc=int(hdr['nchans']);ni=int(hdr.get('nifs',1));nb=int(hdr['nbits'])
    if nb not in (8,16,32,64):raise ValueError('Supported bit depths: 8,16,32,64')
    dtype={8:'u1',16:'<i2',32:'<f4',64:'<f8'}[nb]
    frame_bytes=nc*ni*(nb//8)
    count=(src.stat().st_size-offset)//frame_bytes
    if args.max_frames:count=min(count,args.max_frames)
    if count<1:raise ValueError('No complete frames')
    # SIGPROC layout: [time, IF, channel]. Memory-map instead of loading entire file.
    data=np.memmap(src,dtype=dtype,mode='r',offset=offset,shape=(count,ni,nc))
    scan=min(count,args.scan_frames)
    indexes=np.linspace(0,count-1,scan,dtype=int)
    bands=[]
    for i in range(ni):
        spectrum=np.median(data[indexes,i,:].astype('float64'),axis=0)
        peaks,noise=detect(spectrum,args.max_bands,args.threshold,args.min_separation)
        if not peaks and args.fallback_peak:peaks=[int(np.argmax(spectrum))]
        for p in peaks:
            # Locate half-prominence edges of locally baseline-subtracted band.
            left=max(0,p-args.half_width);right=min(nc-1,p+args.half_width)
            bands.append({'stream_id':f'IF{i+1}_B{len([b for b in bands if b["if_index"]==i])+1}',
                'if_index':i,'peak_channel':p,'start_channel':left,'end_channel':right,
                'peak_frequency_MHz':hdr['fch1']+p*hdr['foff'],
                'start_frequency_MHz':hdr['fch1']+left*hdr['foff'],
                'end_frequency_MHz':hdr['fch1']+right*hdr['foff'],
                'scan_median_peak':float(spectrum[p]),'noise_estimate':float(noise)})
    with (dest/'bands.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(bands[0]) if bands else ['stream_id','if_index','peak_channel']);writer.writeheader();writer.writerows(bands)
    with (dest/'streams.csv').open('w',newline='',encoding='utf-8') as f:
        fields=['frame','seconds','stream_id','if_index','channel','frequency_MHz','amplitude','rounded_integer','gematria','band_sum','band_sum_integer','band_sum_gematria']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for t in range(count):
            for b in bands:
                i=b['if_index'];lo=b['start_channel'];hi=b['end_channel']+1
                section=np.asarray(data[t,i,lo:hi],dtype='float64')
                if not np.isfinite(section).any():continue
                p=lo+int(np.nanargmax(section));v=float(data[t,i,p]);total=float(np.nansum(section))
                rounded=int(math.floor(v+0.5)) if v>=0 else -int(math.floor(-v+0.5))
                total_int=int(math.floor(total+0.5)) if total>=0 else -int(math.floor(-total+0.5))
                writer.writerow({'frame':t,'seconds':t*hdr.get('tsamp',1),'stream_id':b['stream_id'],
                    'if_index':i,'channel':p,'frequency_MHz':hdr['fch1']+p*hdr['foff'],
                    'amplitude':format(v,'.9g'),'rounded_integer':rounded,'gematria':greek(rounded),
                    'band_sum':format(total,'.9g'),'band_sum_integer':total_int,'band_sum_gematria':greek(total_int)})
    meta={'source':str(src),'header':hdr,'frames_processed':count,'bands_detected':len(bands),
          'scan_frames':scan,'threshold_MAD':args.threshold,'half_width_channels':args.half_width,
          'encoding':'round-half-away-from-zero; decimal groups of 3, Greek numeral mapping',
          'note':'Spectral peak extraction and numerical encoding; no assembly transforms or linguistic translation.'}
    (dest/'metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'{count} frames, {ni} IFs, {len(bands)} bands -> {dest}')
    for b in bands:print(b['stream_id'],f"{b['peak_frequency_MHz']:.6f} MHz",'channel',b['peak_channel'])

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',help='SIGPROC .fil input')
    p.add_argument('-o','--output',help='output directory')
    p.add_argument('--scan-frames',type=int,default=64,help='frames sampled for spectral detection')
    p.add_argument('--max-frames',type=int,help='limit frames for testing')
    p.add_argument('--max-bands',type=int,default=16,help='maximum peaks per IF')
    p.add_argument('--threshold',type=float,default=5.,help='peak prominence in robust noise units')
    p.add_argument('--min-separation',type=int,default=32,help='minimum channel spacing')
    p.add_argument('--half-width',type=int,default=8,help='channels on either side of each detected peak')
    p.add_argument('--fallback-peak',action='store_true',help='emit strongest peak when no bands pass threshold')
    args=p.parse_args()
    if args.scan_frames<1 or args.max_bands<1 or args.half_width<0: p.error('invalid positive settings')
    extract(args)
if __name__=='__main__':main()
