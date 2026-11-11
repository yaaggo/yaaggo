from PIL import Image, ImageDraw, ImageFont
import math

WIDTH, HEIGHT = 720, 270
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
frames = []
edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
base = [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
for frame in range(72):
    image = Image.new('RGB', (WIDTH, HEIGHT), '#0d1117')
    draw = ImageDraw.Draw(image)
    angle = frame * 2 * math.pi / 72
    cells = {}
    def project(point):
        x, y, z = point
        x, z = x*math.cos(angle)+z*math.sin(angle), -x*math.sin(angle)+z*math.cos(angle)
        y, z = y*math.cos(.42)-z*math.sin(.42), y*math.sin(.42)+z*math.cos(.42)
        scale = 155 / (4.2-z)
        return WIDTH/2+x*scale, HEIGHT/2+y*scale
    def line(p, q, glyph, color):
        x1,y1 = project(p); x2,y2 = project(q)
        for i in range(101):
            t=i/100
            cell=(round((x1+(x2-x1)*t)/8),round((y1+(y2-y1)*t)/14))
            cells[cell]=(glyph,color)
    for size, glyph, color in [(1.5, '·', '#e6edf3'), (.85, ':', '#8b949e')]:
        points=[tuple(v*size for v in p) for p in base]
        for a,b in edges: line(points[a],points[b],glyph,color)
    for p in base:
        line(tuple(v*.85 for v in p),tuple(v*1.5 for v in p),'.','#6e7681')
    for (x,y),(glyph,color) in cells.items():
        draw.text((x*8,y*14),glyph,font=font,fill=color,anchor='mm')
    frames.append(image)
frames[0].save('assets/geometry.gif', save_all=True, append_images=frames[1:], duration=70, loop=0, optimize=True)
