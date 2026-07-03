r"""
=============================================================================
TEX TO WEBSITE CONVERTER  —  Notebook Theme
=============================================================================

Converts .tex files into website pages using the lab-notebook aesthetic
(warm paper background, Source Serif 4, JetBrains Mono, terracotta accent).

HOW TO USE:
-----------
1. Put your .tex file in the "tex_source" folder
2. Put any images referenced in the .tex file in the same folder
3. Double-click "convert_tex.bat" OR run from terminal:

   For a blog post:
       python tex_to_html.py blog "my_post.tex"

   For a project page:
       python tex_to_html.py project "my_project.tex"

   Or just double-click convert_tex.bat for interactive mode.

SUPPORTED CUSTOM COMMANDS:
---------------------------
  \title{...}            Page / post title
  \author{...}           Author name  (default: Jatin)
  \date{...}             Publication date
  \description{...}      Meta description for SEO
  \category{...}         Tag shown in header chip
  \readtime{...}         Estimated read time  (blog only, e.g. "8 min")
  \duration{...}         Project duration     (project only, e.g. "6 months")
  \githublink{...}       GitHub button URL    (project only)
  \paperlink{...}        Paper / PDF button URL (project only)
  \technode{...}         Process node chip    (project only, e.g. "180nm TSMC")
  \subtitle{...}         Subtitle shown below the title
  \gmidcalc              Inserts the interactive gm/ID calculator widget
  \begin{insight}...\end{insight}   Terracotta insight / callout box
  \begin{infobox}...\end{infobox}   Same as insight box

LATEX THAT IS CONVERTED:
-------------------------
  \section{}, \subsection{}, \subsubsection{}
  \textbf{}, \textit{}, \emph{}, \underline{}, \texttt{}
  $...$ inline math  →  \( ... \)
  $$...$$ display math  →  <div class="math-block">\[ ... \]</div>
  \begin{equation}, \begin{align}
  \begin{itemize}, \begin{enumerate}
  \begin{figure}...\includegraphics...\caption
  \begin{tabular}
  \begin{lstlisting}[language=Python|Matlab]   (% comments preserved inside)
  \begin{verbatim}
  \begin{quote}   →  blockquote

=============================================================================
"""

import os
import re
import sys
import shutil
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
TEX_SOURCE_DIR = os.path.join(SCRIPT_DIR, "tex_source")
PROJECTS_DIR  = os.path.join(SCRIPT_DIR, "projects")
BLOG_DIR      = os.path.join(SCRIPT_DIR, "blog")
IMAGES_DIR    = os.path.join(SCRIPT_DIR, "images")

