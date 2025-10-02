import json
import os
from datetime import datetime
import shutil
from typing import Callable, Optional, Tuple, Any


class JsonHandler:
    def __init__(self, path: str):
        self.path = path
        
        self.data: dict[str, Any] = dict()

        self.loadJson()

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=4)

    def __getitem__(self, key: str):
        return self.data[key]
 
    def loadJson(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def pushJson(self):
        # Создаем папку для бэкапов, если её нет
        backup_dir = os.path.join(os.path.dirname(self.path), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        # Создаем имя файла бэкапа с датой/временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{timestamp}.json"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Создаем бэкап текущего файла, если он существует
        if os.path.exists(self.path):
            shutil.copy2(self.path, backup_path)
            print(f"Создан бэкап: {backup_path}")

        # Сохраняем изменения в файл
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        self.loadJson()

    # Секции
    def createSection(self, section_name: str, section_id: str):
        if section_id not in self.data:
            self.data[section_id] = {
                "name": section_name,
                "id": section_id,
                "content": {}
            }
            self.pushJson()
        else:
            raise ValueError(f"Секция с идентификатором {section_id} уже существует.")

    def editSection(self, section_id_to_edit: str, new_section_name: str, new_section_id: str):
        if section_id_to_edit in self.data:
            # Сохраняем данные старой секции
            section_data = self.data[section_id_to_edit]
            
            # Обновляем данные
            section_data["name"] = new_section_name
            section_data["id"] = new_section_id
            
            # Если ID изменился, перемещаем в новый ключ
            if section_id_to_edit != new_section_id:
                self.data[new_section_id] = section_data
                del self.data[section_id_to_edit]
            
            self.pushJson()
        else:
            raise ValueError(f"Секция с идентификатором {section_id_to_edit} не найдена.")
        
    def deleteSection(self, section_id_to_delete: str):
        if section_id_to_delete in self.data:
            del self.data[section_id_to_delete]
            self.pushJson()
        else:
            raise ValueError(f"Секция с идентификатором {section_id_to_delete} не найдена.")
    
    # Посты
    def createPost(self, section_id: str, title: str, post_id: str, explanation: str):
        if title and post_id and explanation:
            if section_id in self.data:
                if not isinstance(self.data[section_id].get("content"), dict):
                    self.data[section_id]["content"] = {}
                self.data[section_id]["content"][post_id] = {
                    "title": title,
                    "id": post_id,
                    "explanation": explanation,
                    "parameters": [],
                    "code": []
                }
                # if not isinstance(self.data[section_id].get("content"), dict)
                self.pushJson()
            else:
                raise ValueError(f"Секция с идентификатором {section_id} не найдена.")
        else:
            raise ValueError("Заполните заголовок и содержание поста.")

    def showPost(self, section_id: str, post_id: str):
        """
        Форматирует JSON структуру в красивую рамку
        """
        post_data= self.data[section_id]["content"][post_id]

        # Верхняя граница рамки
        top_border = "╔" + "═" * 78 + "╗"
        bottom_border = "╚" + "═" * 78 + "╝"
        
        lines: list[str] = []
        lines.append(top_border)
        
        # Заголовок и id
        title = post_data.get('title', 'Без названия')
        id_text = f"ID: {post_data.get('id', 'N/A')}"
        lines.append(format_two_columns(f"║ {title}", f"{id_text} ║", total_width=80, padding=0))
        lines.append("║" + "═" * 78 + "║")
        
        # Описание
        explanation = post_data.get('explanation', '')
        if explanation:
            # Разбиваем длинное описание на строки
            words = explanation.split()
            current_line = ""
            for word in words:
                if len(current_line + " " + word) <= 76:
                    current_line += (" " + word) if current_line else word
                else:
                    lines.append(f"║ {current_line:<76} ║")
                    current_line = word
            if current_line:
                lines.append(f"║ {current_line:<76} ║")
            lines.append("║" + " " * 78 + "║")
        
        # Атрибуты
        parameters_title = post_data.get('parameters_title', 'Атрибуты:')
        lines.append(f"║ {parameters_title:<76} ║")
        
        parameters = post_data.get('parameters', [])
        for param in parameters:
            name = param.get('name', '')
            description = param.get('description', '')
            param_line = f"  • {name}: {description}"
            
            # Разбиваем длинные строки параметров
            if len(param_line) > 76:
                words = param_line.split()
                current_line = ""
                for i, word in enumerate(words):
                    if i == 0:
                        current_line = word
                    elif len(current_line + " " + word) <= 76:
                        current_line += " " + word
                    else:
                        lines.append(f"║ {current_line:<76} ║")
                        current_line = "    " + word
                lines.append(f"║ {current_line:<76} ║")
            else:
                lines.append(f"║ {param_line:<76} ║")
        
        if parameters:
            lines.append("║" + " " * 78 + "║")
        
        # Код
        code_blocks = post_data.get('code', [])
        for i, code_block in enumerate(code_blocks):
            language = code_block.get('language', '')
            content = code_block.get('content', '')
            
            # Содержание кода
            code_lines = content.split('\n')
            
            # Первая строка кода
            lines.append("║" + "─" * 78 + "║")
            lines.append(format_two_columns(f"║ {code_lines[0]}", f"{language} ║", total_width=80, padding=0))

            for code_line in code_lines[1:]:
                lines.append(f"║ {code_line:<76} ║")
            
            if i < len(code_blocks) - 1:
                lines.append("║" + " " * 78 + "║")
        
        lines.append(bottom_border)
        
        return '\n'.join(lines)

    def editPost(self, section_id: str, post_id: str, new_title: str, new_id: str, new_explanation: str):
        if post_id in self.data[section_id]["content"]:
            post_data = self.data[section_id]["content"][post_id]
            
            post_data["title"] = new_title
            post_data["id"] = new_id
            post_data["explanation"] = new_explanation

            # Если ID изменился, перемещаем в новый ключ
            if post_id != new_id:
                self.data[section_id]["content"][new_id] = post_data
                del self.data[section_id]["content"][post_id]
            
            self.pushJson()
        else:
            raise ValueError(f"Пост с идентификатором {post_id} не найден в секции с идентификатором {section_id}.") 

    def deletePost(self, section_id: str, post_id: str):
        if post_id in self.data[section_id]["content"]:
            del self.data[section_id]["content"][post_id]
            self.pushJson()
        else:
            raise ValueError(f"Пост с идентификатором {post_id} не найден в секции с идентификатором {section_id}.")

    # Параметры
    def createParameter(self, section_id: str, post_id: str, name: str, description: str):
        if post_id in self.data[section_id]["content"]:
            post_data = self.data[section_id]["content"][post_id]
            
            if not isinstance(post_data.get("parameters"), list):
                post_data["parameters"] = []
            
            post_data["parameters"].append({
                "name": name,
                "description": description,
            })
            
            self.pushJson()
        else:
            raise ValueError(f"Пост с идентификатором {post_id} не найден в секции с идентификатором {section_id}.")
        
    def deleteParameter(self, section_id: str, post_id: str, parameter_index: int):
        if post_id in self.data[section_id]["content"]:
            post_data = self.data[section_id]["content"][post_id]
            
            if isinstance(post_data.get("parameters"), list) and parameter_index < len(post_data["parameters"]):
                del post_data["parameters"][parameter_index]
                self.pushJson()
            else:
                raise IndexError(f"Индекс параметра {parameter_index} не валиден для поста с идентификатором {post_id}.")
        else:
            raise ValueError(f"Пост с идентификатором {post_id} не найден в секции с идентификатором {section_id}.")

    # Код
    def createCode(self, section_id: str, post_id: str, lang: str, code: str):
        if post_id in self.data[section_id]["content"]:
            post_data = self.data[section_id]["content"][post_id]
            
            if not isinstance(post_data.get("code"), list):
                post_data["code"] = []
            
            post_data["code"].append({
                "language": lang,
                "content": code,
            })
            
            self.pushJson()
        else:
            raise ValueError(f"Пост с идентификатором {post_id} не найден в секции с идентификатором {section_id}.")
        
    def deleteCode(self, section_id: str, post_id: str, code_index: int):
        if post_id in self.data[section_id]["content"]:
            post_data = self.data[section_id]["content"][post_id]
            
            if isinstance(post_data.get("code"), list) and code_index < len(post_data["code"]):
                del post_data["code"][code_index]
                self.pushJson()
            else:
                raise IndexError(f"Индекс параметра {code_index} не валиден для поста с идентификатором {post_id}.")
        else:
            raise ValueError(f"Пост с идентификатором {post_id} не найден в секции с идентификатором {section_id}.")


def format_two_columns(left_text: str, right_text: str, total_width: int = 78, padding: int = 4):
    """
    Форматирует два текста в одной строке с выравниванием по краям
    
    Args:
        left_text: текст слева
        right_text: текст справа  
        total_width: общая ширина строки
        padding: отступы от краев
    """
    available_width = total_width - padding * 2
    left_part = left_text.ljust(available_width - len(right_text))
    return f"{' ' * padding}{left_part}{right_text}{' ' * padding}"


def validated_input(
        prompt: str = "",
        parse_func: Callable[[str], Any] = str,
        allow_blank: bool = False,
        numbers_range: Optional[Tuple[int, int]] = None
    ) -> Optional[Any]:
    """
    Запрашивает и проверяет пользовательский ввод.

    :param prompt: (str): Сообщение-приглашение для ввода.
    :param parse_func: (Callable): Функция для преобразования и валидации ввода.
    :param allow_blank: (bool): Разрешить пустой ввод.

    :return Результат ввода, преобразованный parse_func, или None если разрешен пустой ввод.
    """
    while True:
        try:
            user_input = input(prompt).strip()

            # Обрабатываем пустой ввод
            if not user_input:
                if allow_blank:
                    return None
                print("Поле не может быть пустым.")
                continue
            elif numbers_range and not (numbers_range[0] <= int(user_input) <= numbers_range[1]):
                print(f"Значение должно быть в диапазоне от {numbers_range[0]} до {numbers_range[1]}.")
                continue

            # Пытаемся преобразовать и проверить ввод
            result = parse_func(user_input)
            return result

        except Exception as error:
            if is_builtin_function(parse_func):
                print(f"Неверный формат. Ожидается: {parse_func.__name__}. Попробуйте еще раз.")
            else:
                print(f"Произошла ошибка: {error}. Попробуйте еще раз.")


def validate_id(id_string: str) -> str:
    """
    Проверяет правильность написания идентификатора.
    
    Args:
        id_string (str): Строка для проверки
        
    Raises:
        ValueError: с описанием ошибки
    """
    if not id_string:
        raise ValueError("ID не может быть пустым")
    
    # Проверяем первый символ - должен быть буквой
    if not id_string[0].isalpha():
        raise ValueError("Первый символ ID должен быть буквой")
    
    # Проверяем все символы - только английские буквы и цифры
    if not id_string.isalnum():
        raise ValueError("ID должен содержать только английские буквы и цифры")
    
    # Дополнительная проверка, что нет не-английских символов
    if not all(char.isascii() for char in id_string):
        raise ValueError("ID должен содержать только английские буквы")
    
    return id_string


def is_builtin_function(func: Callable[[str], bool]) -> bool:
    """
    Проверяет, является ли функция встроенной в Python
    """
    if not callable(func):
        return False
    
    # Основные признаки встроенной функции
    builtin_modules = {'builtins', '__builtin__'}
    
    # Получаем модуль функции
    module_name = getattr(func, '__module__', None)
    
    # Проверяем различные признаки
    if module_name in builtin_modules:
        return True
    
    # Проверяем, находится ли функция в стандартных модулях Python
    standard_lib_modules = {
        'math', 'os', 'sys', 're', 'json', 'datetime', 'collections', 
        'itertools', 'functools', 'random', 'string'
    }
    
    if module_name in standard_lib_modules:
        return True
    
    # Проверяем специальные атрибуты
    if hasattr(func, '__self__') and hasattr(func, '__name__'):
        return False  # Это метод
    
    return False


def choose_option(options: list[str] | list[list[str]], title: str = "Выберите опцию") -> int:
    printFramed(title, options, numbers=True)
    
    res = validated_input("Опция: ", int, numbers_range=(0, len(options)), allow_blank=True)
    return -1 if not res else res


def printFramed(title: str, lines: list[str] | list[list[str]], spacing: int = 2, numbers: bool = False) -> None:
    """
    Универсальная функция для вывода в рамке
    
    Args:
        title: заголовок
        lines: список строк или список пар [название, id]
        spacing: расстояние между колонками
        numbers: добавлять нумерацию строк
    """
    # Инициализация для успокоения Pylance
    max_name_width = 0
    is_pairs = False
    content_width = 0

    # Определяем тип данных
    # print(json.dumps(lines, indent=3, ensure_ascii=False), isinstance(lines[0], list))
    if lines and isinstance(lines[0], list):
        # Вложенные списки - пары [название, id]
        is_pairs = True
        max_name_width = max(len(str(pair[0])) for pair in lines)
        max_id_width = max(len(str(pair[1])) for pair in lines)
        content_width = max_name_width + max_id_width + spacing
    else:
        # Обычный список строк
        is_pairs = False
        content_width = max(len(str(line)) for line in lines) if lines else 0
    
    # Вычисляем общую ширину рамки
    total_width = content_width + 4  # +4 для рамки
    if numbers:
        total_width += 4  # место для нумерации
    
    # Корректируем под заголовок
    if len(title) > total_width - 4:
        total_width = len(title) + 4
    
    border = "═" * (total_width - 2)
    
    print("╔" + border + "╗")
    print(f"║ {title.center(total_width - 4)} ║")
    print("║" + ("─" * (total_width - 2)) + "║")
    
    # Выводим строки
    for i, item in enumerate(lines):
        if is_pairs:
            # Обработка пар [название, id]
            name, id_val = str(item[0]), str(item[1])
            if numbers:
                line_content = f"{i+1}. {name.ljust(max_name_width)}{' ' * spacing}{id_val}"
            else:
                line_content = f"{name.ljust(max_name_width)}{' ' * spacing}{id_val}"
        else:
            # Обработка обычных строк
            if numbers:
                line_content = f"{i+1}. {str(item)}"
            else:
                line_content = str(item)
        
        print(f"║ {line_content.ljust(total_width - 4)} ║")
    
    print("╚" + border + "╝")


def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')


def max_str_len(text: str, long: int) -> str:
    return (text[:long] + "...") if len(text) > long else text


def main(path: str):
    data = JsonHandler(path)

    while True:
        clearConsole()
        section_list = [[data[key]['name'], data[key]['id']] for key in data.data.keys()]
        choosed_section = choose_option([["Добавить секцию", ""]] + section_list, "Выберите секцию:")

        if choosed_section in (-1, 0):
            break
        # Добавить секцию
        elif choosed_section == 1:
            section_name = validated_input("Введите название секции: ", allow_blank=True)
            while True:
                try:
                    section_id = validated_input("Введите id секции: ", validate_id, allow_blank=True)
                    if section_id and section_name:
                        data.createSection(section_name, section_id)
                    break
                except ValueError as e:
                    print(e)
        # Выбор секции
        else:
            section_id = section_list[choosed_section - 2][1]
            section_data = data[section_id]
            while True:
                clearConsole()
                action = choose_option(["Управление постами", "Редактировать секцию", "Удалить секцию"], section_data['name'])

                if action in (-1, 0):
                    break
                # Редактировать секцию
                elif action == 2:
                    new_section_name = validated_input("Введите новое название секции: ", str, allow_blank=True) or section_data["name"]
                    while True:
                        try:
                            new_section_id = validated_input("Введите новое id секции: ", validate_id, allow_blank=True) or section_data["id"]
                            data.editSection(section_id, new_section_name, new_section_id)
                            section_id = new_section_id
                            break
                        except ValueError as e:
                            print(e)
                    break
                # Удалить секцию
                elif action == 3:
                    clearConsole()
                    is_confirmed = choose_option(["Да", "Нет"], f"Удалить секцию {data[section_id]["name"]}?")
                    if is_confirmed == 1:
                        data.deleteSection(section_id)
                        break
                # управление постами
                else:
                    while True:
                        clearConsole()
                        post_list = [[section_data['content'][key]['title'], section_data['content'][key]['id']] for key in section_data['content'].keys()]
                        choosed_post = choose_option([["Добавить пост", ""]] + post_list, "Выберите пост:")
                        
                        if choosed_post in (-1, 0):
                            break
                        # Создание поста
                        elif choosed_post == 1:
                            post_title = validated_input("Введите заголовок поста: ", allow_blank=True)
                            post_id = validated_input("Введите id поста: ", allow_blank=True)
                            post_explanation = validated_input("Введите обьяснение поста: ", allow_blank=True)

                            if not (post_title and post_id and post_explanation):
                                continue
                            data.createPost(section_id, post_title, post_id, post_explanation)
                        # Управление постами
                        else:
                            post_id = post_list[choosed_post - 2][1]
                            while True:
                                clearConsole()
                                post_data = section_data["content"][post_id]
                                action = choose_option(["Посмотреть", "Редактировать", "Параметры", "Код", "Удалить пост"], post_data["title"])
                                
                                if action in (-1, 0):
                                    break
                                # Посмотреть пост
                                elif action == 1:
                                    clearConsole()
                                    print(data.showPost(section_id, post_id))
                                    input("Назад")
                                # Редактировать пост
                                elif action == 2:
                                    new_post_title = validated_input("Введите новый заголовок поста: ", str, allow_blank=True) or post_data['title']
                                    new_post_id = validated_input("Введите новый id поста: ", str, allow_blank=True) or post_data['id']
                                    new_post_explanation = validated_input("Введите новое обьяснение поста: ", str, allow_blank=True) or post_data['explanation']

                                    data.editPost(section_id, post_id, new_post_title, new_post_id, new_post_explanation)
                                    post_id = new_post_id
                                # Параметры поста
                                elif action == 3:
                                    while True:
                                        parameters: list[dict[str, str]] = post_data["parameters"]
                                        clearConsole()
                                        paremeter_list = [f"{param["name"]}: {max_str_len(param["description"], 30)}" for param in parameters]
                                        choosed_paremeter = choose_option(["Добавить параметр"] + paremeter_list, "Выберите параметр:")
                                        
                                        if choosed_paremeter in (-1, 0):
                                            break
                                        # Добавить параметр
                                        elif choosed_paremeter == 1:
                                            param_name = validated_input("Введите название параметра: ", allow_blank=True)
                                            param_content = validated_input("Введите контент параметра: ", allow_blank=True)
                                            if not param_name or not param_content:
                                                continue
                                            data.createParameter(section_id, post_id, param_name, param_content)
                                            if {"name": param_name, "description": param_content} not in parameters:
                                                parameters.append({"name": param_name, "description": param_content})  # Добавление в локальный список
                                        # Удалить
                                        else:
                                            clearConsole()
                                            is_confirmed = choose_option(["Да", "Нет"], f"Удалить параметр {parameters[choosed_paremeter - 2]["name"]}?")
                                            if is_confirmed == 1:
                                                data.deleteParameter(section_id, post_id, (choosed_paremeter - 2))
                                                del parameters[(choosed_paremeter - 2)]
                                # Код поста
                                elif action == 4:
                                    while True:
                                        codes: list[dict[str, str]] = post_data["code"]
                                        clearConsole()
                                        code_list = [f"{code["language"]}: {max_str_len(code["content"], 30)}" for code in codes]
                                        choosed_code = choose_option(["Добавить код"] + code_list, "Выберите код:")
                                        
                                        if choosed_code in (-1, 0):
                                            break
                                        # Добавить параметр
                                        elif choosed_code == 1:
                                            code_name = validated_input("Введите название кода: ")
                                            code_content = validated_input("Введите контент кода: ")
                                            if not code_name or not code_content:
                                                continue
                                            data.createCode(section_id, post_id, code_name, code_content)
                                            if {"language": code_name, "content": code_content} not in codes:
                                                codes.append({"language": code_name, "content": code_content})  # Добавление в локальный список
                                        # Удалить
                                        else:
                                            clearConsole()
                                            is_confirmed = choose_option(["Да", "Нет"], f"Удалить код {codes[choosed_code - 2]["language"]}?")
                                            if is_confirmed == 1:
                                                data.deleteCode(section_id, post_id, (choosed_code - 2))
                                                del codes[(choosed_code - 2)]  # Удаление из локального списка
                                # Удалить пост
                                elif action == 5:
                                    clearConsole()
                                    is_confirmed = choose_option(["Да", "Нет"], f"Удалить пост {data[section_id]['content'][post_id]['title']}?")
                                    if is_confirmed == 1:
                                        data.deletePost(section_id, post_id)
                                        section_data = data[section_id]
                                        break


if __name__ == "__main__":
    docs = os.listdir(path="docs")
    del docs[docs.index("backups")]
    choosed_file_index = choose_option(["Создать новый файл"] + docs, "Выберите файл:")
    
    if choosed_file_index == 1:  # "Создать новый файл"
        filename = input("Введите имя нового файла (без .json): ") + ".json"
        main_path = os.path.join("docs", filename)
        
        # Создаем файл только если выбран пункт "Создать новый файл"
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write('''{
    "basics": {
        "name": "Основы",
        "id": "basics",
        "content": {}
    }
}'''
                    )
    else:
        # Для существующих файлов - не перезаписываем!
        main_path = os.path.join("docs", docs[choosed_file_index - 2])
    
    main(main_path)
