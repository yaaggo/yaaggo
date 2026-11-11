"""Render the original ascii-solids-rotation cube to a looping GIF (requires GCC and Pillow)."""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
source = (root / 'scripts' / 'cube.c').as_posix()
wrapper = r'''#define main original_cube_main
#include "SOURCE"
#undef main
int main(void) {
    for (int f = 0; f < 240; ++f) {
        A1 = 0;
        A2 = f * 6.28318530718f / 240;
        A3 = 0;
        render();
        fwrite(buffer, 1, BUFFER_SIZE, stdout);
    }
}'''.replace('SOURCE', source)
with tempfile.TemporaryDirectory() as temp:
    cfile, exe = Path(temp) / 'frames.c', Path(temp) / 'frames.exe'
    cfile.write_text(wrapper)
    subprocess.run(['gcc', '-O2', str(cfile), '-lm', '-o', str(exe)], check=True)
    raw = subprocess.check_output([str(exe)])
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 10)
frames = []
for n in range(240):
    chars = raw[n*160*44:(n+1)*160*44].decode('ascii')
    im = Image.new('RGB', (720, 440), '#0d1117')
    draw = ImageDraw.Draw(im)
    for y in range(44):
        row = chars[y*160:(y+1)*160][40:120]
        draw.text((120, y*10), row, font=font, fill='#e6edf3')
    frames.append(im)
frames[0].save(root / 'assets' / 'geometry.gif', save_all=True, append_images=frames[1:], duration=60, loop=0, optimize=True)