# ---------------------------------------------------------------------------
# Notebook theme CSS  (shared by blog and project generators)
# ---------------------------------------------------------------------------
NOTEBOOK_CSS = """
        :root {
            --paper:     #f2ede2;
            --paper-2:   #ece6d7;
            --paper-3:   #e4ddca;
            --line:      #cdc5ae;
            --line-soft: #ded6c0;
            --ink:       #0f1620;
            --ink-soft:  #3a4656;
            --ink-dim:   #6a7485;
            --ink-dimmer:#8f9aab;
            --blue:      #0e2a4a;
            --accent:    #b54a2b;
            --green:     #2f6a3e;
            --amber:     #8c6b1a;
            --red:       #a8321e;
            --serif:     'Source Serif 4', Georgia, serif;
            --sans:      'Inter', system-ui, sans-serif;
            --mono:      'JetBrains Mono', ui-monospace, monospace;
        }
        * { box-sizing: border-box; }
        html, body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--sans); font-size: 15px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
        a { color: inherit; text-decoration: none; }

        /* READING PROGRESS */
        #reading-progress { position: fixed; top: 52px; left: 0; width: 0%; height: 3px; background: var(--accent); z-index: 200; transition: width .1s linear; }

        /* HEADER */
        .page-kicker { font-family: var(--mono); font-size: 11px; color: var(--accent); letter-spacing: 0.18em; font-weight: 600; margin-bottom: 14px; display: flex; align-items: center; gap: 10px; }
        .page-kicker::before { content: ''; width: 24px; height: 2px; background: var(--accent); }
        h1.page-title { font-family: var(--serif); font-size: 42px; font-weight: 600; line-height: 1.1; letter-spacing: -0.02em; margin: 0 0 16px; color: var(--ink); }
        .page-subtitle { font-family: var(--serif); font-size: 18px; color: var(--ink-soft); line-height: 1.55; margin: 0 0 20px; }
        .meta-row { display: flex; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 28px; }
        .meta-chip { font-family: var(--mono); font-size: 10.5px; padding: 4px 10px; background: var(--paper-2); border: 1px solid var(--line); color: var(--ink-soft); letter-spacing: 0.04em; font-weight: 500; }
        .meta-chip.primary { background: var(--ink); color: var(--paper); border-color: var(--ink); }
        .page-header { margin-bottom: 2.5rem; padding-bottom: 2rem; border-bottom: 2px solid var(--ink); }

        /* BODY TEXT */
        .page-content h2 { font-family: var(--serif); font-size: 24px; font-weight: 600; letter-spacing: -0.01em; margin: 2.5rem 0 1rem; padding-bottom: 10px; border-bottom: 1px solid var(--line); color: var(--ink); }
        .page-content h2:first-child { margin-top: 0; }
        .page-content h3 { font-family: var(--serif); font-size: 19px; font-weight: 600; color: var(--ink); margin: 1.75rem 0 0.6rem; }
        .page-content h4 { font-family: var(--serif); font-size: 16px; font-weight: 600; color: var(--ink); margin: 1.25rem 0 0.5rem; }
        .page-content p { color: var(--ink-soft); line-height: 1.8; margin-bottom: 1rem; font-size: 15.5px; }
        .page-content p strong { color: var(--ink); font-weight: 600; }
        .page-content p em { color: var(--blue); font-style: italic; }
        .page-content ul, .page-content ol { color: var(--ink-soft); margin: 0 0 1rem 1.4rem; }
        .page-content li { margin-bottom: 6px; line-height: 1.7; font-size: 15px; }
        .page-content li strong { color: var(--ink); }
        .page-content code { background: rgba(14,42,74,0.1); padding: 0.15rem 0.45rem; font-family: var(--mono); font-size: 0.87em; color: var(--blue); }

        /* MATH */
        .math-block { background: var(--paper-2); padding: 1.1rem 1.4rem; border-left: 3px solid var(--blue); margin: 1.1rem 0; overflow-x: auto; font-size: 1.05em; }

        /* INFO / INSIGHT BOX */
        .info-box, .insight-box { margin: 1.5rem 0; border: 1px solid var(--line); border-left: 3px solid var(--accent); background: var(--paper-2); padding: 14px 16px; }
        .info-box strong, .insight-box strong { color: var(--accent); font-weight: 700; }

        /* CODE BLOCK */
        .code-block { border: 1px solid var(--ink); margin: 1.25rem 0; background: #1a1f28; overflow: hidden; }
        .code-block-head { display: flex; justify-content: space-between; align-items: center; padding: 8px 14px; background: #0d1219; border-bottom: 1px solid #2a3140; }
        .code-lang-badge { font-family: var(--mono); font-size: 10px; font-weight: 700; letter-spacing: 0.14em; padding: 2px 8px; }
        .code-lang-badge.matlab { background: #b54a2b; color: #f2ede2; }
        .code-lang-badge.python { background: #2f6a3e; color: #f2ede2; }
        .code-lang-badge.default { background: #3a4656; color: #d5dce8; }
        .copy-btn { font-family: var(--mono); font-size: 10px; color: #a7b4c8; letter-spacing: 0.12em; padding: 4px 10px; background: transparent; border: 1px solid #3a4656; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; transition: all .15s; }
        .copy-btn:hover { color: var(--paper); border-color: #6a7485; }
        .copy-btn.copied { color: #77c487; border-color: #77c487; }
        .code-block pre { margin: 0; padding: 1.1rem 1.4rem; font-family: var(--mono); font-size: 13px; line-height: 1.7; overflow-x: auto; color: #d5dce8; white-space: pre; }
        .code-block pre code { background: none; padding: 0; color: inherit; font-size: inherit; }

        /* TABLE */
        .page-content table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; border: 1px solid var(--ink); }
        .page-content th { text-align: left; padding: 9px 14px; background: var(--ink); color: var(--paper); font-family: var(--mono); font-size: 10px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; }
        .page-content td { padding: 11px 14px; border-bottom: 1px solid var(--line-soft); color: var(--ink-soft); }
        .page-content tbody tr:nth-child(odd) { background: var(--paper-2); }
        .page-content tbody tr:hover { background: var(--paper-3); }

        /* BLOCKQUOTE */
        .page-content blockquote { border-left: 3px solid var(--accent); padding: 1rem 1rem 1rem 1.4rem; margin: 1.5rem 0; color: var(--ink-soft); font-family: var(--serif); font-style: italic; font-size: 16.5px; background: var(--paper-2); }

        /* FIGURE */
        .content-figure { margin: 1.75rem 0; text-align: center; background: var(--paper-2); padding: 1.25rem; border: 1px solid var(--line); }
        .content-figure img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
        .content-figure figcaption { color: var(--ink-dim); font-size: 0.87rem; margin-top: 0.7rem; font-family: var(--mono); letter-spacing: 0.04em; }

        /* PROJECT ACTION BUTTONS */
        .project-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 28px; }

        /* AUTHOR */
        .author-section { display: flex; align-items: flex-start; gap: 1.25rem; padding: 1.5rem; background: var(--paper-2); border: 1px solid var(--line); border-left: 3px solid var(--ink); margin-top: 3rem; }
        .author-avatar { width: 48px; height: 48px; background: var(--ink); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; color: var(--paper); flex-shrink: 0; }
        .author-info h4 { font-family: var(--mono); font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 600; color: var(--ink); margin: 0 0 6px; }
        .author-info p { color: var(--ink-soft); font-size: 0.9rem; margin: 0; line-height: 1.6; }

        /* SHARE */
        .share-section { display: flex; align-items: center; gap: 1rem; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--line); flex-wrap: wrap; }
        .share-section span { font-family: var(--mono); font-size: 11px; color: var(--ink-soft); letter-spacing: 0.1em; text-transform: uppercase; }
        .share-btns { display: flex; gap: 0.75rem; }
        .share-btn { width: 38px; height: 38px; border-radius: 50%; border: 1.5px solid var(--line); display: flex; align-items: center; justify-content: center; color: var(--ink-dim); font-size: 14px; transition: all 0.2s ease; text-decoration: none; }
        .share-btn:hover { border-color: var(--accent); color: var(--accent); transform: translateY(-2px); }

        /* gm/ID calculator retheme */
        #gmid-calc-root { margin: 1.5rem 0; }
        #gmid-calc-root .gmid-calculator,
        #gmid-calc-root [class*="calculator"] { background: var(--paper-2) !important; border: 1px solid var(--line) !important; border-radius: 0 !important; color: var(--ink) !important; }
        #gmid-calc-root input[type=range] { accent-color: var(--accent); }
        #gmid-calc-root label, #gmid-calc-root p, #gmid-calc-root span, #gmid-calc-root div { color: var(--ink-soft) !important; font-family: var(--sans) !important; }
        #gmid-calc-root .calc-value, #gmid-calc-root [class*="value"], #gmid-calc-root [class*="result"] { color: var(--ink) !important; font-family: var(--mono) !important; }
        #gmid-calc-root canvas { filter: hue-rotate(160deg) saturate(0.7) brightness(0.8); }

        /* FOOTER */
        .page-footer { background: var(--ink); color: var(--paper); padding: 20px 32px; display: flex; justify-content: space-between; align-items: center; font-family: var(--mono); font-size: 10px; letter-spacing: 0.12em; }
        .page-footer .c { color: #6a7485; }

        @media print {
            .navbar, .share-section, .page-footer { display: none !important; }
            .page-outer { padding: 24px !important; }
            body { background: white !important; }
        }
"""

