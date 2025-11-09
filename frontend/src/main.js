// Seleção de elementos
const cameraCountSelect = document.getElementById('cameraCount');
const header = document.querySelector('header');
const cameraGrid = document.querySelector('.camera-grid');
const logoutBtn = document.getElementById('logoutBtn');

// URLs de exemplo para simular o streaming MJPEG
// ATENÇÃO: Substitua estas URLs pelas URLs reais do seu back-end Python
const STREAM_URLS = {
  1: "http://localhost:5000/camera/0", // Exemplo de URL de stream MJPEG
  2: "http://localhost:5000/camera/1",
  3: "http://localhost:5000/camera/2",
  4: "http://localhost:5000/camera/3",
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
    const cameraNumber = index + 1;
    const videoElement = card.querySelector('img');
    const statusIndicator = card.querySelector('.status-indicator');
    
    // Se a câmera estiver visível
    if (cameraNumber <= visibleCount) {
 
      
      const streamUrl = STREAM_URLS[cameraNumber];
      
      if (streamUrl) {
        
        videoElement.src = streamUrl;
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
        console.warn(`URL de stream não definida para a Câmera ${cameraNumber}`);
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

// Carregar preferência salva ao iniciar a página
window.addEventListener('DOMContentLoaded', () => {
  const savedCount = localStorage.getItem('cameraCount');
  
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
  

});

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
