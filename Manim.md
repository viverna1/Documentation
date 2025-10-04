<!--
<video autoplay loop muted src="" title="Title"></video>
-->

## Начало

```python
class Anim(Scene):
    def construct(self):
        [...]
```

# Фигуры

### Виды

- `Circle()` - Круг
- `Square()` - Квадрат

> Анимация всех фигур по порядку

### Параметры фигур

```python
obj = Circle()
```

- `obj.set_fill`(Цвет, прозрачность)
- `obj.rotate`(Угол в хз в чём или PI/4)
- `obj.next_to(`    - Устанавливает позицию
  - `obj2`          - обьект, после которого будет текущий
  - `RIGHT`         - в какой стороне он будет
  - `buff=0.5)`     - буфер расстояния между фигурами
- `shift`           - смещение относительно центра
- `animate`         - устанавливается в self.play() и делает анимации обьектов

**пример:**
```python
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

```
<video autoplay loop muted src="media/manim/anim1.mp4" title="Title"></video>


```python
class TwoTransforms(Scene):
    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(Transform(a, b))
        self.play(Transform(a, c))
        self.play(FadeOut(a))

    def replacement_transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(ReplacementTransform(a, b))
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(c))

    def construct(self):
        self.transform()
        self.wait(0.5)  # wait for 0.5 seconds
        self.replacement_transform()
```
<video autoplay loop muted src="media/manim/anim2.mp4" title="Title"></video>


### Расположение

-

## Анимации

```python
self.play(<что то>)
```

> Если писать через запятую обьекты будут появляться одновременно `self.play(Анимация1, Анимация2)`

- `Create()` — Создаёт фигуру с анимацией по кругу
- `Transform(Ф1, Ф1)` — Превращение из одного обьекта в другую
- `FadeIn()` - Плавное появление
- `FadeOut()` - Плавное исчезновение
- `Rotate(obj, angle=угол)` - повернуть обьект



