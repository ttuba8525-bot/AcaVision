// --- CUSTOM CURSOR & PARTICLE TRAIL ---
const cursor = document.getElementById('cursor');

// Disable native cursor globally, but restore it where cursor element fails
document.body.style.cursor = 'none';

let mouseX = 0, mouseY = 0;
let customCursorX = 0, customCursorY = 0;

// Cursor tracking
document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    if (cursor) {
        cursor.style.left = `${mouseX}px`;
        cursor.style.top = `${mouseY}px`;
    }

    createParticle(mouseX, mouseY);
});

// Magnetic Hover Effects on Buttons and Cards
const magneticElements = document.querySelectorAll('.btn-primary, .btn-outline, .magnetic');

magneticElements.forEach(el => {
    el.addEventListener('mouseenter', () => {
        if (cursor) cursor.classList.add('hover-magnetic');
    });
    el.addEventListener('mouseleave', () => {
        if (cursor) cursor.classList.remove('hover-magnetic');
    });

    // Magnetic pull calculation for premium feel
    el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        // Gentle magnetic pull (max 10px translate)
        const pullX = x * 0.1;
        const pullY = y * 0.1;

        el.style.transform = `translate(${pullX}px, ${pullY}px) scale(1.02)`;
    });

    el.addEventListener('mouseleave', () => {
        el.style.transform = ''; // Reset transform
    });
});

// Particle Trail Logic
function createParticle(x, y) {
    if (Math.random() > 0.4) return; // Limit particle generation rate

    const particle = document.createElement('div');
    particle.className = 'particle';

    // Randomize color between primary blue and purple
    const isBlue = Math.random() > 0.5;
    const color = isBlue ? 'rgba(79, 140, 255, 0.6)' : 'rgba(166, 108, 255, 0.6)';

    const size = Math.random() * 8 + 4; // 4px to 12px

    particle.style.background = color;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${x}px`;
    particle.style.top = `${y}px`;
    particle.style.boxShadow = `0 0 ${size}px ${color}`;

    document.body.appendChild(particle);

    // Animate and remove
    const destX = x + (Math.random() - 0.5) * 60;
    const destY = y + (Math.random() - 0.5) * 60 - 40; // Float upwards

    particle.animate([
        { transform: 'translate(0, 0) scale(1)', opacity: 1 },
        { transform: `translate(${destX - x}px, ${destY - y}px) scale(0)`, opacity: 0 }
    ], {
        duration: Math.random() * 1000 + 500,
        easing: 'cubic-bezier(0, .9, .57, 1)'
    }).onfinish = () => {
        particle.remove();
    };
}


// --- NAVBAR SCROLL EFFECT ---
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.9)';
            navbar.style.boxShadow = '0 4px 30px rgba(79, 140, 255, 0.1)';
        } else {
            navbar.style.background = 'rgba(245, 249, 255, 0.8)';
            navbar.style.boxShadow = 'none';
        }
    }
});

// Highlight Active Nav Link
const currentLocation = location.pathname;
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    if (link.getAttribute('href') === currentLocation && currentLocation !== '/') {
        link.classList.add('active');
    } else if (currentLocation === '/' && link.getAttribute('href') === '/') {
        link.classList.add('active');
    }
});
