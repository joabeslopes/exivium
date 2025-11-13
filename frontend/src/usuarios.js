if (!token){
  window.location.href = "login.html";
};

let usuarios = {};

function preencheOptionsUsuarios(element){
  const usuarioList = element.querySelector('[name="UsuarioList"]');

  usuarioList.innerHTML = "";
  for (const [id, usuario] of Object.entries(usuarios)){
    const option = document.createElement("option");
    option.value = id;
    option.textContent = usuario.nome;
    usuarioList.appendChild(option);
  };
};

async function criaUsuario(event) {
  event.preventDefault();

  const nome = document.getElementById("UsuarioNome");
  const telefone = document.getElementById("UsuarioTelefone");
  const email = document.getElementById("UsuarioEmail");
  const senha = document.getElementById("UsuarioSenha");

  const request = {
    "token": token,
    "nome": nome.value,
    "telefone": telefone.value,
    "email": email.value,
    "senha": senha.value
  };

  const newId = await post("/usuario", request);

  if (newId){

    if (usuarios[newId]){
      alert("Usuario já foi criado");
    } else {
      usuarios[newId] = {
        "nome": request.nome
      };
      nome.value = "";
      telefone.value = "";
      email.value = "";
      senha.value = "";
      alert("Sucesso");
    };

  } else {
    alert("Erro ao criar Usuario");
  };

};

async function removeUsuario(event) {
  event.preventDefault();

  const removeUsuarioSection = document.getElementById("removeUsuarioSection");
  const removeUsuarioList = removeUsuarioSection.querySelector('[name="UsuarioList"]');
  const id = removeUsuarioList.value;

  if (usuarios[id]){
    const deleted = await del(`/usuario/${id}`);

    if (deleted){
      delete usuarios[id]
      preencheOptionsUsuarios(removeUsuarioSection);
      alert("Sucesso");
    } else {
      alert("Erro ao deletar Usuario");
    };
  } else {
    alert("Não existe Usuario com esse ID")
  };

};

// Garante que o código só roda depois que o DOM estiver pronto
document.addEventListener("DOMContentLoaded", async () => {

  const usuariosAtuais = await get("/usuarios");
  if (usuariosAtuais){
    for (const u of usuariosAtuais){
      const id = u.id;
      delete u.id;
      usuarios[id] = u;
    };
  };

  // Seletores principais
  const menuConfig = document.getElementById("menuConfig");
  const addUsuarioSection = document.getElementById("addUsuarioSection");
  const removeUsuarioSection = document.getElementById("removeUsuarioSection");

  // Botões
  const btnAddUsuario = document.getElementById("btnAddUsuario");
  const btnRemoveUsuario = document.getElementById("btnRemoveUsuario");
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


  // Adicionar Usuario
  btnAddUsuario.addEventListener("click", () => {
    addUsuarioSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    removeUsuarioSection.classList.add("hidden");
  });

  // Remover Usuario
  btnRemoveUsuario.addEventListener("click", () => {
    removeUsuarioSection.classList.remove("hidden");
    menuConfig.classList.add("hidden");
    addUsuarioSection.classList.add("hidden");

    preencheOptionsUsuarios(removeUsuarioSection);
  });

  // Voltar ao menu principal
  document.querySelectorAll(".btnVoltar").forEach((btn) => {
    btn.addEventListener("click", () => {
      menuConfig.classList.remove("hidden");
      addUsuarioSection.classList.add("hidden");
      removeUsuarioSection.classList.add("hidden");
    });
  });


});
