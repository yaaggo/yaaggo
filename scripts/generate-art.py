from PIL import Image, ImageDraw, ImageFont
import math
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
frames=[]
for frame in range(48):
    im=Image.new('RGB',(720,250),'#0d1117')
    d=ImageDraw.Draw(im)
    angle=frame*2*math.pi/48
    vertices=[]
    for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
        x,z=x*math.cos(angle)+z*math.sin(angle),-x*math.sin(angle)+z*math.cos(angle)
        y,z=y*math.cos(.48)-z*math.sin(.48),y*math.sin(.48)+z*math.cos(.48)
        scale=66/(3.8-z)
        vertices.append((360+x*scale*2.3,125+y*scale*2.3))
    edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    cells=set()
    for a,b in edges:
        x1,y1=vertices[a]; x2,y2=vertices[b]
        for i in range(101):
            t=i/100
            cells.add((round((x1+(x2-x1)*t)/8),round((y1+(y2-y1)*t)/14)))
    for x,y in cells: d.text((x*8,y*14),'·',font=font,fill='#e6edf3',anchor='mm')
    frames.append(im)
frames[0].save('assets/geometry.gif',save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True)
