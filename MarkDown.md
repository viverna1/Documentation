# Markdown

## Заголовки разного уровня

### Заголовок
###### Заголовок



## Форматирование текста

*курсив*

**жирный**

~~Зачёркнутый~~



## Списки

### Нумерованный список:
1. one
2. two
   1. three

### Маркированный список:
- li
- li
  - li

* dot
* dot
+ plus

### Список задач:
- [ ] Невыполненная задача
- [X] Выполненная задача
- [ ] Ещё одна задача



## Другие элементы

[ссылка](https://google.com)

[ссылка2](https://example.com "Всплывающая подсказка")

![Картинка](/media/cat.jpg)

> Это пример цитаты. Она выделяется отступом и специальным форматированием.

```python
print("пример кода")
def hello():
    return "Hello, World!"
```



## Таблица

| Заголовок 1 | Заголовок 2 |
|-------------|-------------|
| ячейка 1    | ячейка 3    |
| ячейка 2    | ячейка 4    |

| Столбец 1 | Столбец 2 | Столбец 3 |
|:----------|:----------:|----------:|
| выравнивание влево | по центру | вправо |
| содержимое | данные | числа |


## Специальные элементы

<u style="color: lime">HTML-разметка в Markdown</u>





# Математика в Markdown

Markdown поддерживает LaTeX-подобный синтаксис для формул.

### Встроенные формулы
Используй `$...$` для формул внутри текста:  
Пример: `$a^2 + b^2 = c^2$` → $a^2 + b^2 = c^2$

### Блоки формул
Используй `$$...$$` для отдельного блока формулы:

$$
\int_0^1 x^2 \, dx
$$

### Символы
- Греческие буквы: $\alpha$, $\beta$, $\gamma$, $\pi$, $\phi$, $\mu$, $\theta$
- Прописные греческие: $\Gamma$, $\Pi$, $\Phi$, $\Delta$, $\Sigma$, $\Omega$
- Другие: $\infty$, $\partial$, $\nabla$, $\approx$, $\neq$, $\leq$, $\geq$

### Арифметика и операции
- Основные: `+`, `-`, `*`, `/`, `^`
- Дроби: `\frac{a}{b}` → $\frac{a}{b}$
- Корни: `\sqrt{x}`, `\sqrt[n]{x}` → $\sqrt{x}$, $\sqrt[3]{8}$
- Надстрочные и подстрочные: $x^2$, $x_i$
- Скобки: `\left(...\right)`, `\left[...\right]`, `\left\{...\right\}` → $\left( x + y \right)$

### Суммы, интегралы и пределы
- Суммы: `\sum_{i=1}^{n} i^2`: 
  $$\sum_{i=1}^{n} i^2$$
- Интегралы: `\int_0^1 x^2 dx`:
  $$\int_0^1 x^2 dx$$
- Пределы: `\lim_{x \to \infty} f(x)`:
   $$\lim_{x \to \infty} f(x)$$

### Функции
- Тригонометрические: `\sin`, `\cos`, `\tan`, `\cot`, `\sec`, `\csc`
- Обратные: `\arcsin`, `\arccos`, `\arctan`
- Экспоненты и логарифмы: `\exp(x)`, `\ln(x)`, `\log_{2}(x)` → $\exp(x)$, $\ln(x)$, $\log_{2}(x)$

### Матрицы
```latex
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
```

$$
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
$$

### Системы уравнений

```latex
\begin{cases}
x + 2y = 7 \\
3x - y = 1
\end{cases}
```
$$
\begin{cases}
x + 2y = 7 \\
3x - y = 1
\end{cases}
$$

### Прочее

* Абсолютное значение: `\lvert x \rvert` → $\lvert x \rvert$
* Нормы: `\lVert x \rVert` → $\lVert x \rVert$
* Степени и индексы в сложных выражениях: `$x_i^2$` → $x_i^2$
* Уравнения с несколькими строками: `\begin{align} ... \end{align}`

### Стрелки и отношения

- `\rightarrow`, `\Rightarrow`, `\leftrightarrow`, `\Leftrightarrow` → $\rightarrow, \Rightarrow, \leftrightarrow, \Leftrightarrow$
- `\mapsto`, `\to`, `\gets` → $\mapsto, \to, \gets$
- `\in`, `\notin`, `\subset`, `\subseteq`, `\supset`, `\supseteq` → $\in, \notin, \subset, \subseteq, \supset, \supseteq$
- `\forall`, `\exists`, `\nexists` → $\forall, \exists, \nexists$

### Диакритические знаки
- `\hat{a}`, `\bar{b}`, `\vec{c}`, `\dot{d}`, `\ddot{e}` → $\hat{a}, \bar{b}, \vec{c}, \dot{d}, \ddot{e}$
- `\acute{f}`, `\grave{g}`, `\check{h}`, `\breve{i}` → $\acute{f}, \grave{g}, \check{h}, \breve{i}$

$$\frac{dy}{dx}, \frac{\partial f}{\partial x}, \nabla f$$

$$\bar{x}, \hat{p}, \tilde{\mu}, \overline{X_n}$$
