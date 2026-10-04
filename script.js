document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const header = document.querySelector('.site-header');
    const toggle = document.querySelector('.nav-toggle');

    // Mobile menu
    const setMenu = (open) => {
        body.classList.toggle('menu-open', open);
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    toggle.addEventListener('click', () => setMenu(!body.classList.contains('menu-open')));
    document.querySelectorAll('.nav-menu a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') setMenu(false);
    });

    // Header border once the page is scrolled
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    // Reveal on scroll + highlight the current section in the nav
    if ('IntersectionObserver' in window) {
        const revealer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        document.querySelectorAll('.reveal').forEach((el) => revealer.observe(el));

        const links = document.querySelectorAll('.nav-link');
        const spy = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                links.forEach((l) => l.classList.toggle('active', l.getAttribute('href') === '#' + entry.target.id));
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        document.querySelectorAll('main section[id]').forEach((s) => spy.observe(s));
    } else {
        document.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
    }

    // Click-to-load YouTube embeds (keeps the page light until a video is wanted)
    document.querySelectorAll('.video[data-yt]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const iframe = document.createElement('iframe');
            iframe.src = `https://www.youtube-nocookie.com/embed/${btn.dataset.yt}?autoplay=1&start=${btn.dataset.start || 0}`;
            iframe.title = btn.getAttribute('aria-label').replace('Play ', '');
            iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
            iframe.allowFullscreen = true;
            const wrap = document.createElement('div');
            wrap.className = 'video';
            wrap.appendChild(iframe);
            btn.replaceWith(wrap);
        }, { once: true });
    });
});
