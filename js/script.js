/* ==========================================
   JATIN - Professional Portfolio Website
   JavaScript Functionality
   ========================================== */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    initNavigation();
    initTypingEffect();
    initScrollAnimations();
    initMagneticLinks();
    initExperienceTabs();
    initProjectFilters();
    initSkillBars();
    initContactForm();
    initBackToTop();
    initReadingProgress();
    initCopyButtons();
    initStarCanvas();
    initDarkModeToggle();
});

/* ==========================================
   NAVIGATION
   ========================================== */
function initNavigation() {
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Scroll effect for navbar
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Update active nav link based on scroll position
        updateActiveNavLink();
    });

    // Mobile menu toggle
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Smooth scroll for nav links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Update active nav link based on scroll position
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;

        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

/* ==========================================
   TYPING EFFECT
   ========================================== */
function initTypingEffect() {
    const typedTextElement = document.getElementById('typed-text');

    // CHANGE: You can add or remove titles from this list.
    // Make sure each title is inside quotes '' and ends with a comma ,
    const titles = [
        'Senior Analog Design Engineer',
        'Data Converter Architect',
        'OTA Sizing Specialist',
        'Silicon Validation Engineer'
    ];

    let titleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function type() {
        const currentTitle = titles[titleIndex];

        if (isDeleting) {
            typedTextElement.textContent = currentTitle.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50;
        } else {
            typedTextElement.textContent = currentTitle.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100;
        }

        if (!isDeleting && charIndex === currentTitle.length) {
            // Pause at end of word
            typingSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            titleIndex = (titleIndex + 1) % titles.length;
            typingSpeed = 500;
        }

        setTimeout(type, typingSpeed);
    }

    // Start typing effect
    setTimeout(type, 1000);
}

/* ==========================================
   SCROLL REVEAL (Intersection Observer)
   ========================================== */
function initScrollAnimations() {
    const revealElements = document.querySelectorAll('.section-header, .about-content, .timeline-item, .project-card, .skills-category, .blog-card, .contact-content');

    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');

                // If it's a grid, stagger its children
                if (entry.target.classList.contains('stagger-reveal')) {
                    staggerChildren(entry.target);
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    revealElements.forEach(element => {
        element.classList.add('reveal');
        revealObserver.observe(element);
    });
}

function staggerChildren(container) {
    const children = container.querySelectorAll('.project-card, .blog-card, .skill-item');
    children.forEach((child, index) => {
        child.style.transitionDelay = `${(index + 1) * 0.1}s`;
    });
}

/* ==========================================
   MAGNETIC INTERACTION
   ========================================== */
function initMagneticLinks() {
    const magneticElements = document.querySelectorAll('.btn-primary, .btn-secondary, .project-link, .blog-link, .project-action');

    magneticElements.forEach(el => {
        el.addEventListener('mousemove', function (e) {
            const pos = el.getBoundingClientRect();
            const x = e.pageX - pos.left - window.scrollX;
            const y = e.pageY - pos.top - window.scrollY;

            const centerX = pos.width / 2;
            const centerY = pos.height / 2;

            const deltaX = x - centerX;
            const deltaY = y - centerY;

            // Subtle pull effect
            el.style.transform = `translate(${deltaX * 0.2}px, ${deltaY * 0.2}px)`;
        });

        el.addEventListener('mouseleave', function () {
            el.style.transform = 'translate(0, 0)';
        });
    });
}

/* ==========================================
   EXPERIENCE TABS
   ========================================== */
function initExperienceTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const timelines = document.querySelectorAll('.timeline');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            // Update active button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Show corresponding timeline
            timelines.forEach(timeline => {
                timeline.classList.remove('active');
                if (timeline.id === targetTab) {
                    timeline.classList.add('active');
                    // CSS animations in styles-cyberpunk.css handle the node reveal
                }
            });
        });
    });
}

/* ==========================================
   PROJECT FILTERS
   ========================================== */
function initProjectFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');

            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Filter projects
            projectCards.forEach(card => {
                const category = card.getAttribute('data-category');

                if (filter === 'all' || category === filter) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
}

/* ==========================================
   SKILL BARS ANIMATION
   ========================================== */
function initSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');

    const animateSkillBars = () => {
        skillBars.forEach(bar => {
            const barTop = bar.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (barTop < windowHeight - 50) {
                const progress = bar.getAttribute('data-progress');
                bar.style.width = progress + '%';
            }
        });
    };

    window.addEventListener('scroll', animateSkillBars);
    animateSkillBars(); // Initial check
}

/* ==========================================
   CONTACT FORM
   ========================================== */
function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Show success message (replace with actual form submission logic)
        const button = form.querySelector('button[type="submit"]');
        const originalContent = button.innerHTML;

        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        button.disabled = true;

        // Simulate form submission
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-check"></i> Message Sent!';
            button.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';

            // Reset form
            form.reset();

            // Reset button after 3 seconds
            setTimeout(() => {
                button.innerHTML = originalContent;
                button.style.background = '';
                button.disabled = false;
            }, 3000);
        }, 1500);

        // Log form data (for testing)
        console.log('Form submitted:', data);

        // TODO: Add actual form submission logic
        // You can use services like:
        // - Formspree (https://formspree.io)
        // - Netlify Forms
        // - EmailJS (https://emailjs.com)
    });
}

