"""Draw original native-resolution pixel assets. No source images are modified.
Run from any directory with Python + Pillow. Not needed to install the mod.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Sprites'
OUT.mkdir(exist_ok=True)

base = Image.new('RGBA', (32, 32))
b = ImageDraw.Draw(base)
b.ellipse((3, 13, 29, 31), fill='#252a30')
b.rectangle((3, 19, 29, 24), fill='#40474c')
b.ellipse((3, 16, 29, 30), fill='#515960')
# Individually placed masonry courses.
for xy, c in [((4,19,9,23),'#88908c'),((11,21,16,25),'#727c7b'),
              ((18,21,23,25),'#5d696c'),((25,18,28,23),'#414d55'),
              ((5,25,10,27),'#747f7b'),((12,27,18,29),'#5e696b'),
              ((20,26,25,28),'#47555e')]:
    b.rectangle(xy, fill=c)
b.ellipse((3, 12, 29, 24), fill='#303b42')
b.ellipse((4, 12, 28, 22), fill='#a1a69a')
b.ellipse((8, 14, 24, 20), fill='#273946')
b.ellipse((10, 16, 23, 20), fill='#17649c')
b.line((12, 18, 16, 18), fill='#49b7d6')
b.line((18, 17, 21, 17), fill='#2d91c0')
for a,z in [((7,14),(9,15)),((12,12),(13,14)),((21,13),(21,14)),
            ((26,16),(24,17)),((9,20),(10,22)),((16,21),(16,23)),((23,20),(24,22))]:
    b.line((a,z), fill='#525e63')
b.line((5,17,6,15), fill='#ccd0bb')
b.line((10,13,12,13), fill='#c5caba')
b.line((12,23,18,23), fill='#707c7c')

upper = Image.new('RGBA', (32, 32))
u = ImageDraw.Draw(upper)
# Asymmetric isometric timber frame with a diagonal windlass.
u.polygon([(2,21),(4,19),(7,21),(6,24),(3,24)], fill='#45413b')
u.polygon([(24,26),(26,24),(30,26),(29,29),(25,29)], fill='#403a32')
u.rectangle((3,2,6,21), fill='#503520')
u.rectangle((3,3,4,20), fill='#a07840')
u.line((5,4,5,19), fill='#77532c')
u.rectangle((25,9,28,26), fill='#513820')
u.rectangle((25,10,26,25), fill='#956c37')
u.line((27,11,27,24), fill='#71502a')
u.polygon([(5,4),(7,2),(27,10),(27,14),(25,15),(5,7)], fill='#593c22')
u.polygon([(5,4),(7,3),(27,11),(25,12)], fill='#bc9250')
u.line((6,5,25,13), fill='#99703a', width=2)
for x,y in [(3,6),(25,13),(3,18),(25,23)]:
    u.rectangle((x,y,x+3,y+1), fill='#444c50')
    u.point((x,y), fill='#a4aaa3')
for x,y in [(13,5),(15,6),(17,7)]:
    u.line((x,y,x-1,y+4), fill='#d1b581')
u.line((16,11,16,18), fill='#99713b')
u.line((16,11,16,16), fill='#d0ae70')
u.line((28,12,30,13), fill='#777f79')
u.line((30,13,30,16), fill='#6c4726')
u.line((29,16,31,17), fill='#b08a4b')

bucket = Image.new('RGBA', (16,16))
k = ImageDraw.Draw(bucket)
k.ellipse((2,2,13,12), outline='#51504c')
k.ellipse((3,2,12,11), outline='#a5a398')
k.polygon([(2,6),(13,6),(12,13),(10,15),(5,15),(3,13)], fill='#493322')
k.polygon([(3,6),(12,6),(11,13),(9,14),(5,14),(4,12)], fill='#916538')
k.line((5,8,6,13), fill='#ba8c48')
k.line((8,8,8,14), fill='#674629')
k.line((11,8,10,13), fill='#674629')
k.line((3,10,12,10), fill='#575e5c')
k.line((4,11,11,11), fill='#a0a394')
k.line((5,14,10,14), fill='#555c59')
k.ellipse((2,4,13,8), fill='#c79b53')
k.ellipse((3,5,12,7), fill='#174b75')
k.line((4,6,11,6), fill='#2589ba')
k.line((5,5,8,5), fill='#74d3e2')
k.point((10,6), fill='#b3edeb')

atlas = Image.new('RGBA',(128,32))
atlas.paste(base,(0,0))
atlas.paste(upper,(32,0))
atlas.paste(bucket,(64,0))
# Match the vanilla atlas's magenta color-key background.
# Keep previews in conventional RGBA, but encode the game texture like default.png.
keyed_atlas = atlas.copy()
for yy in range(keyed_atlas.height):
    for xx in range(keyed_atlas.width):
        if keyed_atlas.getpixel((xx, yy))[3] == 0:
            keyed_atlas.putpixel((xx, yy), (255, 0, 255, 255))
keyed_atlas.save(OUT / 'water-distillery.png')
well = Image.alpha_composite(base, upper)
well.save(OUT / 'brewing-well-preview.png')
bucket.save(OUT / 'water-bucket-preview.png')

# Build an inspection sheet by drawing each source pixel as a sharp square.
preview = Image.new('RGB',(760,380),'#171d28')
p = ImageDraw.Draw(preview)
p.text((24,18),'WATER DISTILLERY | native pixel sprites',fill='#dae5ee')
for im,x,y,s,label in [(well,36,63,8,'Brewing Well | 32 x 32'),
                        (bucket,408,114,12,'Water bucket | 16 x 16')]:
    for yy in range(im.height):
        for xx in range(im.width):
            rgba=im.getpixel((xx,yy))
            if rgba[3]:
                p.rectangle((x+xx*s,y+yy*s,x+(xx+1)*s-1,y+(yy+1)*s-1),fill=rgba[:3])
    p.text((x,337),label,fill='#a4b5c6')
preview.save(ROOT / 'artwork-preview.png')
print('Created water-distillery.png: 128x32 RGBA; well layers 32x32; bucket 16x16.')