NOTEBOOK_FONTS = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">"""

NOTEBOOK_NAVBAR = """
<nav class="navbar" id="navbar">
    <div class="nav-container">
        <a class="nav-logo" href="../index.html#home">
            <span class="logo-text">&lt;Jatin/&gt;</span>
        </a>
        <div class="nav-menu" id="nav-menu">
            <!-- Navigation Links -->
            <a class="nav-link" href="../index.html#home">Home</a>
            <a class="nav-link" href="../index.html#about">About</a>
            <a class="nav-link" href="../index.html#experience">Experience</a>
            <a class="nav-link {active_projects}" href="../index.html#projects">Projects</a>
            <a class="nav-link" href="../index.html#skills">Skills</a>
            <a class="nav-link {active_blog}" href="../index.html#blog">Blog</a>
            <a class="nav-link" href="../index.html#contact">Contact</a>
            <!-- Dark Mode Toggle -->
            <button aria-label="Toggle dark mode" class="theme-toggle-btn" id="theme-toggle">
                <i class="fas fa-moon"></i>
            </button>
            <!-- Resume Link -->
            <a class="nav-btn" download="" href="../resume.pdf">
                <i class="fas fa-download"></i> Resume
            </a>
        </div>
        <!-- Mobile Menu Icon -->
        <div class="hamburger" id="hamburger">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </div>
    </div>
</nav>"""

