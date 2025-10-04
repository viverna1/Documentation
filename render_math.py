from manim import *  # type: ignore
import os
import shutil
from PIL import Image
from pathlib import Path

# Конфигурация прозрачного фона
config.background_color = "#00000000"
config.media_dir = "./media"  # Явно указываем медиа директорию

class Formula(Scene):
    def construct(self):
        # Создаем отрезок с точками
        line = Line(start=LEFT*2, end=RIGHT*2, color=WHITE, stroke_width=8)
        
        # Создаем точки на отрезке
        point_a = Dot(point=LEFT*1, color=RED, radius=0.08)
        point_b = Dot(point=RIGHT*1, color=RED, radius=0.08)
        
        # Добавляем подписи точек
        label_a = Text("A", font_size=24, color=WHITE).next_to(point_a, DOWN, buff=0.2)
        label_b = Text("B", font_size=24, color=WHITE).next_to(point_b, DOWN, buff=0.2)
        
        # Группируем все элементы
        group = VGroup(line, point_a, point_b, label_a, label_b)
        group.move_to(ORIGIN)
        
        # Анимация появления
        self.play(Create(line))
        self.play(
            GrowFromCenter(point_a),
            GrowFromCenter(point_b),
            Write(label_a),
            Write(label_b)
        )
        self.wait(1)


def main(formula_name: str, outpath: str = "math", image_mode: bool = False, 
         video_mode: bool = False, quality: str = "l"):
    """
    Основная функция рендеринга
    
    Args:
        formula_name: название выходного файла
        outpath: путь для сохранения результатов
        image_mode: рендерить ли изображение
        video_mode: рендерить ли видео
        quality: качество рендеринга ('l' - low, 'm' - medium, 'h' - high, 'p' - production)
    """
    # Получаем имя текущего скрипта
    file_name = os.path.basename(__file__)
    
    # Создаем целевую директорию
    target_dir = Path("media") / outpath
    target_dir.mkdir(parents=True, exist_ok=True)
    
    image_mode = image_mode or not video_mode
    print(f"Режимы - Изображение: {image_mode}, Видео: {video_mode}, Качество: {quality}")

    # Рендеринг изображения
    if image_mode:
        print("Рендеринг изображения...")
        
        # Команда для рендеринга PNG с прозрачным фоном
        cmd = f"manim -q{quality} {file_name} Formula --format=png --transparent"
        os.system(cmd)
        
        # Находим последний PNG
        media_dir = Path(f"media/images/{file_name[:-3]}")
        if media_dir.exists():
            png_files = list(media_dir.glob("*.png"))
            if png_files:
                png_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                last_png = png_files[0]
                
                # Обрезка по содержимому с отступом
                img = Image.open(last_png)
                alpha = img.split()[-1]
                bbox = alpha.getbbox()
                
                if bbox:
                    left, upper, right, lower = bbox
                    # Добавляем отступ 20 пикселей
                    padding = 20
                    left = max(left - padding, 0)
                    upper = max(upper - padding, 0)
                    right = min(right + padding, img.width)
                    lower = min(lower + padding, img.height)
                    img_cropped = img.crop((left, upper, right, lower))
                    
                    # Сохраняем обрезанное изображение
                    target_path = target_dir / f"{formula_name}.png"
                    img_cropped.save(target_path)
                    print(f"Изображение сохранено: {target_path}")
    
    # Рендеринг видео
    if video_mode:
        print("Рендеринг видео...")
        
        # Команда для рендеринга видео с прозрачным фоном
        cmd = f"manim -q{quality} {file_name} Formula --format=mp4 --transparent"
        # cmd = f"manim -q{quality} {file_name} Formula --format=webm --transparent"
        os.system(cmd)
        
        # Находим последнее видео
        media_dir = Path(f"media/videos/{file_name[:-3]}")
        if media_dir.exists():
            mp4_files = list(media_dir.glob("**/*.mov"))
            if mp4_files:
                mp4_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                last_mp4 = mp4_files[0]
                
                # Копируем .mov в целевую директорию
                target_mov = target_dir / f"{formula_name}.mov"
                shutil.copy2(last_mp4, target_mov)
                print(f"Видео сохранено: {target_mov}")

                # Конвертируем в webm с альфой
                target_webm = target_dir / f"{formula_name}.webm"
                os.system(f'ffmpeg -y -i "{target_mov}" -c:v libvpx -pix_fmt yuva420p "{target_webm}"')
                print(f"Видео сконвертировано в: {target_webm}")

    
    # Очистка временных файлов
    cleanup_dirs = ["videos1", "images", "Tex", "texts"]
    for dir_path in cleanup_dirs:
        dir_path = Path(f"media/{dir_path}")
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"Очищена директория: {dir_path}")


if __name__ == "__main__":
    # Примеры использования:
    
    # Только изображение (по умолчанию)
    # main("line_segment", script_name, outpath="math")
    
    # Изображение и видео
    main("line_segment", outpath="math", video_mode=True, quality="m")
    
    # Только видео высокого качества
    # main("line_segment", script_name, outpath="math", image_mode=False, video_mode=True, quality="h")
    