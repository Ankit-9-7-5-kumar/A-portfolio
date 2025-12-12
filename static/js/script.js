// mobile menu toggle
const toggle = document.getElementById('mobile-toggle');
const nav = document.querySelector('.main-nav');

toggle && toggle.addEventListener('click', () => {
  if (!nav) return;
  nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
  nav.style.flexDirection = 'column';
  nav.style.position = 'absolute';
  nav.style.right = '18px';
  nav.style.top = '72px';
  nav.style.background = 'rgba(10,14,20,0.95)';
  nav.style.padding = '12px';
  nav.style.borderRadius = '10px';
  nav.style.zIndex = 9999;
});

// smooth-scroll with offset (safety)
const headerH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 72;
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click', function(e){
    const href = this.getAttribute('href');
    if(!href || href === '#') return;
    const target = document.querySelector(href);
    if(!target) return;
    e.preventDefault();
    const topPos = target.getBoundingClientRect().top + window.pageYOffset;
    const offset = topPos - headerH - 12;
    window.scrollTo({ top: offset, behavior: 'smooth' });
    // hide mobile nav after click
    if(window.innerWidth <= 720 && nav) nav.style.display = 'none';
  });
});