NOTEBOOK_SCRIPTS = """
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="../js/gmid-calculator.js"></script>
<script src="../js/code-runner.js"></script>
<script>
    window.addEventListener('scroll', () => {
        const el = document.getElementById('reading-progress');
        if (!el) return;
        const h = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        el.style.width = (h > 0 ? (window.pageYOffset / h) * 100 : 0) + '%';
    });
    function copyCode(btn) {
        const code = btn.closest('.code-block').querySelector('code').innerText;
        navigator.clipboard.writeText(code).then(() => {
            const icon = btn.querySelector('i');
            const old = icon.className; icon.className = 'fas fa-check';
            btn.classList.add('copied');
            setTimeout(() => { icon.className = old; btn.classList.remove('copied'); }, 2000);
        });
    }

    // Dark mode toggle functionality
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
        const moonIcon = '<i class="fas fa-moon"></i>';
        const sunIcon = '<i class="fas fa-sun"></i>';
        const updateButton = () => {
            const isLight = document.body.classList.contains('light-theme');
            toggleBtn.innerHTML = isLight ? moonIcon : sunIcon;
        };
        updateButton();
        toggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            const isLight = document.body.classList.contains('light-theme');
            localStorage.setItem('jatin-theme-pref', isLight ? 'light' : 'dark');
            updateButton();
        });
    }

    // Hamburger mobile menu toggle
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
</script>"""

MATHJAX_HEAD = """
    <script>
        MathJax = {
            tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true },
            options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>"""

# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def ensure_directories():
    for d in [TEX_SOURCE_DIR, PROJECTS_DIR, BLOG_DIR, IMAGES_DIR]:
        os.makedirs(d, exist_ok=True)
    os.makedirs(os.path.join(IMAGES_DIR, "projects"), exist_ok=True)
    os.makedirs(os.path.join(IMAGES_DIR, "blogs"), exist_ok=True)


def read_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------------------

def _find(pattern, text, default=""):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else default


def extract_title(tex):       return _find(r'\\title\s*\{((?:[^{}]|\{[^{}]*\})*)\}',   tex) or "Untitled"
def extract_author(tex):      return _find(r'\\author\s*\{((?:[^{}]|\{[^{}]*\})*)\}',  tex) or "Jatin"
def extract_subtitle(tex):    return _find(r'\\subtitle\s*\{([^}]+)\}',                tex)

def extract_meta(tex):
    keys = ['githublink','paperlink','category','readtime','duration',
            'date','description','technode']
    return {k: _find(rf'\\{k}\s*\{{([^}}]+)\}}', tex) for k in keys}


def extract_document_content(tex):
    m = re.search(r'\\begin\{document\}(.*)\\end\{document\}', tex, re.DOTALL)
    return m.group(1).strip() if m else tex


# ---------------------------------------------------------------------------
# LaTeX → HTML converter
# ---------------------------------------------------------------------------

