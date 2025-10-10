const token = 'meu_token';
const host = window.location.host === '' ? 'localhost:8000' : window.location.host;
const protocol = window.location.protocol === 'file:' ? 'http:' : window.location.protocol;
const apiUrl =  `${protocol}//${host}/api`;

async function getRecursos(){
  const url = `${apiUrl}/recursos?token=${token}`
  const allRecursos = await fetch(url)
                    .then(response => response.json())
                    .catch(error => alert('Erro ao buscar cameras'))
  return allRecursos;
};

async function startRecurso(id) {
  const url = `${apiUrl}/video/${id}?token=${token}`;

  const img = document.createElement('img');
  img.id = "video"+id;
  img.width = 320;
  img.height = 240;
  img.src = url;
  document.body.appendChild(img);
};

async function init() {
  recursos = await getRecursos()
  recursos.forEach( startRecurso );
};

init()