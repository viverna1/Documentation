from manim import *  # type: ignore
import os
import shutil
from PIL import Image
from pathlib import Path

import subprocess
import cv2
import numpy as np

# config.background_color = "#000000"
config.media_dir = "./media"  # Явно указываем медиа директорию


class Formula(Scene):
    def construct(self):
        circle = Circle()  # создать обьект
        circle.set_fill(BLUE, opacity=0.5)  # устаноить цвет и прозрачность

        square = Square()
        square.shift(2 * LEFT) # переместить
        square.rotate(PI/4) # повернуть обьект

        circle.next_to(square, RIGHT, buff=0.5)  # позиция справа от квадрата

        self.play(Create(circle), Create(square))  # показать фигуры
        self.play(square.animate.rotate(PI/4))  # анимация поворота
        Wait(1) # пауза
        self.play(Rotate(square, angle=PI)) # другая анимация поворота

        




def crop_video(input_path, size, crop_mode='center', replace_original=False):
    """
    Обрезает видео до указанных размеров с использованием FFmpeg.
    
    Args:
        input_path (str): Путь к исходному видеофайлу
        size: Может быть:
              - tuple (width, height) для стандартной обрезки
              - tuple (left, top, right, bottom) для обрезки с указанием отступов
        crop_mode (str): Режим обрезки ('center', 'top_left', 'top_right', 'bottom_left', 'bottom_right')
                        Используется только при size=(width, height)
        replace_original (bool): Заменять ли оригинальное видео (True) или создать копию (False)
    
    Returns:
        str: Путь к обработанному видеофайлу
    """
    
    # Проверяем существование файла
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Файл {input_path} не найден")
    
    # Проверяем формат size
    if len(size) == 2:
        # Режим (width, height)
        width, height = size
        mode = 'dimensions'
    elif len(size) == 4:
        # Режим (left, top, right, bottom)
        left, top, right, bottom = size
        mode = 'margins'
    else:
        raise ValueError("size должен быть tuple (width, height) или (left, top, right, bottom)")
    
    # Получаем информацию о видео
    try:
        cmd_info = [
            'ffprobe', 
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=p=0',
            input_path
        ]
        result = subprocess.run(cmd_info, capture_output=True, text=True, check=True)
        orig_width, orig_height = map(int, result.stdout.strip().split(','))
    except Exception as e:
        raise ValueError(f"Не удалось получить информацию о видео: {e}")
    
    print(f"Исходный размер: {orig_width}x{orig_height}")
    
    # Вычисляем параметры обрезки в зависимости от режима
    if mode == 'dimensions':
        # Режим (width, height)
        print(f"Целевой размер: {width}x{height}")
        
        # Проверяем размеры
        if width > orig_width or height > orig_height:
            raise ValueError(f"Запрошенные размеры ({width}x{height}) больше исходных ({orig_width}x{orig_height})")
        
        # Определяем координаты обрезки
        if crop_mode == 'center':
            x = (orig_width - width) // 2
            y = (orig_height - height) // 2
        elif crop_mode == 'top_left':
            x = 0
            y = 0
        elif crop_mode == 'top_right':
            x = orig_width - width
            y = 0
        elif crop_mode == 'bottom_left':
            x = 0
            y = orig_height - height
        elif crop_mode == 'bottom_right':
            x = orig_width - width
            y = orig_height - height
        else:
            raise ValueError("Неверный режим обрезки. Допустимые значения: 'center', 'top_left', 'top_right', 'bottom_left', 'bottom_right'")
        
        crop_filter = f"crop={width}:{height}:{x}:{y}"
        print(f"Режим обрезки: {crop_mode}")
        print(f"Координаты обрезки: x={x}, y={y}")
        
    else:
        # Режим (left, top, right, bottom)
        print(f"Отступы: left: {left}, top: {top}, right: {right}, bottom: {bottom}")
        
        # Вычисляем ширину и высоту обрезанного видео
        width = orig_width - left - right
        height = orig_height - top - bottom
        
        # Проверяем корректность отступов
        if width <= 0 or height <= 0:
            raise ValueError(f"Некорректные отступы. Результирующий размер: {width}x{height}")
        
        if left < 0 or top < 0 or right < 0 or bottom < 0:
            raise ValueError("Отступы не могут быть отрицательными")
        
        if width > orig_width or height > orig_height:
            raise ValueError(f"Результирующий размер ({width}x{height}) больше исходного ({orig_width}x{orig_height})")
        
        crop_filter = f"crop={width}:{height}:{left}:{top}"
        print(f"Результирующий размер: {width}x{height}")
    
    # Определяем выходной путь
    if replace_original:
        output_path = input_path
        temp_path = input_path + '.temp.mp4'
    else:
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_cropped{input_path_obj.suffix}")
        temp_path = output_path
    
    # Строим команду FFmpeg
    cmd = [
        'ffmpeg',
        '-i', input_path,           # Входной файл
        '-vf', crop_filter,         # Фильтр обрезки
        '-c:a', 'copy',             # Копируем аудио без перекодирования
        '-y',                       # Перезаписывать выходной файл
        temp_path
    ]
    
    print(f"Команда: {' '.join(cmd)}")
    
    try:
        # Запускаем FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Если заменяем оригинал, перемещаем временный файл
        if replace_original:
            os.replace(temp_path, output_path)
        
        print("✅ Видео успешно обрезано!")
        print(f"📁 Результат сохранен в: {output_path}")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка FFmpeg: {e}")
        print(f"Stderr: {e.stderr}")
        # Удаляем временный файл если он создался
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None


