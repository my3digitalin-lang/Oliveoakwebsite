from PIL import Image, ImageStat

print('Sharpness check — first 20 frames of Laptop source:')
results = []
for i in range(1, 21):
    path = f'Laptop/ezgif-frame-{i:03d}.png'
    with Image.open(path) as img:
        gray = img.convert('L').resize((192, 108))
        stat = ImageStat.Stat(gray)
        variance = stat.var[0]
        status = 'BLURRY' if variance < 200 else 'OK'
        results.append((i, variance, status))
        print(f'  Frame {i:03d}: var={variance:.0f}  [{status}]')

blurry = [r for r in results if r[2] == 'BLURRY']
print(f'\nBlurry frames: {[r[0] for r in blurry]}')
print(f'First sharp frame: {next((r[0] for r in results if r[2] == "OK"), "None")}')
