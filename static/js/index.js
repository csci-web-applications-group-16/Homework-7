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