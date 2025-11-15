if (!token){
  window.location.href = "login.html";
};

// Seleção de elementos
const cameraCountSelect = document.getElementById('cameraCount');
const header = document.querySelector('header');
const cameraGrid = document.querySelector('.camera-grid');
const logoutBtn = document.getElementById('logoutBtn');
const voltarBtn = document.getElementById('voltarBtn');

var STREAM_CAMERAS = [];

async function getRecursos(){

  const allRecursos = await get('/ativos');

  if (allRecursos){
    STREAM_CAMERAS = Object.keys(allRecursos);
  };

};

// Função para atualizar o número de câmeras visíveis
function updateCameraDisplay(count) {
  cameraGrid.setAttribute('data-camera-count', count);
  
  // Salvar preferência no localStorage
  localStorage.setItem('cameraCount', count);
  
  console.log(`Exibindo ${count} câmera(s)`);
  
  // Recarrega os streams para as câmeras visíveis
  loadCameraStreams(count);
}

// Função para carregar stream de câmera (adaptada para MJPEG)
function loadCameraStreams(visibleCount) {
  const allCameraCards = document.querySelectorAll('.camera-card');
  
  allCameraCards.forEach((card, index) => {
    const videoElement = card.querySelector('img');
    const statusIndicator = card.querySelector('.status-indicator');

    // Se a câmera estiver visível
    if (index <= visibleCount) {

      const cameraNumber = STREAM_CAMERAS[index];

      if (cameraNumber) {

        videoElement.src = `${apiUrl}/video/${cameraNumber}?token=${token}`;
        videoElement.style.display = 'block';
        statusIndicator.classList.remove('offline');
        statusIndicator.classList.add('online');

        // Adicionar um listener para detectar falha no carregamento (simulando offline)
        videoElement.onerror = () => {
          console.error(`Falha ao carregar stream da Câmera ${cameraNumber}`);
          videoElement.style.display = 'none';
          statusIndicator.classList.remove('online');
          statusIndicator.classList.add('offline');
         
        };

      } else {
        console.warn(`URL de stream não definida para a câmera ${index}`);
        videoElement.src = '';
        videoElement.style.display = 'none';
        statusIndicator.classList.remove('online');
        statusIndicator.classList.add('offline');
      }
      
    } else {
      videoElement.src = '';
      videoElement.style.display = 'none';
      statusIndicator.classList.remove('online', 'offline');
    }
  });
}

// --- Funções de Controle ---

// Função para alternar o modo tela cheia no container da câmera
function handleFullscreen(event) {
  const cameraCard = event.currentTarget.closest('.camera-card'); // toda a câmera
  const isFullscreen =
    document.fullscreenElement === cameraCard ||
    document.mozFullScreenElement === cameraCard ||
    document.webkitFullscreenElement === cameraCard ||
    document.msFullscreenElement === cameraCard;

  if (isFullscreen) {
    // Sai do modo tela cheia
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  } else {
    // Entra em tela cheia apenas a câmera selecionada
    if (cameraCard.requestFullscreen) {
      cameraCard.requestFullscreen();
    } else if (cameraCard.mozRequestFullScreen) {
      cameraCard.mozRequestFullScreen();
    } else if (cameraCard.webkitRequestFullscreen) {
      cameraCard.webkitRequestFullscreen();
    } else if (cameraCard.msRequestFullscreen) {
      cameraCard.msRequestFullscreen();
    }
  }
}


// Carregar ao iniciar a página
window.addEventListener('DOMContentLoaded', async () => {

  await getRecursos();
  const savedCount = localStorage.getItem('cameraCount');

  // Listener para gerenciar a visibilidade do cabeçalho
  document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement) {
      // Entrou em tela cheia
      header.classList.add('hidden-on-fullscreen');
    } else {
      // Saiu de tela cheia
      header.classList.remove('hidden-on-fullscreen');
    }
  });

  // Event listener para mudança no select
  cameraCountSelect.addEventListener('change', (e) => {
    const selectedCount = parseInt(e.target.value);
    updateCameraDisplay(selectedCount);
  });

  if (savedCount) {
    cameraCountSelect.value = savedCount;
    updateCameraDisplay(parseInt(savedCount));
  } else {
    // Usar o valor padrão do select (4 câmeras)
    updateCameraDisplay(parseInt(cameraCountSelect.value));
  }
  
  // Adicionar listeners aos botões de controle
  document.querySelectorAll('.btn-fullscreen').forEach(button => {
    button.addEventListener('click', handleFullscreen);
  });

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

  // Função de voltar
  voltarBtn.addEventListener('click', () => {
    window.location.href = 'index.html';
  });

});