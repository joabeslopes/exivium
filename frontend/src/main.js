if (!token){
  window.location.href = "login.html"
};

// Espera o DOM carregar para aplicar o efeito de fade-in
window.addEventListener("DOMContentLoaded", () => {

  document.body.classList.add("loaded");

  // Exibe o nome do usuário (pode vir do backend futuramente)
  document.getElementById("userName").textContent = "Rafael";

  const logoutBtn = document.getElementById("logoutBtn");

  // Função de logout
  logoutBtn.addEventListener('click', () => {
    const confirmLogout = confirm('Deseja realmente sair do sistema?');

    if (confirmLogout) {
      // Limpar dados salvos
      localStorage.clear();

      // Redirecionar para página de login (ajuste o caminho conforme necessário)
      window.location.href = 'login.html';
    }
  });
});

// Função genérica de transição suave entre páginas
function fadeAndRedirect(url) {
  document.body.classList.add("fade-out");
  setTimeout(() => {
    window.location.href = url;
  }, 400); // tempo igual ao do CSS
}

// Botão: Ver Câmeras
function goToCameras() {
  fadeAndRedirect("dashboard.html");
}

// Botão: Configurações (futuramente)
function goToConfig() {
  fadeAndRedirect("config.html");
}