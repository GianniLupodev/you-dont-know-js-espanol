// YDKJS Español — interacción del lector
(function(){
  var root = document.documentElement;
  var saved = localStorage.getItem('ydkjs-theme');
  if(saved){ root.setAttribute('data-theme', saved); }
  function syncThemeIcon(){
    var dark = root.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('#themeBtn').forEach(function(b){ b.textContent = dark ? '☀️' : '🌙'; });
  }
  syncThemeIcon();
  document.querySelectorAll('#themeBtn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var dark = root.getAttribute('data-theme') === 'dark';
      var next = dark ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('ydkjs-theme', next);
      syncThemeIcon();
    });
  });

  // Menú móvil
  var menuBtn = document.getElementById('menuBtn');
  var sidebar = document.getElementById('sidebar');
  var scrim = document.getElementById('scrim');
  function closeMenu(){ if(sidebar) sidebar.classList.remove('open'); if(scrim) scrim.classList.remove('show'); }
  if(menuBtn){ menuBtn.addEventListener('click', function(){
    sidebar.classList.toggle('open'); scrim.classList.toggle('show');
  });}
  if(scrim){ scrim.addEventListener('click', closeMenu); }

  // Botón copiar código
  document.querySelectorAll('.copy-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var code = btn.parentElement.querySelector('code');
      navigator.clipboard.writeText(code.innerText).then(function(){
        btn.textContent = '¡Copiado!'; btn.classList.add('done');
        setTimeout(function(){ btn.textContent = 'Copiar'; btn.classList.remove('done'); }, 1600);
      });
    });
  });

  // Barra de progreso + botón arriba
  var progress = document.getElementById('progressBar');
  var topBtn = document.getElementById('topBtn');
  function onScroll(){
    var h = document.documentElement;
    var scrolled = h.scrollTop / (h.scrollHeight - h.clientHeight);
    if(progress) progress.style.width = (scrolled*100) + '%';
    if(topBtn){ if(h.scrollTop > 500) topBtn.classList.add('show'); else topBtn.classList.remove('show'); }
    highlightTOC();
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  if(topBtn){ topBtn.addEventListener('click', function(){ window.scrollTo({top:0,behavior:'smooth'}); }); }

  // Resaltar sección activa en el TOC
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc-list a'));
  var targets = tocLinks.map(function(a){ return document.getElementById(a.getAttribute('href').slice(1)); });
  function highlightTOC(){
    if(!tocLinks.length) return;
    var pos = window.scrollY + 120, idx = 0;
    for(var i=0;i<targets.length;i++){ if(targets[i] && targets[i].offsetTop <= pos) idx = i; }
    tocLinks.forEach(function(a,i){ a.classList.toggle('active', i===idx); });
  }
  onScroll();
})();
