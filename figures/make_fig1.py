# -*- coding: utf-8 -*-
"""Fig. 1 — tata letak ChatGPT, ukuran huruf disetarakan dengan gambar lama."""
from PIL import ImageFont
FT='/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf'
_c={}
def f(size,bold):
    k=(size,bold)
    if k not in _c: _c[k]=ImageFont.truetype(FT%('Bold' if bold else 'Regular'),size*4)
    return _c[k]
def wpx(s,size,bold=False): return f(size,bold).getlength(s)/4.0
def wrap(text,size,maxw,bold=False):
    out,cur=[],""
    for word in text.split():
        trial=(cur+" "+word).strip()
        if cur and wpx(trial,size,bold)>maxw: out.append(cur); cur=word
        else: cur=trial
    if cur: out.append(cur)
    return out

NAVY="#1F4E79"; EDGE="#9DC3E6"; BODY="#333333"; ARR="#808080"
TS, BS = 28, 24                      # px: judul dan isi
LH, PAD = 29, 18                     # tinggi baris, padding dalam kotak
W = 1650
C1X,C1W = 30, 300
C2X,C2W = 390, 330
C3X,C3W = 790, 500
C4X,C4W = 1350, 270

STAGES=[("A · Base-model selection",
         "Eight algorithms under an 80:20 split with the same 65 features (Table 2)"),
        ("B · Controlled experiment at n = 29",
         "Six categories trimmed one at a time to the same 29 training samples and the "
         "same balancing target, so only category varies. No handling, random oversampling "
         "and SMOTE, under Random Forest, XGBoost and a two-layer perceptron (Tables 3–5)"),
        ("C · Why the gains differ",
         "Geometry of the training subsets; where synthetic points intrude and where missed "
         "attacks are sent instead; feature overlap and restricted representation "
         "(Tables 6–9, 13–14)"),
        ("D · Robustness and attribution",
         "Nested ablation at 29, 50, 100 and 500 training samples; sensitivity to the SMOTE "
         "neighbourhood size and oversampling ratio; classifier capacity varied with the "
         "subset held fixed (Tables 10–12)"),
        ("E · Limits on a scarce category",
         "Twelve configurations on the 36-record Infiltration category; CSE-CIC-IDS2018 "
         "learning curve at 1:1 (Tables 15–17)")]
PREP=["drop non-numeric and constant columns","drop infinite and missing values",
      "scaling fitted on the training folds only","map labels to seven categories",
      "cap each category at 30,000 records"]
EVAL=["precision, recall and F1 per category","stratified five-fold cross-validation, three seeds",
      "resolution limit r, 95% Wilson intervals","Wilcoxon signed-rank tests on folds",
      "Spearman correlation across categories"]
DATA=[("CIC-IDS2017",["de-duplicated","124,127 records","65 features"]),
      ("CSE-CIC-IDS2018",["de-duplicated","Infiltration capture days"])]

TOP, GAP = 30, 30
s=[]
def rect(x,y,w,h,fill,stroke=None):
    e=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}"'
    if stroke: e+=f' stroke="{stroke}" stroke-width="2.5"'
    s.append(e+'/>')
def title_lines(t,maxw):
    return wrap(t,TS,maxw,bold=True)
def txt(x,y,t,size,fill,bold=False,anchor=None):
    a=f' text-anchor="{anchor}"' if anchor else ''
    b=' font-weight="bold"' if bold else ''
    t=t.replace('&','&amp;').replace('<','&lt;')
    s.append(f'<text x="{x}" y="{y}" font-size="{size}px" fill="{fill}"{b}{a}>{t}</text>')
def bullets(x,y,items,maxw,fill,gap_extra=0):
    """butir dengan indentasi gantung; mengembalikan y setelah butir terakhir"""
    for it in items:
        for i,ln in enumerate(wrap(it,BS,maxw-16)):
            txt(x+(0 if i==0 else 16), y, ("• " if i==0 else "")+ln, BS, fill)
            y+=LH
        y+=gap_extra
    return y

# ---- kolom 3: kotak tahapan, tinggi mengikuti isi -----------------------------
boxes=[]; y=TOP
for title,body in STAGES:
    lines=wrap(body,BS,C3W-2*PAD)
    h=PAD+TS+10+len(lines)*LH+PAD-6
    boxes.append((y,h,title,lines)); y+=h+GAP
H=y-GAP+TOP                                    # tinggi kanvas
col_top, col_bot = boxes[0][0], boxes[-1][0]+boxes[-1][1]

# ---- panah --------------------------------------------------------------------
d2_h=lambda lines: PAD+TS+6+len(lines)*LH+PAD-6
dbox=[(t,ls,d2_h(ls)) for t,ls in [(t,[l for l in b]) for t,b in DATA]]
dh=[PAD+len(title_lines(t,C1W-2*PAD))*(TS+4)+10+
     sum(len(wrap(x,BS,C1W-2*PAD)) for x in b)*LH+PAD-6 for t,b in DATA]
