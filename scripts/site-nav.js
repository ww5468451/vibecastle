// WW.WIKI 移动端导航：自动为 .navbar 注入汉堡按钮，无需修改每页 HTML 结构
document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.navbar');
    const links = nav && nav.querySelector('.nav-links');
    if (!nav || !links) return;

    const burger = document.createElement('button');
    burger.className = 'nav-burger';
    burger.type = 'button';
    burger.setAttribute('aria-label', '切换导航菜单');
    burger.setAttribute('aria-expanded', 'false');
    burger.innerHTML = '<span></span><span></span><span></span>';
    nav.appendChild(burger);

    const setOpen = (open) => {
        document.body.classList.toggle('nav-open', open);
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    };

    burger.addEventListener('click', (e) => {
        e.stopPropagation();
        setOpen(!document.body.classList.contains('nav-open'));
    });

    links.addEventListener('click', (e) => {
        if (e.target.closest('a')) setOpen(false);
    });

    document.addEventListener('click', (e) => {
        if (document.body.classList.contains('nav-open') && !nav.contains(e.target)) setOpen(false);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') setOpen(false);
    });
});
