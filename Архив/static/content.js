import data from '/docs/data.json' with { type: 'json' };

export function createElement(options = {}) {
    const {
        parent = null,
        tag = 'div',
        className = '',
        content = '',
        attributes = {},
        html = ''
    } = options;
    
    const element = document.createElement(tag);
    
    if (className) element.className = className;
    if (content) element.textContent = content;
    if (html) element.innerHTML = html;
    
    // Добавляем атрибуты
    for (const [key, value] of Object.entries(attributes)) {
        element.setAttribute(key, value);
    }
    
    if (parent && parent.appendChild) {
        parent.appendChild(element);
    }
    
    return element;
}

function createArticle(parent_id, article_data) {
    // Находим родительский section по id
    const parentSection = document.getElementById(parent_id);
    if (!parentSection) return;

    // Создаём article
    const article = createElement({
        parent: parentSection,
        tag: 'article',
        className: 'example-card',
        attributes: { id: article_data.id }
    });

    // Заголовок статьи
    createElement({
        parent: article,
        tag: 'h3',
        className: 'example-title',
        content: article_data.title
    });

    // Описание
    const contentDiv = createElement({
        parent: article,
        tag: 'div',
        className: 'example-content'
    });

    createElement({
        parent: contentDiv,
        tag: 'p',
        className: 'example-description',
        content: article_data.explanation
    });

    // Параметры (если есть)
    if (article_data.parameters && article_data.parameters.length > 0) {
        const attrDiv = createElement({
            parent: contentDiv,
            tag: 'div',
            className: 'attributes-info'
        });

        createElement({
            parent: attrDiv,
            tag: 'h4',
            content: article_data.parameters_title || 'Параметры:'
        });

        const ul = createElement({
            parent: attrDiv,
            tag: 'ul'
        });

        article_data.parameters.forEach(param => {
            createElement({
                parent: ul,
                tag: 'li',
                html: `<code>${param.name}</code>${param.description ? ' - ' + param.description : ''}`
            });
        });
    }

    // Блок с примерами кода
    if (article_data.code && article_data.code.length > 0) {
        const demoDiv = createElement({
            parent: article,
            tag: 'div',
            className: 'code-demo'
        });

        article_data.code.forEach(codeBlock => {
            const boxClass = codeBlock.language === 'output' ? 'result-box' : 'code-box';
            const label = codeBlock.language.toUpperCase();

            const codeBox = createElement({
                parent: demoDiv,
                tag: 'div',
                className: boxClass
            });

            createElement({
                parent: codeBox,
                tag: 'span',
                className: 'code-label',
                content: label === 'OUTPUT' ? 'Output' : label
            });
            
            const codeClass = boxClass === 'result-box' 
                ? 'result-output' 
                : `code-block language-${codeBlock.language}`;

            const codeTag = createElement({
                parent: codeBox,
                tag: 'code',
                className: codeClass,
            });

            const isOutput = codeBlock.language.toUpperCase() === "OUTPUT";

            createElement({
                parent: codeTag,
                tag: 'pre',
                [isOutput ? 'html' : 'content']: codeBlock.content
            });
            
        });
    }

    // Разделитель
    createElement({parent: article, tag: 'hr', className: 'article-divider'});
}

export function createSideBar(parent) {
    data.forEach(section => {
        // Создаём аккордеон
        const accordion = createElement({
            parent: parent,
            tag: 'div',
            className: 'accordion'
        });

        // Кнопка аккордеона
        const header = createElement({
            parent: accordion,
            tag: 'button',
            className: 'accordion-header',
            attributes: { 'aria-expanded': 'false' }
        });

        createElement({
            parent: header,
            tag: 'span',
            className: 'accordion-arrow',
            content: '▶'
        });

        createElement({
            parent: header,
            tag: 'span',
            className: 'accordion-title',
            content: section.name
        });

        // Контент аккордеона
        const content = createElement({
            parent: accordion,
            tag: 'div',
            className: 'accordion-content',
            attributes: { hidden: true }
        });

        // Ссылки на разделы
        section.sections.forEach(article => {
            createElement({
                parent: content,
                tag: 'a',
                className: 'nav-link',
                attributes: { href: `#${article.id}` },
                content: article.title
            });
        });
    });
}

function createMain(parent) {
    data.forEach(item => {
    // создание секции
    createElement({
        parent: parent, 
        tag: "section",
        className: 'content-section',
        attributes: {id: item.id},
        html: `<h2>${item.name}</h2>`
    });
                

    // создание разделов
    item.sections.forEach(article_data => {
        createArticle(item.id, article_data);
    })
});
    
}

const mainSection = document.querySelector('main');
const sideBar = document.getElementById('sidebar-nav');


createSideBar(sideBar);
// Добавляем обработчик только один раз после генерации
document.querySelectorAll('.accordion-header').forEach(button => {
    button.addEventListener('click', () => {
        const expanded = button.getAttribute('aria-expanded') === 'true';
        const content = button.nextElementSibling;
        
        button.setAttribute('aria-expanded', !expanded);
        content.hidden = expanded;
        button.querySelector('.accordion-arrow').textContent = expanded ? '▶' : '▼';
    });
});

createMain(mainSection);