/* ==========================================
   BACK TO TOP BUTTON
   ========================================== */
function initBackToTop() {
    const backToTopButton = document.getElementById('back-to-top');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/* ==========================================
   PARTICLE BACKGROUND
   ========================================== */
/* ==========================================
   SMOOTH SCROLL HELPER
   ========================================== */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            const offsetTop = targetElement.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

/* ==========================================
   READING PROGRESS BAR
   ========================================== */
function initReadingProgress() {
    const progress = document.getElementById('reading-progress');
    if (!progress) return;

    const updateProgress = () => {
        const winScroll = window.pageYOffset || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;

        if (height > 0) {
            progress.style.width = Math.min(Math.max(scrolled, 0), 100) + "%";
        }
    };

    window.addEventListener('scroll', updateProgress);
    window.addEventListener('resize', updateProgress);
    updateProgress(); // Initial check
}

/* ==========================================
   COPY CODE TO CLIPBOARD
   ========================================== */
async function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // Fallback for file:// or non-secure contexts
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-999px";
        textArea.style.top = "0";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            const successful = document.execCommand('copy');
            textArea.remove();
            return successful ? Promise.resolve() : Promise.reject();
        } catch (err) {
            textArea.remove();
            return Promise.reject(err);
        }
    }
}

function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');

    copyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const container = btn.closest('.code-container');
            const code = container.querySelector('code').innerText;

            copyToClipboard(code).then(() => {
                const icon = btn.querySelector('i');
                const originalClass = icon.className;
                icon.className = 'fas fa-check';
                btn.classList.add('copied');

                setTimeout(() => {
                    icon.className = originalClass;
                    btn.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Copy failed:', err);
            });
        });
    });
}

// Reading progress and copy buttons functions are above.

/* ==========================================
   STAR CANVAS OVERLAY (Hero Section)
   Subtle floating nodes with faint lines
   ========================================== */
function initStarCanvas() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let animationId;
    let nodes = [];
    const NODE_COUNT = 45;
    const CONNECT_DIST = 120;

    function resize() {
        const hero = canvas.parentElement.parentElement;
        canvas.width = hero.offsetWidth;
        canvas.height = hero.offsetHeight;
    }

    function createNodes() {
        nodes = [];
        for (let i = 0; i < NODE_COUNT; i++) {
            nodes.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
                r: Math.random() * 1.8 + 0.8,
                opacity: Math.random() * 0.4 + 0.15
            });
        }
    }

    function getColors() {
        const isDark = document.body.classList.contains('dark-theme');
        return {
            node: isDark ? 'rgba(184, 150, 90,' : 'rgba(181, 74, 43,',
            line: isDark ? 'rgba(184, 150, 90,' : 'rgba(205, 197, 174,'
        };
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const colors = getColors();

        // Draw connecting lines
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < CONNECT_DIST) {
                    const alpha = (1 - dist / CONNECT_DIST) * 0.12;
                    ctx.beginPath();
                    ctx.strokeStyle = colors.line + alpha + ')';
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);
                    ctx.stroke();
                }
            }
        }

        // Draw nodes
        for (const n of nodes) {
            ctx.beginPath();
            ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
            ctx.fillStyle = colors.node + n.opacity + ')';
            ctx.fill();
        }
    }

    function update() {
        for (const n of nodes) {
            n.x += n.vx;
            n.y += n.vy;
            if (n.x < 0 || n.x > canvas.width) n.vx *= -1;
            if (n.y < 0 || n.y > canvas.height) n.vy *= -1;
        }
    }

    function loop() {
        update();
        draw();
        animationId = requestAnimationFrame(loop);
    }

    // Only animate when hero is in viewport
    const heroSection = document.getElementById('home');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (!animationId) loop();
            } else {
                cancelAnimationFrame(animationId);
                animationId = null;
            }
        });
    }, { threshold: 0.05 });

    resize();
    createNodes();
    observer.observe(heroSection);

    window.addEventListener('resize', () => {
        resize();
        createNodes();
    });
}

/* ==========================================
   DARK MODE TOGGLE
   ========================================== */
function initDarkModeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    const STORAGE_KEY = 'jatin-theme-pref';
    const moonIcon = '<i class="fas fa-moon"></i>';
    const sunIcon = '<i class="fas fa-sun"></i>';

    // Apply saved preference (default to dark/no-class if not set)
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light') {
        document.body.classList.add('light-theme');
        toggleBtn.innerHTML = moonIcon;
    } else {
        document.body.classList.remove('light-theme');
        toggleBtn.innerHTML = sunIcon;
    }

    toggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        localStorage.setItem(STORAGE_KEY, isLight ? 'light' : 'dark');
        toggleBtn.innerHTML = isLight ? moonIcon : sunIcon;
    });
}
