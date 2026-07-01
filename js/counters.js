/**
 * counters.js
 * Animates stat numbers in the About section counting up from 0
 * when they first scroll into view.
 *
 * Usage: add data-count="N" to any element whose text should animate.
 * The element's textContent is replaced with the animated number +
 * whatever suffix string is in data-suffix (default "").
 *
 * Example already in HTML:
 *   <span data-count="3" data-suffix="+ Years Working">3+ Years Working</span>
 */

(function () {
    const DURATION = 1400;  // ms for the count-up animation
    const EASING   = t => 1 - Math.pow(1 - t, 3);  // ease-out cubic

    function animateCounter(el) {
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const start  = performance.now();

        function step(now) {
            const elapsed  = now - start;
            const progress = Math.min(elapsed / DURATION, 1);
            const value    = Math.round(EASING(progress) * target);
            el.textContent = value + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }

        requestAnimationFrame(step);
    }

    function init() {
        const counters = document.querySelectorAll('[data-count]');
        if (!counters.length) return;

        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);  // run once
                    }
                });
            },
            { threshold: 0.6 }
        );

        counters.forEach(el => observer.observe(el));
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
