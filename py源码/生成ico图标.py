from PIL import Image, ImageDraw

src = Image.open("logo.png").convert("RGBA")

# 1. 裁掉四周透明留白
bbox = src.getbbox()
if bbox:
    src = src.crop(bbox)

# 2. 补成正方形，避免拉伸变形
w, h = src.size
side = max(w, h)
tmp = Image.new("RGBA", (side, side), (0, 0, 0, 0))
tmp.paste(src, ((side - w) // 2, (side - h) // 2), src)

# 3. 放大到 256
tmp = tmp.resize((256, 256), Image.LANCZOS)

# 4. 垫圆角深蓝底，让图标饱满（不需要底色就把这段删掉）
bg = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
d = ImageDraw.Draw(bg)
d.rounded_rectangle([0, 0, 255, 255], radius=48, fill=(11, 37, 69, 255))
logo = tmp.resize((200, 200), Image.LANCZOS)
bg.paste(logo, (28, 28), logo)

# 5. 生成多尺寸 ico
bg.save(
    "logo.ico",
    format="ICO",
    sizes=[(128,128),(256,256)],
)
print("完成")