def find_black_borders(video_path, sample_frames=10, threshold=10):
    """
    Определяет размер чёрных полей вокруг контента в видео.
    
    Args:
        video_path (str): Путь к видеофайлу
        sample_frames (int): Количество кадров для анализа
        threshold (int): Порог черного цвета (0-255)
    
    Returns:
        dict: {'left': int, 'top': int, 'right': int, 'bottom': int}
    """
    cap = cv2.VideoCapture(video_path)
    borders = []
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total_frames // sample_frames)
    
    for i in range(sample_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
        ret, frame = cap.read()
        
        if not ret:
            continue
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Находим границы контента
        left = np.argmax(gray.max(axis=0) > threshold)
        right = gray.shape[1] - np.argmax(gray.max(axis=0)[::-1] > threshold)
        top = np.argmax(gray.max(axis=1) > threshold)
        bottom = gray.shape[0] - np.argmax(gray.max(axis=1)[::-1] > threshold)
        
        borders.append((left, top, gray.shape[1] - right, gray.shape[0] - bottom))
    
    cap.release()
    
    # Усредняем результаты по всем кадрам
    avg_borders = np.mean(borders, axis=0).astype(int)
    return avg_borders.tolist()


def ctext(text, color: str = 'reset', style: str = 'reset') -> str:
    """Описание:
        Функция позволяет выводить текст определенным цветом и стилем в терминале.

    Аргументы:
        text (any): Текст, который нужно вывести с определенным цветом и стилем
        color (str): Цвет текста. Может принимать следующие значения:
            - 'black': черный
            - 'red': красный
            - 'green': зеленый
            - 'yellow': желтый
            - 'blue': синий
            - 'purple': фиолетовый
            - 'grey': серый
            - 'dark_grey': тёмно-серый
            - 'cyan': голубой
            - 'white': белый
            - 'reset': сбросить цвет на стандартный (по умолчанию)
        style (str): Стиль текста. Может принимать следующие значения:
            - 'bold': жирный
            - 'italic': курсивный
            - 'underline': подчеркнутый
            - 'strikethrough': зачёркнутый
            - 'frame': текст в рамке
            - 'reset': сбросить стиль на стандартный (по умолчанию)

    Возвращает:
        str: Строка с примененным к ней цветом и стилем.
    """
    styles = {
        'bold': '\033[1m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'strikethrough': '\033[9m',
        'frame': '\033[51m',
        'reset': '\033[0m'
    }
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'grey': '\033[37m',
        'dark_grey': '\033[90m',
        'darkgrey': '\033[90m',
        'reset': '\033[0m'
    }

    if color not in colors or style not in styles:
        return str(text)  # Вывести текст без изменений, если цвет не определён
    else:
        return f"{styles[style]}{colors[color] if color != 'reset' else ''}{str(text)}\033[0m"


def createAnim(formula_name: str, outpath: str = "math", image_mode: bool = False, 
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
    target_dir = Path(outpath)
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
        
        # Команда для рендеринга видео (без прозрачности, так как mp4 не поддерживает альфу)
        cmd = f"manim -q{quality} {file_name} Formula --format=mp4"
        os.system(cmd)
        
        # Находим последнее видео
        media_dir = Path(f"media/videos/{file_name[:-3]}")
        if media_dir.exists():
            mp4_files = list(media_dir.glob("**/*.mp4"))
            if mp4_files:
                mp4_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                last_mp4 = mp4_files[0]
                
                # Копируем в целевую директорию
                target_mp4 = target_dir / f"{formula_name}.mp4"
                shutil.copy2(last_mp4, target_mp4)
                print(f"Видео сохранено: {target_mp4}")

                # Автоматическая обрезка
                # cropped_mp4 = target_dir / f"{formula_name}_cropped.mp4"
                # crop_video(target_mp4, cropped_mp4)


def cleanup():    
    """
    Функция для очистки временных файлов, созданных Manim
    """
    # Очистка временных файлов
    cleanup_dirs = ["videos", "images", "Tex", "texts"]
    for dir_path in cleanup_dirs:
        dir_path = Path(f"media/{dir_path}")
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"Очищена директория: {dir_path}")


class Config:
    # ╔═══════════════════════╗
    # ║ Пути и имена файлов   ║
    # ╚═══════════════════════╝
    path = "media"              # Корневая папка для медиа
    out_folder = "manim"        # Папка для текущего md файла
    anim_name = "anim1"          # Имя анимации

    # ╔═══════════════════════╗
    # ║ Режимы работы         ║
    # ╚═══════════════════════╝
    video_mode = True           # Рендерить видео
    image_mode = False          # Рендерить одиночное изображение
    quality = "h"               # Качество: l - low, m - medium, h - high, p - production

    # ╔═══════════════════════╗
    # ║ Обрезка видео         ║
    # ╚═══════════════════════╝
    crop = 0                 # Включить обрезку
    offset = [0, 0, 0, 0]       # Смещение границ: left, top, right, bottom
    sample_frames = 10          # Сколько кадров анализировать для поиска границ

    # ╔═══════════════════════╗
    # ║ Отладка и очистка     ║
    # ╚═══════════════════════╝
    debug = False                # Включить режим отладки (не заменяет исходный файл)
    clean = True                # Удалять временные файлы после рендеринга



if __name__ == "__main__":
    config = Config()
    final_path = f"{config.path}/{config.out_folder}/{config.anim_name}.mp4"
    
    # 1. Рендеринг, если файл не существует
    if os.path.exists(final_path):
        print(ctext("Анимация существует", "green", "bold"))
    else:
        createAnim(config.anim_name, outpath=f"{config.path}/{config.out_folder}", 
             image_mode=config.image_mode, video_mode=config.video_mode, quality=config.quality)
    
    # 2. Обрезка видео
    if config.crop:
        # detected_borders = find_black_borders(final_path, sample_frames=config.sample_frames)
        # crop_values = [a + b for a, b in zip(config.offset, detected_borders)]
        crop_values = config.offset
        crop_video(final_path, crop_values, crop_mode="center", replace_original=not config.debug)
    
    # 3. Очистка временных файлов
    if config.clean:
        cleanup()

