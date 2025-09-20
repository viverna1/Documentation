import data from './data.json' with { type: 'json' };

function createElement(options = {}) {
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

            createElement({
                parent: codeBox,
                tag: 'pre',
                html: `<code class="${boxClass === 'result-box' ? 'result-output' : 'code-block language-' + codeBlock.language}">${codeBlock.content}</code>`
            });
        });
    }

    // Разделитель
    createElement({parent: article, tag: 'hr', className: 'article-divider'});
}

const mainSection = document.querySelector('main');

data.forEach(item => {
    createElement({
        parent: mainSection, 
        tag: "section",
        className: 'content-section',
        attributes: {id: item.id},
        html: `<h2>${item.name}</h2>`
    });

    item.sections.forEach(article_data => {
        createArticle(item.id, article_data);
    })
});