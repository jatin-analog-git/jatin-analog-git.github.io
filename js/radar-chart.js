/**
 * radar-chart.js
 * Renders an interactive radar/spider chart of skills using Chart.js.
 * Targets <canvas id="skills-radar"> in the Skills section.
 * Reads accent colors from CSS custom properties so it respects theme switching.
 */

(function () {
    function getCSSVar(name) {
        return getComputedStyle(document.documentElement)
            .getPropertyValue(name)
            .trim();
    }

    function buildChart() {
        const canvas = document.getElementById('skills-radar');
        if (!canvas) return;

        const accentPrimary   = getCSSVar('--accent-primary')   || '#00d4ff';
        const accentTertiary  = getCSSVar('--accent-tertiary')  || '#00ff88';
        const textSecondary   = getCSSVar('--text-secondary')   || '#94a3b8';
        const bgTertiary      = getCSSVar('--bg-tertiary')      || '#161830';

        const data = {
            labels: [
                'OTA Design',
                'Data Converters',
                'Bandgap & Refs',
                'PLL Design',
                'Cadence Virtuoso',
                'HSPICE / Spectre',
                'MATLAB',
                'gm/ID Methodology',
            ],
            datasets: [
                {
                    label: 'Proficiency',
                    data: [95, 85, 90, 70, 95, 85, 90, 92],
                    fill: true,
                    backgroundColor: accentPrimary + '22',
                    borderColor: accentPrimary,
                    pointBackgroundColor: accentTertiary,
                    pointBorderColor: accentPrimary,
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: accentPrimary,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 2,
                },
            ],
        };

        const config = {
            type: 'radar',
            data,
            options: {
                responsive: true,
                maintainAspectRatio: true,
                animation: {
                    duration: 1200,
                    easing: 'easeOutQuart',
                },
                scales: {
                    r: {
                        min: 0,
                        max: 100,
                        ticks: {
                            stepSize: 25,
                            display: false,
                        },
                        grid: {
                            color: accentPrimary + '22',
                            lineWidth: 1,
                        },
                        angleLines: {
                            color: accentPrimary + '33',
                            lineWidth: 1,
                        },
                        pointLabels: {
                            color: textSecondary,
                            font: {
                                family: "'Inter', sans-serif",
                                size: 11,
                            },
                        },
                    },
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: bgTertiary,
                        borderColor: accentPrimary + '66',
                        borderWidth: 1,
                        titleColor: accentPrimary,
                        bodyColor: textSecondary,
                        callbacks: {
                            label: ctx => `  ${ctx.raw}%`,
                        },
                    },
                },
            },
        };

        /* Animate in when the canvas scrolls into view */
        let chart = null;

        const observer = new IntersectionObserver(
            entries => {
                if (entries[0].isIntersecting && !chart) {
                    chart = new Chart(canvas, config);
                    observer.unobserve(canvas);
                }
            },
            { threshold: 0.3 }
        );

        observer.observe(canvas);

        /* Re-render on theme switch so colors update */
        document.addEventListener('themeChanged', () => {
            if (!chart) return;
            const p = getCSSVar('--accent-primary');
            const t = getCSSVar('--accent-tertiary');
            const s = getCSSVar('--text-secondary');
            chart.data.datasets[0].backgroundColor  = p + '22';
            chart.data.datasets[0].borderColor       = p;
            chart.data.datasets[0].pointBackgroundColor = t;
            chart.data.datasets[0].pointBorderColor  = p;
            chart.options.scales.r.grid.color        = p + '22';
            chart.options.scales.r.angleLines.color  = p + '33';
            chart.options.scales.r.pointLabels.color = getCSSVar('--text-secondary');
            chart.update();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildChart);
    } else {
        buildChart();
    }
})();
