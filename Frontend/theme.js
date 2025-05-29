// theme.js - Versão Corrigida
document.addEventListener('DOMContentLoaded', function() {
  // Sistema de tema completo
  const themeToggle = document.getElementById('darkModeToggle');
  const html = document.documentElement;
  
  // Carrega tema salvo ou preferência do sistema
  const savedTheme = localStorage.getItem('theme') || 
                    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  
  // Aplica o tema inicial
  applyTheme(savedTheme);

  // Configura o botão
  if (themeToggle) {
    themeToggle.addEventListener('click', function(e) {
      e.preventDefault();
      const currentTheme = html.getAttribute('data-bs-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
    });
  }

  function applyTheme(theme) {
    // 1. Aplica no HTML
    html.setAttribute('data-bs-theme', theme);
    
    // 2. Salva preferência
    localStorage.setItem('theme', theme);
    
    // 3. Atualiza ícone
    updateThemeIcon(theme);
    
    // 4. Força redesenho
    forceRedraw();
  
    // 5. Ajusta cores específicas
    adjustCustomColors(theme);
  }

  function updateThemeIcon(theme) {
    const icons = document.querySelectorAll('#darkModeToggle i');
    icons.forEach(icon => {
      icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    });
  }

  function forceRedraw() {
    // Técnica para forçar recálculo de estilos
    const tmp = html.style.visibility;
    html.style.visibility = 'hidden';
    html.style.visibility = tmp;
  }

  function adjustCustomColors(theme) {
    // Ajusta a cor do navbar que estava fixa
    const navbars = document.querySelectorAll('.navbar');
    navbars.forEach(navbar => {
      navbar.style.backgroundColor = theme === 'dark' ? '#145a25' : '#1e7e34';
    });
  }
  
  // Verifica mudanças no sistema (opcional)
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('theme')) { // Só muda se não tiver preferência salva
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });
});