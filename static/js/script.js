// ═══════════════════════════════════════════
// EduInsight — Global JS
// Cursor, Particles, Navbar, AOS, Nav active
// ═══════════════════════════════════════════

// ── Custom Cursor ──────────────────────────
const dot = document.getElementById('cursor-dot');
const ring = document.getElementById('cursor-ring');

document.addEventListener('mousemove', e => {
    if (dot) { dot.style.left = e.clientX + 'px'; dot.style.top = e.clientY + 'px'; }
    if (ring) { ring.style.left = e.clientX + 'px'; ring.style.top = e.clientY + 'px'; }
});

document.querySelectorAll('a,button,input,select,.glass').forEach(el => {
    el.addEventListener('mouseenter', () => { ring && ring.classList.add('ring-grow'); });
    el.addEventListener('mouseleave', () => { ring && ring.classList.remove('ring-grow'); });
});

// ── Particle Canvas ────────────────────────
(function () {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];

    function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
    resize();
    window.addEventListener('resize', resize);

    class Particle {
        constructor() { this.reset(); }
        reset() {
            this.x = Math.random() * W; this.y = Math.random() * H;
            this.r = Math.random() * 1.5 + 0.3;
            this.vx = (Math.random() - .5) * .3; this.vy = (Math.random() - .5) * .3;
            this.a = Math.random() * .4 + .1;
            this.c = Math.random() > .6 ? '0,245,255' : '124,58,237';
        }
        update() {
            this.x += this.vx; this.y += this.vy;
            if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
        }
        draw() {
            ctx.beginPath(); ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${this.c},${this.a})`; ctx.fill();
        }
    }

    for (let i = 0; i < 60; i++) particles.push(new Particle());

    function connect() {
        for (let i = 0; i < particles.length; i++)
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x, dy = particles[i].y - particles[j].y;
                const d = Math.sqrt(dx * dx + dy * dy);
                if (d < 120) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(0,245,255,${.08 * (1 - d / 120)})`;
                    ctx.lineWidth = .4; ctx.stroke();
                }
            }
    }

    function animate() {
        ctx.clearRect(0, 0, W, H);
        particles.forEach(p => { p.update(); p.draw(); });
        connect();
        requestAnimationFrame(animate);
    }
    animate();
})();

// ── Navbar scroll ──────────────────────────
window.addEventListener('scroll', () => {
    document.getElementById('navbar')?.classList.toggle('scrolled', window.scrollY > 40);
});

// ── Active nav link ────────────────────────
const path = location.pathname;
document.querySelectorAll('.nav-link').forEach(a => {
    if (a.getAttribute('href') === path || (path === '/' && a.getAttribute('href') === '/')) {
        a.classList.add('active');
    }
});

// ── AOS Init ──────────────────────────────
if (typeof AOS !== 'undefined') AOS.init({ once: true, duration: 700, easing: 'ease-out-cubic', offset: 60 });

// ── GSAP + ScrollTrigger ───────────────────
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
}

// ── Slider fill init (call on pages with sliders) ──
document.querySelectorAll('input[type="range"]').forEach(el => {
    const pct = ((el.value - el.min) / (el.max - el.min)) * 100;
    el.style.setProperty('--pct', pct + '%');
});

