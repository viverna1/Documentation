from manim import * # type: ignore
import os
from PIL import Image

config.background_color = "#00000000"

class Formula(Scene):
    def construct(self):
        # Создаем отрезок с точками
        line = Line(start=LEFT*2, end=RIGHT*2, color=WHITE, stroke_width=8)
        
        # Создаем точки на отрезке
        point_a = Dot(point=LEFT*1, color=RED, radius=0.08)
        point_b = Dot(point=RIGHT*1, color=RED, radius=0.08)
        
        
        # Группируем все элементы
        group = VGroup(line, point_a, point_b)
        group.move_to(ORIGIN)
        
        self.add(group)
        

def main(formula_name: str):
    # Рендерим PNG с прозрачным фоном
    os.system("manim -ql render_math.py Formula -s --format=png --transparent")
    
    # Находим последний PNG
    media_dir = "media/images/render_math"
    png_files = [f for f in os.listdir(media_dir) if f.endswith(".png")]
    png_files.sort(key=lambda x: os.path.getmtime(os.path.join(media_dir, x)))
    last_png = os.path.join(media_dir, png_files[-1])
    
    # Обрезка по содержимому с отступом 10 пикселей
    img = Image.open(last_png)
    # Преобразуем в альфа-канал, чтобы понять границы
    alpha = img.split()[-1]
    bbox = alpha.getbbox()  # bbox = (left, upper, right, lower)
    if bbox:
        left, upper, right, lower = bbox
        # Добавляем отступ 10 пикселей, но не выходим за пределы картинки
        left = max(left-10, 0)
        upper = max(upper-10, 0)
        right = min(right+10, img.width)
        lower = min(lower+10, img.height)
        img_cropped = img.crop((left, upper, right, lower))
        img_cropped.save(last_png)

    # Перемещяем PNG в нужную папку
    target_dir = "media/math"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    target_path = os.path.join(target_dir, formula_name + ".png")
    os.replace(last_png, target_path)
    
    # Удаляем папку videos и images
    videos_path = "media/videos"
    if os.path.exists(videos_path):
        import shutil
        shutil.rmtree(videos_path)
    images_path = "media/images"
    if os.path.exists(images_path):
        import shutil
        shutil.rmtree(images_path)
    images_path = "media/Tex"
    if os.path.exists(images_path):
        import shutil
        shutil.rmtree(images_path)


if __name__ == "__main__":
    main("test2")