p_lines=sum(len(wrap(i,BS,C2W-2*PAD-16)) for i in PREP)
ph=PAD+len(title_lines("Identical preprocessing",C2W-2*PAD))*(TS+4)+14+p_lines*LH+4*6+PAD-6
py=(col_top+col_bot)/2-ph/2
d1y=py-70-dh[0]; d2y=py+ph+70
if d1y<col_top: d1y=col_top
if d2y+dh[1]>col_bot: d2y=col_bot-dh[1]

spine=C3X-28
s.append(f'<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" '
         f'orient="auto" markerUnits="userSpaceOnUse">'
         f'<path d="M 0 0 L 9 4.5 L 0 9 Z" fill="{ARR}"/></marker></defs>')
g=[f'<g fill="none" stroke="{ARR}" stroke-width="2.5">']
mid1=d1y+dh[0]/2; mid2=d2y+dh[1]/2
j=(C1X+C1W+C2X)/2
g.append(f'<path d="M {C1X+C1W} {mid1:.0f} H {j:.0f} V {py+ph*0.28:.0f} H {C2X-9}" marker-end="url(#arrow)"/>')
g.append(f'<path d="M {C1X+C1W} {mid2:.0f} H {j:.0f} V {py+ph*0.72:.0f} H {C2X-9}" marker-end="url(#arrow)"/>')
g.append(f'<path d="M {C2X+C2W} {py+ph/2:.0f} H {spine}"/>')
first=boxes[0][0]+boxes[0][1]/2; last=boxes[-1][0]+boxes[-1][1]/2
g.append(f'<path d="M {spine} {first:.0f} V {last:.0f}"/>')
for by,bh,_,_ in boxes:
    cy=by+bh/2
    g.append(f'<path d="M {spine} {cy:.0f} H {C3X-9}" marker-end="url(#arrow)"/>')
    g.append(f'<path d="M {C3X+C3W} {cy:.0f} H {C4X-9}" marker-end="url(#arrow)"/>')
g.append('</g>'); s+=g

# ---- kotak ---------------------------------------------------------------------
for (title,body),by,bh in zip(DATA,[d1y,d2y],dh):
    rect(C1X,by,C1W,bh,NAVY)
    yy=by+PAD+TS-8
    for ln in title_lines(title,C1W-2*PAD):
        txt(C1X+C1W/2,yy,ln,TS,"#FFFFFF",bold=True,anchor="middle"); yy+=TS+4
    yy+=10+BS-TS
    for b in body:
        for ln in wrap(b,BS,C1W-2*PAD):
            txt(C1X+C1W/2,yy,ln,BS,"#FFFFFF",anchor="middle"); yy+=LH

rect(C2X,py,C2W,ph,NAVY)
pt_=title_lines("Identical preprocessing",C2W-2*PAD)
yy=py+PAD+TS-8
for ln in pt_: txt(C2X+C2W/2,yy,ln,TS,"#FFFFFF",bold=True,anchor="middle"); yy+=TS+4
bullets(C2X+PAD,yy+14+BS-TS,PREP,C2W-2*PAD,"#FFFFFF",gap_extra=6)

for by,bh,title,lines in boxes:
    rect(C3X,by,C3W,bh,"#FFFFFF",EDGE)
    txt(C3X+PAD,by+PAD+TS-8,title,TS,NAVY,bold=True)
    yy=by+PAD+TS+10+BS-8
    for ln in lines: txt(C3X+PAD,yy,ln,BS,BODY); yy+=LH

eh=col_bot-col_top
rect(C4X,col_top,C4W,eh,NAVY)
txt(C4X+C4W/2,col_top+PAD+TS-8,"Evaluation",TS,"#FFFFFF",bold=True,anchor="middle")
nl=sum(len(wrap(i,BS,C4W-2*PAD-16)) for i in EVAL)
free=eh-(PAD+TS+24)-nl*LH-PAD
bullets(C4X+PAD,col_top+PAD+TS+24+BS-8,EVAL,C4W-2*PAD,"#FFFFFF",gap_extra=free/4.4)

svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" '
     f'viewBox="0 0 {W} {H:.0f}" font-family="Arial, Helvetica, sans-serif">'
     f'<rect width="{W}" height="{H:.0f}" fill="#FFFFFF"/>'+"".join(s)+'</svg>')
open('fig1.svg','w').write(svg)
sc=468.0/W
print(f"kanvas {W} x {H:.0f}  rasio {W/H:.2f}  -> pada 6,5 inci: tinggi {6.5*H/W:.2f} inci")
print(f"huruf judul {TS}px = {TS*sc:.1f} pt   isi {BS}px = {BS*sc:.1f} pt")
