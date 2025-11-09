// Garante que o código só roda depois que o DOM estiver pronto
document.addEventListener("DOMContentLoaded", () => {


  // Seletores principais
  const menuConfig = document.getElementById("menuConfig");
  const addCameraSection = document.getElementById("addCameraSection");
  const removeCameraSection = document.getElementById("removeCameraSection");
  const cameraList = document.getElementById("cameraList");

  // Botões
  const btnAddCamera = document.getElementById("btnAddCamera");
  const btnRemoveCamera = document.getElementById("btnRemoveCamera");
  const logoutBtn = document.getElementById("logoutBtn");
  const addCameraForm = document.getElementById("addCameraForm");

  // Botão de logout
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("loggedIn");
    localStorage.removeItem("username");
    window.location.href = "login.html";
  });

  // Adicionar câmera (mostra formulário)
  btnAddCamera.addEventListener("click", () => {
    menuConfig.classList.add("hidden");
    addCameraSection.classList.remove("hidden");
    removeCameraSection.classList.add("hidden");
  });

  // Remover câmera (mostra lista)
  btnRemoveCamera.addEventListener("click", () => {
    menuConfig.classList.add("hidden");
    removeCameraSection.classList.remove("hidden");
    addCameraSection.classList.add("hidden");
    loadCameraList();
  });

  // Voltar ao menu principal
  document.querySelectorAll(".btnVoltar").forEach((btn) => {
    btn.addEventListener("click", () => {
      addCameraSection.classList.add("hidden");
      removeCameraSection.classList.add("hidden");
      menuConfig.classList.remove("hidden");
    });
  });


});
