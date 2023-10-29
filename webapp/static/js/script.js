const menu = document.querySelector('.menu-toggle');
const menuIcon = document.querySelector('.bx-menu');
const closeIcon = document.querySelector('.bx-x');


setInterval(() => {
    if (document.getElementById('alert')) {
        document.getElementById('alert').style.display = 'none';
    }
}, 3000);


menuIcon.addEventListener('click', ()=> {
    if (menu.style.display == 'none') {
        showMenuToggle();
    }
    else {
        hideMenuToggle();
    }
});
// hide menu toggle when click out of menu div
document.addEventListener('click', (e) => {
    if (e.target !== menu && e.target !== menuIcon ) {
        hideMenuToggle();
    }
})
function hideMenuToggle() {
    menu.style.display = 'none';
    menuIcon.style.display = 'block';
    closeIcon.style.display = 'none';
}
function showMenuToggle() {
    menu.style.display = 'block';
    menuIcon.style.display = 'none';
    closeIcon.style.display = 'block';
}

function changePassword() {
    const divChange = document.querySelector('.change-password')
    if (divChange.style.display === 'none') {
        divChange.style.display = 'block';
    }else {
        divChange.style.display = 'none';
    }
}

function showVert(categoryName) {
    const category = document.getElementById(categoryName + '-vert');
    if (category.style.display === 'none') {
        category.style.display = 'flex';
    }
    else {
        category.style.display = 'none';
    }
}