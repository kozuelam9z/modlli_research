import sys, math
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGB')
cols = [(112,242),(248,378),(384,514),(520,650),(655,785),(791,921),(930,1060),(1066,1196)]
rows = [(198,326),(381,509),(563,693)]
names = ['orig','recon','+light','+dark','+red','+yellow','+pale','-pale']
def lin(c):
    c/=255
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lab(r,g,b):
    r,g,b = lin(r),lin(g),lin(b)
    X=(0.4124*r+0.3576*g+0.1805*b)/0.95047
    Y=(0.2126*r+0.7152*g+0.0722*b)
    Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    L=116*f(Y)-16; a=500*(f(X)-f(Y)); bb=200*(f(Y)-f(Z))
    return L,a,bb
def patch(x0,y0,w=14,h=14):
    px=[im.getpixel((x,y)) for x in range(x0,x0+w) for y in range(y0,y0+h)]
    r=sum(p[0] for p in px)/len(px); g=sum(p[1] for p in px)/len(px); b=sum(p[2] for p in px)/len(px)
    return lab(r,g,b)
for ri,(y0,y1) in enumerate(rows):
    print('row',ri+1)
    for (x0,x1),n in zip(cols,names):
        tl=patch(x0+3,y0+3); tr=patch(x1-17,y0+3)
        L=(tl[0]+tr[0])/2; a=(tl[1]+tr[1])/2; b=(tl[2]+tr[2])/2
        h=math.degrees(math.atan2(b,a))
        print(f'  {n:8s} bgL={L:6.1f} a={a:6.1f} b={b:6.1f} h={h:6.1f}')
