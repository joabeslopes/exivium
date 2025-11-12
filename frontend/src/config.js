if (!token){
  window.location.href = "login.html";
};

let recursos = {};
let ativos = {};

async function criaRecurso(event) {
  event.preventDefault();

  const nome = document.getElementById("RecursoNome");
  const tipo = document.getElementById("RecursoTipo");
  const gitRepo = document.getElementById("RecursoGitRepo");

  const request = {
    "token": token,
    "nome": nome.value,
    "tipo": tipo.value,
    "git_repo_url": gitRepo.value
  };

  console.log(request);

  nome.value = "";
  tipo.value = "";
  gitRepo.value = "";
};

async function removeRecurso(event) {
  event.preventDefault();

  const removeRecursoSection = document.getElementById("removeRecursoSection");
  const recursoList = removeRecursoSection.querySelector('[name="RecursoList"]')[0];

};

async function ativaRecurso(event) {
  event.preventDefault();

  const ativaRecursoSection = document.getElementById("ativaRecursoSection");
  const recursoList = ativaRecursoSection.querySelector('[name="RecursoList"]')[0];

};

async function desativaRecurso(event) {
  event.preventDefault();

  const desativaRecursoSection = document.getElementById("desativaRecursoSection");
  const recursoList = desativaRecursoSection.querySelector('[name="RecursoList"]')[0];


};

// Garante que o código só roda depois que o DOM estiver pronto
document.addEventListener("DOMContentLoaded", () => {

  // Seletores principais
  const menuConfig = document.getElementById("menuConfig");
  const addRecursoSection = document.getElementById("addRecursoSection");
  const removeRecursoSection = document.getElementById("removeRecursoSection");
  const ativaRecursoSection = document.getElementById("ativaRecursoSection");
  const desativaRecursoSection = document.getElementById("desativaRecursoSection");

  // Botões
  const btnAddRecurso = document.getElementById("btnAddRecurso");
  const btnRemoveRecurso = document.getElementById("btnRemoveRecurso");
  const btnAtivaRecurso = document.getElementById("btnAtivaRecurso");
  const btnDesativaRecurso = document.getElementById("btnDesativaRecurso");
  const logoutBtn = document.getElementById("logoutBtn");
  const voltarBtn = document.getElementById('voltarBtn');

  // Função de logout
  logoutBtn.addEventListener('click', () => {
    const confirmLogout = confirm('Deseja realmente sair do sistema?');

    if (confirmLogout) {
      // Limpar dados salvos
      localStorage.clear();

      // Redirecionar para página de login
      window.location.href = 'login.html';
    }
  });

  // Botão de voltar
  voltarBtn.addEventListener('click', () => {
    window.location.href = 'index.html';
  });


  // Adicionar recurso
  btnAddRecurso.addEventListener("click", () => {
    addRecursoSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    removeRecursoSection.classList.add("hidden");
    ativaRecursoSection.classList.add("hidden");
    desativaRecursoSection.classList.add("hidden");
  });

  // Remover recurso
  btnRemoveRecurso.addEventListener("click", () => {
    removeRecursoSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    addRecursoSection.classList.add("hidden");
    ativaRecursoSection.classList.add("hidden");
    desativaRecursoSection.classList.add("hidden");
  });

  // Ativar recurso
  btnAtivaRecurso.addEventListener("click", () => {
    ativaRecursoSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    addRecursoSection.classList.add("hidden");
    removeRecursoSection.classList.add("hidden");
    desativaRecursoSection.classList.add("hidden");
  });

  // Desativar recurso
  btnDesativaRecurso.addEventListener("click", () => {
    desativaRecursoSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    addRecursoSection.classList.add("hidden");
    removeRecursoSection.classList.add("hidden");
    ativaRecursoSection.classList.add("hidden");
  });

  // Voltar ao menu principal
  document.querySelectorAll(".btnVoltar").forEach((btn) => {
    btn.addEventListener("click", () => {
      menuConfig.classList.remove("hidden");
      addRecursoSection.classList.add("hidden");
      removeRecursoSection.classList.add("hidden");
      ativaRecursoSection.classList.add("hidden");
      desativaRecursoSection.classList.add("hidden");
    });
  });


});
