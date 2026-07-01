/* ==========================================
   NOTEBOOK ENHANCEMENTS JS
   Scroll-reveal, reading progress, active nav, easter egg
   ========================================== */

// --- SCROLL-REVEAL (Intersection Observer) ---
(function() {
    const revealElements = document.querySelectorAll('.reveal');
    if (!revealElements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => observer.observe(el));
})();

// --- READING PROGRESS BAR ---
(function() {
    const progressBar = document.getElementById('reading-progress');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = progress + '%';
    }, { passive: true });
})();

// --- ACTIVE NAV HIGHLIGHTING ON SCROLL ---
(function() {
    const sections = document.querySelectorAll('.section, .hero');
    const navLinks = document.querySelectorAll('.nav-link');
    if (!sections.length || !navLinks.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { threshold: 0.3, rootMargin: '-52px 0px -50% 0px' });

    sections.forEach(section => observer.observe(section));
})();

// --- CONSOLE EASTER EGG ---
console.log(`
%c╔═══════════════════════════════════════╗
║  Hey, you're inspecting my code!      ║
║  I like your curiosity.               ║
║                                       ║
║  → github.com/jatin-analog-git        ║
║  → Designed with gm/ID methodology    ║
╚═══════════════════════════════════════╝
`, 'color: #d4a574; font-family: monospace; font-size: 12px;');
