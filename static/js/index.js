const PAGES = {
    'UPLOAD': {
        'url': 'fragments/upload.htm'
    },
    'VERIFY': {
        'url': 'fragments/verify.htm'
    },
    'CONFIGURE': {
        'url': 'fragments/configure.htm'
    },
    'RUN TESTS': {
        'url': 'fragments/tests.htm'
    },
    'REVIEW': {
        'url': 'fragments/review.htm'
    },
};

let currentPageIndex = 0;

function renderBreadcrumbs() {
    let output = "<ol class='breadcrumb'>";
    let strings = Object.keys(PAGES);

    for (let i = 0; i < strings.length; i++) {
        if (i === currentPageIndex) {
            output += `<li class='breadcrumb-item active' aria-current='page'>${strings[i]}</li>`;
        } else {
            output += `<li class='breadcrumb-item'>${strings[i]}</li>`;
        }
    }

    output += '</ol>';

    $('#breadcrumbs').html(output);
}

function loadPage() {
    const key = Object.keys(PAGES)[currentPageIndex];
    $('#page-content').load(PAGES[key].url);
}

function previousPage() {
    currentPageIndex--;
    if (currentPageIndex < 0) currentPageIndex = 0;

    refresh();
}

function nextPage() {
    currentPageIndex++;
    const length = Object.keys(PAGES).length;
    if (currentPageIndex >= length - 1) currentPageIndex = length - 1;

    refresh();
}

function refresh() {
    renderBreadcrumbs();
    loadPage();
}

function setCookie(name, val) {
    document.cookie = `${name}=${val}`;
}

function deleteCookie(name) {
    setCookie(name, '', -1);
}

function getCookie(name) {
    const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}

window.onload = function () {
    refresh();
};