def convert_tex_to_html(tex_content, image_folder):
    html = tex_content

    # Strip preamble commands that might have leaked into body
    preamble = [
        r'\\documentclass\[[^\]]*\]\{[^}]+\}', r'\\documentclass\{[^}]+\}',
        r'\\usepackage\[[^\]]*\]\{[^}]+\}',    r'\\usepackage\{[^}]+\}',
        r'\\title\{[^}]+\}', r'\\author\{[^}]+\}', r'\\date\{[^}]+\}',
        r'\\description\{[^}]+\}', r'\\subtitle\{[^}]+\}',
        r'\\maketitle', r'\\tableofcontents',
        r'\\begin\{document\}', r'\\end\{document\}',
        r'\\githublink\{[^}]+\}', r'\\paperlink\{[^}]+\}',
        r'\\category\{[^}]+\}', r'\\readtime\{[^}]+\}',
        r'\\duration\{[^}]+\}', r'\\technode\{[^}]+\}',
    ]
    for p in preamble:
        html = re.sub(p, '', html)

    # ── Protect code blocks so % comments inside are not stripped ──────────
    code_blocks = []
    def protect_code(m):
        code_blocks.append(m.group(0))
        return f"__CODEBLOCK_{len(code_blocks)-1}__"

    html = re.sub(r'\\begin\{lstlisting\}(?:\[[^\]]*\])?(.+?)\\end\{lstlisting\}',
                  protect_code, html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{verbatim\}(.+?)\\end\{verbatim\}',
                  protect_code, html, flags=re.DOTALL)

    # Strip LaTeX comments
    html = re.sub(r'(?<!\\)%.*$', '', html, flags=re.MULTILINE)

    # ── Sections ────────────────────────────────────────────────────────────
    html = re.sub(r'\\section\*?\{([^}]+)\}',       r'<h2>\1</h2>', html)
    html = re.sub(r'\\subsection\*?\{([^}]+)\}',    r'<h3>\1</h3>', html)
    html = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'<h4>\1</h4>', html)

    # ── Text formatting ──────────────────────────────────────────────────────
    html = re.sub(r'\\textbf\{([^}]+)\}',   r'<strong>\1</strong>', html)
    html = re.sub(r'\\textit\{([^}]+)\}',   r'<em>\1</em>',         html)
    html = re.sub(r'\\emph\{([^}]+)\}',     r'<em>\1</em>',         html)
    html = re.sub(r'\\underline\{([^}]+)\}',r'<u>\1</u>',           html)
    html = re.sub(r'\\texttt\{([^}]+)\}',   r'<code>\1</code>',     html)

    # ── Math ────────────────────────────────────────────────────────────────
    html = re.sub(r'\\begin\{equation\*?\}(.+?)\\end\{equation\*?\}',
                  r'<div class="math-block">\\[\1\\]</div>', html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{align\*?\}(.+?)\\end\{align\*?\}',
                  r'<div class="math-block">\\[\\begin{align}\1\\end{align}\\]</div>',
                  html, flags=re.DOTALL)
    html = re.sub(r'\$\$(.+?)\$\$',
                  r'<div class="math-block">\\[\1\\]</div>', html, flags=re.DOTALL)
    html = re.sub(r'\$([^$\n]+)\$', r'\\(\1\\)', html)

    # ── Lists ───────────────────────────────────────────────────────────────
    def convert_list(tag, match):
        items = re.findall(r'\\item\s*(.+?)(?=\\item|$)', match.group(1), re.DOTALL)
        return f'<{tag}>\n' + ''.join(f'    <li>{i.strip()}</li>\n' for i in items) + f'</{tag}>'

    html = re.sub(r'\\begin\{itemize\}(.+?)\\end\{itemize\}',
                  lambda m: convert_list('ul', m), html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{enumerate\}(.+?)\\end\{enumerate\}',
                  lambda m: convert_list('ol', m), html, flags=re.DOTALL)

    # ── Figures ─────────────────────────────────────────────────────────────
    def convert_figure(m):
        c = m.group(1)
        img = re.search(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', c)
        cap = re.search(r'\\caption\{([^}]+)\}', c)
        if not img:
            return ''
        name = os.path.basename(img.group(1))
        caption = cap.group(1) if cap else ''
        return (f'<figure class="content-figure">\n'
                f'    <img src="../images/{image_folder}/{name}" alt="{caption}">\n'
                f'    <figcaption>{caption}</figcaption>\n'
                f'</figure>')

    html = re.sub(r'\\begin\{figure\}(?:\[[^\]]*\])?(.+?)\\end\{figure\}',
                  convert_figure, html, flags=re.DOTALL)
    html = re.sub(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',
                  lambda m: f'<img src="../images/{image_folder}/{os.path.basename(m.group(1))}" alt="">',
                  html)

    # ── Tables ──────────────────────────────────────────────────────────────
    def convert_table(m):
        rows = m.group(1).strip().split('\\\\')
        out = '<table>\n<thead>\n'
        first = True
        for row in rows:
            cleaned = re.sub(r'\\hline', '', row).strip()
            if not cleaned:
                continue
            cells = [c.strip() for c in cleaned.split('&') if c.strip()]
            if not cells:
                continue
            if first:
                out += '    <tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>\n'
                out += '</thead>\n<tbody>\n'
                first = False
            else:
                out += '    <tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n'
        out += '</tbody>\n</table>'
        return out

    html = re.sub(r'\\begin\{tabular\}\{[^}]+\}(.+?)\\end\{tabular\}',
                  convert_table, html, flags=re.DOTALL)

    # ── Restore and convert code blocks ─────────────────────────────────────
    for i, raw in enumerate(code_blocks):
        # Parse language option
        lang_m = re.search(r'\\begin\{lstlisting\}\[([^\]]*)\]', raw)
        lang = ''
        if lang_m:
            lm = re.search(r'language\s*=\s*(\w+)', lang_m.group(1), re.IGNORECASE)
            lang = lm.group(1).lower() if lm else ''

        # Extract code body
        body_m = re.search(r'\\begin\{(?:lstlisting|verbatim)\}(?:\[[^\]]*\])?(.*?)\\end\{(?:lstlisting|verbatim)\}',
                           raw, re.DOTALL)
        code = body_m.group(1).strip() if body_m else raw

        code_escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        if lang in ('python',):
            badge = '<span class="code-lang-badge python">PYTHON</span>'
        elif lang in ('matlab', 'octave'):
            badge = '<span class="code-lang-badge matlab">MATLAB</span>'
        else:
            badge = '<span class="code-lang-badge default">CODE</span>'

        block = (f'<div class="code-block">\n'
                 f'    <div class="code-block-head">\n'
                 f'        <div>{badge}</div>\n'
                 f'        <button class="copy-btn" onclick="copyCode(this)"><i class="far fa-copy"></i> COPY</button>\n'
                 f'    </div>\n'
                 f'    <pre><code>{code_escaped}</code></pre>\n'
                 f'</div>')
        html = html.replace(f"__CODEBLOCK_{i}__", block)

    # ── Blockquotes ─────────────────────────────────────────────────────────
    html = re.sub(r'\\begin\{quote\}(.+?)\\end\{quote\}',
                  r'<blockquote>\1</blockquote>', html, flags=re.DOTALL)

    # ── Insight / infobox ───────────────────────────────────────────────────
    def box(m):
        return f'<div class="insight-box">{m.group(1).strip()}</div>'

    html = re.sub(r'\\begin\{insight\}(.+?)\\end\{insight\}',   box, html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{infobox\}(.+?)\\end\{infobox\}',   box, html, flags=re.DOTALL)
    html = re.sub(r'\\insight\{([^}]+)\}',
                  r'<div class="insight-box">\1</div>', html)

    # ── Custom site widgets ──────────────────────────────────────────────────
    html = re.sub(r'\\gmidcalc', '<div id="gmid-calc-root"></div>', html)

    # ── Cleanup ─────────────────────────────────────────────────────────────
    for cmd in [r'\\label\{[^}]+\}', r'\\ref\{[^}]+\}', r'\\cite\{[^}]+\}',
                r'\\centering', r'\\hline', r'\\newpage', r'\\clearpage', r'\\noindent']:
        html = re.sub(cmd, '', html)

    # ── Wrap loose text in <p> ───────────────────────────────────────────────
    # Protect block elements
    blocks, protected = [], []
    def protect_block(m):
        protected.append(m.group(0))
        return f"__BLOCK_{len(protected)-1}__"

    for pat in [r'<h[1-6][^>]*>.*?</h[1-6]>', r'<pre[^>]*>.*?</pre>',
                r'<table[^>]*>.*?</table>', r'<blockquote[^>]*>.*?</blockquote>',
                r'<figure[^>]*>.*?</figure>', r'<ul[^>]*>.*?</ul>',
                r'<ol[^>]*>.*?</ol>', r'<div[^>]*>.*?</div>', r'<p[^>]*>.*?</p>']:
        html = re.sub(pat, protect_block, html, flags=re.DOTALL)

    segments = re.split(r'\n\s*\n', html)
    out_segs = []
    for seg in segments:
        s = seg.strip()
        if not s:
            continue
        if re.match(r'^__BLOCK_\d+__$', s):
            out_segs.append(s)
        else:
            out_segs.append(f'<p>{s}</p>')
    html = '\n\n'.join(out_segs)

    for i in range(len(protected) - 1, -1, -1):
        html = html.replace(f"__BLOCK_{i}__", protected[i])

    html = re.sub(r'\n{3,}', '\n\n', html)
    return html.strip()


# ---------------------------------------------------------------------------
# Image copying
# ---------------------------------------------------------------------------

def copy_images(tex_filepath, page_type):
    tex_dir = os.path.dirname(tex_filepath)
    target  = os.path.join(IMAGES_DIR, f"{page_type}s")
    with open(tex_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    images  = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', content)
    copied  = []
    for img in images:
        name = os.path.basename(img)
        for ext in ['', '.png', '.jpg', '.jpeg', '.pdf']:
            src = os.path.join(tex_dir, img + ext)
            if os.path.exists(src):
                dest = os.path.join(target, os.path.basename(src))
                shutil.copy2(src, dest)
                copied.append(os.path.basename(src))
                print(f"  ✓ Copied image: {os.path.basename(src)}")
                break
    return copied


# ---------------------------------------------------------------------------
# HTML page generators
# ---------------------------------------------------------------------------

def generate_blog_page(title, content, meta, author="Jatin"):
    category    = meta.get('category') or "Blog"
    date_str    = meta.get('date')    or datetime.now().strftime("%B %d, %Y")
    read_time   = meta.get('readtime') or "5 min"
    description = meta.get('description') or f"{title} — Blog post by Jatin"
    subtitle    = meta.get('subtitle', '')

    subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''
    navbar = NOTEBOOK_NAVBAR.format(
        active_projects='', active_blog='active')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Jatin</title>
    <meta name="description" content="{description}">
{NOTEBOOK_FONTS}
    <link rel="stylesheet" href="../css/styles-notebook.css">
{MATHJAX_HEAD}
    <style>{NOTEBOOK_CSS}
        .page-outer {{ max-width: 940px; margin: 0 auto; padding: 100px 40px 80px; }}
        @media (max-width: 768px) {{
            .page-outer {{
                padding-top: 80px !important;
                padding-left: 20px !important;
                padding-right: 20px !important;
                padding-bottom: 40px !important;
            }}
            h1.page-title {{
                font-size: 28px !important;
            }}
            .page-content h2 {{
                font-size: 20px !important;
            }}
            .page-content table {{
                display: block;
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            .btn {{
                width: 100%;
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
<script>
    if (localStorage.getItem('jatin-theme-pref') === 'light') {{
        document.body.classList.add('light-theme');
    }}
</script>

<div id="reading-progress"></div>

{navbar}

<main class="page-outer">

    <a href="../index.html#blog" class="btn btn-primary" style="margin-bottom: 2.5rem;">
        <i class="fas fa-arrow-left"></i> BACK TO BLOG
    </a>

    <header class="page-header">
        <div class="page-kicker">{category}</div>
        <h1 class="page-title">{title}</h1>
        {subtitle_html}
        <div class="meta-row">
            <span class="meta-chip primary">{category}</span>
            <span class="meta-chip"><i class="far fa-calendar" style="margin-right:5px;"></i>{date_str}</span>
            <span class="meta-chip"><i class="far fa-clock" style="margin-right:5px;"></i>{read_time} read</span>
            <span class="meta-chip"><i class="far fa-user" style="margin-right:5px;"></i>{author}</span>
        </div>
    </header>

    <div class="page-content">
{content}
    </div>

    <div class="author-section">
        <div class="author-avatar"><i class="fas fa-user"></i></div>
        <div class="author-info">
            <h4>Written by {author}</h4>
            <p>Analog Circuit Design Engineer passionate about pushing the boundaries of silicon design.
            Specializing in OTAs, data converters, and design automation.</p>
        </div>
    </div>

    <div class="share-section">
        <span>Share:</span>
        <div class="share-btns">
            <a href="#" class="share-btn" aria-label="Share on Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" class="share-btn" aria-label="Share on LinkedIn"><i class="fab fa-linkedin-in"></i></a>
            <a href="#" class="share-btn" aria-label="Copy link"
               onclick="navigator.clipboard.writeText(location.href);return false;"><i class="fas fa-link"></i></a>
        </div>
    </div>

    <div style="text-align:center; margin-top:3rem;">
        <a href="../index.html#blog" class="btn btn-primary"><i class="fas fa-arrow-left"></i> BACK TO ALL POSTS</a>
    </div>

</main>

<footer class="page-footer">
    <span>&copy; 2026 Jatin</span>
    <span class="c">Analog Circuit Design</span>
</footer>

{NOTEBOOK_SCRIPTS}
</body>
</html>"""


def generate_project_page(title, content, meta):
    category    = meta.get('category') or "Project"
    date_str    = meta.get('date')     or datetime.now().strftime("%B %Y")
    description = meta.get('description') or f"{title} — Project by Jatin"
    duration    = meta.get('duration') or ""
    github      = meta.get('githublink') or "#"
    paper       = meta.get('paperlink')  or "#"
    technode    = meta.get('technode')   or ""
    subtitle    = meta.get('subtitle', '')

    subtitle_html  = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''
    technode_chip  = f'<span class="meta-chip">{technode}</span>' if technode else ''
    duration_chip  = f'<span class="meta-chip"><i class="far fa-clock" style="margin-right:5px;"></i>{duration}</span>' if duration else ''
    github_btn     = f'<a href="{github}" target="_blank" class="btn btn-primary"><i class="fab fa-github"></i> VIEW CODE</a>'
    paper_btn      = f'<a href="{paper}"  target="_blank" class="btn btn-secondary"><i class="fas fa-file-pdf"></i> READ PAPER</a>'

    navbar = NOTEBOOK_NAVBAR.format(
        active_projects='active', active_blog='')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Jatin</title>
    <meta name="description" content="{description}">
{NOTEBOOK_FONTS}
    <link rel="stylesheet" href="../css/styles-notebook.css">
{MATHJAX_HEAD}
    <style>{NOTEBOOK_CSS}
        .page-outer {{ max-width: 940px; margin: 0 auto; padding: 100px 40px 80px; }}
        @media (max-width: 768px) {{
            .page-outer {{
                padding-top: 80px !important;
                padding-left: 20px !important;
                padding-right: 20px !important;
                padding-bottom: 40px !important;
            }}
            h1.page-title {{
                font-size: 28px !important;
            }}
            .page-content h2 {{
                font-size: 20px !important;
            }}
            .page-content table {{
                display: block;
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            .btn {{
                width: 100%;
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
<script>
    if (localStorage.getItem('jatin-theme-pref') === 'light') {{
        document.body.classList.add('light-theme');
    }}
</script>

<div id="reading-progress"></div>

{navbar}

<main class="page-outer">

    <a href="../index.html#projects" class="btn btn-primary" style="margin-bottom: 2.5rem;">
        <i class="fas fa-arrow-left"></i> BACK TO PROJECTS
    </a>

    <header class="page-header">
        <div class="page-kicker">{category}</div>
        <h1 class="page-title">{title}</h1>
        {subtitle_html}
        <div class="meta-row">
            <span class="meta-chip primary">{category}</span>
            <span class="meta-chip"><i class="far fa-calendar" style="margin-right:5px;"></i>{date_str}</span>
            {technode_chip}
            {duration_chip}
        </div>
        <div class="project-actions">
            {github_btn}
            {paper_btn}
        </div>
    </header>

    <div class="page-content">
{content}
    </div>

    <div class="share-section">
        <span>Share:</span>
        <div class="share-btns">
            <a href="#" class="share-btn" aria-label="Share on Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" class="share-btn" aria-label="Share on LinkedIn"><i class="fab fa-linkedin-in"></i></a>
            <a href="#" class="share-btn" aria-label="Copy link"
               onclick="navigator.clipboard.writeText(location.href);return false;"><i class="fas fa-link"></i></a>
        </div>
    </div>

    <div style="text-align:center; margin-top:3rem;">
        <a href="../index.html#projects" class="btn btn-primary"><i class="fas fa-arrow-left"></i> BACK TO ALL PROJECTS</a>
    </div>

</main>

<footer class="page-footer">
    <span>&copy; 2026 Jatin</span>
    <span class="c">Analog Circuit Design</span>
</footer>

{NOTEBOOK_SCRIPTS}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Slug
# ---------------------------------------------------------------------------

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    ensure_directories()

    print("\n" + "="*60)
    print("  TEX TO WEBSITE CONVERTER  (Notebook Theme)")
    print("="*60 + "\n")

    if len(sys.argv) >= 3:
        page_type = sys.argv[1]
        tex_file  = sys.argv[2]
    else:
        print("Choose page type:")
        print("  1. Project")
        print("  2. Blog Post")
        choice    = input("\nEnter 1 or 2: ").strip()
        page_type = "project" if choice == "1" else "blog"

        tex_files = [f for f in os.listdir(TEX_SOURCE_DIR) if f.endswith('.tex')]
        if not tex_files:
            print(f"\n⚠  No .tex files found in '{TEX_SOURCE_DIR}'")
            input("\nPress Enter to exit...")
            return

        print(f"\nAvailable .tex files:")
        for i, f in enumerate(tex_files, 1):
            print(f"  {i}. {f}")

        fc = input("\nEnter file number: ").strip()
        try:
            tex_file = tex_files[int(fc) - 1]
        except Exception:
            print("Invalid choice!")
            return

    tex_filepath = os.path.join(TEX_SOURCE_DIR, tex_file)
    if not os.path.exists(tex_filepath):
        print(f"\n✗ Error: File not found: {tex_filepath}")
        return

    print(f"\n→ Processing: {tex_file}")

    tex_content  = read_tex_file(tex_filepath)
    title        = extract_title(tex_content)
    author       = extract_author(tex_content)
    subtitle     = extract_subtitle(tex_content)
    meta         = extract_meta(tex_content)
    meta['subtitle'] = subtitle

    doc_content  = extract_document_content(tex_content)
    html_content = convert_tex_to_html(doc_content, f"{page_type}s")

    print("→ Copying images...")
    copied = copy_images(tex_filepath, page_type)
    if not copied:
        print("  (No images found)")

    print("→ Generating HTML page...")
    if page_type == "project":
        full_html  = generate_project_page(title, html_content, meta)
        output_dir = PROJECTS_DIR
    else:
        full_html  = generate_blog_page(title, html_content, meta, author)
        output_dir = BLOG_DIR

    output_path = os.path.join(output_dir, slugify(title) + ".html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"\n✓ Done!  →  {output_path}\n")

    if len(sys.argv) < 3:
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
