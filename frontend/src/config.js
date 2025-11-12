if (!token){
  window.location.href = "login.html";
};

let recursos = {};
let ativos = [];

function preencheOptionsRecursos(element){
  const removeRecursoList = element.querySelector('[name="RecursoList"]');

  removeRecursoList.innerHTML = "";
  for (const [id, recurso] of Object.entries(recursos)){
    const option = document.createElement("option");
    option.value = id;
    option.textContent = recurso.nome;
    removeRecursoList.appendChild(option);
  };
};

function preencheOptionsAtivos(element){
  const desativaRecursoList = element.querySelector('[name="RecursoList"]');

  desativaRecursoList.innerHTML = "";
  for (const id of ativos){
    const option = document.createElement("option");
    option.value = id;
    option.textContent = id;
    desativaRecursoList.appendChild(option);
  };
};

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

  const newId = await post("/recurso", request);

  if (newId){

    if (recursos[newId]){
      alert("Recurso já foi criado");
    } else {
      recursos[newId] = {
        "nome": request.nome
      };
      nome.value = "";
      gitRepo.value = "";
      alert("Sucesso");
    };

  } else {
    alert("Erro ao criar recurso");
  };

};

async function removeRecurso(event) {
  event.preventDefault();

  const removeRecursoSection = document.getElementById("removeRecursoSection");
  const removeRecursoList = removeRecursoSection.querySelector('[name="RecursoList"]');
  const id = removeRecursoList.value;

  if (recursos[id]){
    const deleted = await del(`/recurso/${id}`);

    if (deleted){
      delete recursos[id]
      preencheOptionsRecursos(removeRecursoSection);
      alert("Sucesso");
    } else {
      alert("Erro ao deletar recurso");
    };
  } else {
    alert("Não existe recurso com esse ID")
  };

};

async function ativaRecurso(event) {
  event.preventDefault();

  const ativaRecursoSection = document.getElementById("ativaRecursoSection");
  const ativaRecursoList = ativaRecursoSection.querySelector('[name="RecursoList"]');
  const id = ativaRecursoList.value;
  const alvo = document.getElementById("RecursoAlvo");  

  const request = {
    "token": token,
    "recurso_id": id,
    "recurso_alvo": alvo.value
  };

  const newId = await post("/ativo", request);

  if (newId){

    if (!ativos.includes(newId)){
      ativos.push(newId);
      alvo.value = "";
      alert("Sucesso");
    } else {
      alert("Recurso já foi ativado");
    };

  } else {
    alert("Erro ao criar recurso");
  };

};

async function desativaRecurso(event) {
  event.preventDefault();

  const desativaRecursoSection = document.getElementById("desativaRecursoSection");
  const desativaRecursoList = desativaRecursoSection.querySelector('[name="RecursoList"]');
  const id = desativaRecursoList.value;

  const deleted = await del(`/ativo/${id}`);

  if (deleted){
    ativos = ativos.filter( (ativoId) => ativoId != id );
    preencheOptionsAtivos(desativaRecursoSection);
    alert("Sucesso");
  } else {
    alert("Erro ao criar recurso");
  };
};

// Garante que o código só roda depois que o DOM estiver pronto
document.addEventListener("DOMContentLoaded", async () => {

  const ativosAtuais = await get("/ativos");
  if (ativosAtuais){
    ativos = ativosAtuais;
  };

  const recursosAtuais = await get("/recursos");
  if (recursosAtuais){
    recursos = recursosAtuais;
  };

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

    preencheOptionsRecursos(removeRecursoSection);
  });

  // Ativar recurso
  btnAtivaRecurso.addEventListener("click", () => {
    ativaRecursoSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    addRecursoSection.classList.add("hidden");
    removeRecursoSection.classList.add("hidden");
    desativaRecursoSection.classList.add("hidden");

    preencheOptionsRecursos(ativaRecursoSection);
  });

  // Desativar recurso
  btnDesativaRecurso.addEventListener("click", () => {
    desativaRecursoSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    addRecursoSection.classList.add("hidden");
    removeRecursoSection.classList.add("hidden");
    ativaRecursoSection.classList.add("hidden");

    preencheOptionsAtivos(desativaRecursoSection);
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
