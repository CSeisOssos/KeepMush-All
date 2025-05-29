document.addEventListener('DOMContentLoaded', function() {
  // Controle da barra de pesquisa
  const searchBtn = document.getElementById('searchBtn');
  const searchBar = document.getElementById('searchBar');
  
  searchBtn.addEventListener('click', function(e) {
    e.preventDefault();
    searchBar.classList.toggle('d-none');
  });

  // Modal de informações
  const infoBtn = document.getElementById('infoBtn');
  infoBtn.addEventListener('click', function(e) {
    e.preventDefault();
    const infoModal = new bootstrap.Modal(document.getElementById('infoModal'));
    infoModal.show();
  });



  // Função para renderizar os cogumelos
  function renderMushrooms() {
    const container = document.getElementById('mushroomsContainer');
    container.innerHTML = '';

    mushrooms.forEach(mushroom => {
      const col = document.createElement('div');
      col.className = 'col-md-6 col-lg-4 mb-4';
      
      const card = document.createElement('div');
      card.className = 'card mushroom-card h-100';
      
      const badgeConfig = {
        edible: { icon: 'bi-egg-fried', class: 'edible-badge', tooltip: 'Comestível' },
        poisonous: { icon: 'bi-exclamation-triangle', class: 'poisonous-badge', tooltip: 'Venenoso' },
        psychoactive: { icon: 'bi-activity', class: 'psychoactive-badge', tooltip: 'Psicoativo' },
        inedible: { icon: 'bi-slash-circle', class: 'inedible-badge', tooltip: 'Não comestível' }
      };

      const type = mushroom.type in badgeConfig ? mushroom.type : 'inedible';
      const { icon, class: badgeClass, tooltip } = badgeConfig[type];

      // Cria o elemento do ícone separadamente
      const badgeIcon = document.createElement('i');
      badgeIcon.className = `bi ${icon} mushroom-badge ${badgeClass}`;
      badgeIcon.setAttribute('data-bs-toggle', 'tooltip');
      badgeIcon.setAttribute('data-bs-placement', 'top');
      badgeIcon.setAttribute('title', tooltip);
      
      // Cria o botão de detalhes com evento diretamente
      const detailsButton = document.createElement('button');
      detailsButton.className = 'btn btn-success btn-sm view-details';
      detailsButton.setAttribute('data-id', mushroom.id);
      detailsButton.textContent = 'Ver detalhes';
      detailsButton.addEventListener('click', () => showMushroomDetails(mushroom.id));
      
      // Conteúdo do card
      card.innerHTML = `
        <img src="${mushroom.image}" class="card-img-top mushroom-img" alt="${mushroom.name}" loading="lazy">
        <div class="card-body">
          <h5 class="card-title mushroom-title">${mushroom.name}</h5>
          <p class="card-text">
            <strong>Família:</strong> ${mushroom.family}<br>
            <strong>Gênero:</strong> ${mushroom.genus}
          </p>
        </div>
      `;

      // Adiciona o botão e o ícone manualmente
      card.querySelector('.card-body').appendChild(detailsButton);
      card.appendChild(badgeIcon);
      col.appendChild(card);
      container.appendChild(col);
    });

    // Inicializa tooltips
    initTooltips();
  }

  function initTooltips() {
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl);
      });
    } else {
      console.warn('Bootstrap Tooltip não está disponível');
    }
  }

  function getBadgeTitle(type) {
    switch(type) {
      case 'edible': 
        return '<span class="badge edible-badge">Comestível</span>';
      case 'poisonous': 
        return '<span class="badge poisonous-badge">Venenoso</span>';
      case 'psychoactive': 
        return '<span class="badge psychoactive-badge">Psicoativo</span>';
      default: 
        return '<span class="badge inedible-badge">Não comestível</span>';
    }
  }

  // Função para mostrar detalhes do cogumelo no modal
  function showMushroomDetails(id) {
    const mushroom = mushrooms.find(m => m.id === id);
    if (!mushroom) return;
    
    const modal = new bootstrap.Modal(document.getElementById('mushroomModal'));
    document.getElementById('mushroomModalTitle').textContent = mushroom.name;
    document.getElementById('mushroomModalImage').src = mushroom.image;
    document.getElementById('mushroomModalImage').alt = mushroom.name;
    
    const modalContent = document.getElementById('mushroomModalContent');
    
    // Cria o conteúdo do modal de forma dinâmica
    let contentHTML = `
      <div class="row">
        <div class="col-md-6">
          <p><strong>Reino:</strong> ${mushroom.kingdom}</p>
          <p><strong>Divisão:</strong> ${mushroom.division}</p>
          <p><strong>Classe:</strong> ${mushroom.class}</p>
          <p><strong>Ordem:</strong> ${mushroom.order}</p>
        </div>
        <div class="col-md-6">
          <p><strong>Família:</strong> ${mushroom.family}</p>
          <p><strong>Gênero:</strong> ${mushroom.genus}</p>
          <p><strong>Espécie:</strong> ${mushroom.species}</p>
          <p><strong>Tipo:</strong> ${getBadgeTitle(mushroom.type)}</p>
        </div>
      </div>
      <hr>
      <div class="mushroom-description">
        ${formatDescription(mushroom.description)}
      </div>
      ${getWarningText(mushroom.type)}
    `;
   
    modalContent.innerHTML = contentHTML;
    modal.show();
  }

  // Função auxiliar para formatar a descrição com quebras de linha
  function formatDescription(desc) {
    return desc.split('\n').map(paragraph => {
      if (paragraph.trim().startsWith('Descrição') || 
          paragraph.trim().startsWith('Comestibilidade') ||
          paragraph.trim().startsWith('Habitat')) {
        return `<p class="fw-bold">${paragraph}</p>`;
      }
      return `<p>${paragraph}</p>`;
    }).join('');
  }

  // Função auxiliar para o texto de aviso
  function getWarningText(type) {
    if (type === 'poisonous') {
      return `
        <div class="alert alert-danger mt-3">
          <i class="bi bi-exclamation-triangle-fill"></i>
          ATENÇÃO: Este cogumelo é venenoso e não deve ser consumido em nenhuma circunstância.
        </div>
      `;
    } else if (type === 'edible') {
      return `
        <div class="alert alert-warning mt-3">
          <i class="bi bi-exclamation-triangle"></i>
          É crucial lembrar que a segurança alimentar deve ser priorizada, e qualquer consumo desse cogumelo deve ser realizado com cautela e conhecimento adequado.
        </div>
      `;
    }
    return '';
  }

  // Funções da Câmera
  let stream = null;

  document.querySelector('a[href="camera.html"]')?.addEventListener('click', function(e) {
    e.preventDefault();
    const cameraModal = new bootstrap.Modal(document.getElementById('cameraModal'));
    cameraModal.show();
  });

  document.getElementById('startCamera')?.addEventListener('click', startCamera);
  document.getElementById('capturePhoto')?.addEventListener('click', capturePhoto);
  document.getElementById('uploadBtn')?.addEventListener('click', () => document.getElementById('fileInput').click());
  document.getElementById('fileInput')?.addEventListener('change', handleFileUpload);
  document.getElementById('retryButton')?.addEventListener('click', resetCameraUI);
  document.getElementById('analyzeButton')?.addEventListener('click', analyzeImage);

  async function startCamera() {
    try {
      const video = document.getElementById('cameraPreview');
      const placeholder = document.getElementById('cameraPlaceholder');
      
      stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' }, 
        audio: false 
      });
      
      video.srcObject = stream;
      video.classList.remove('d-none');
      placeholder.classList.add('d-none');
      document.getElementById('capturePhoto').classList.remove('d-none');
      document.getElementById('startCamera').classList.add('d-none');
    } catch (err) {
      alert('Não foi possível acessar a câmera: ' + err.message);
    }
  }

  function capturePhoto() {
    const video = document.getElementById('cameraPreview');
    const canvas = document.getElementById('photoCanvas');
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    showImagePreview(canvas.toDataURL('image/jpeg'));
    stopCamera();
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      document.getElementById('cameraPreview').classList.add('d-none');
      document.getElementById('cameraPlaceholder').classList.remove('d-none');
    }
  }

  function handleFileUpload(e) {
    const file = e.target.files[0];
    if (file && file.type.match('image.*')) {
      const reader = new FileReader();
      reader.onload = (event) => showImagePreview(event.target.result);
      reader.readAsDataURL(file);
      document.getElementById('fileName').textContent = file.name;
    }
  }

  function showImagePreview(imageSrc) {
    const preview = document.getElementById('imagePreview');
    preview.src = imageSrc;
    document.getElementById('imagePreviewContainer').classList.remove('d-none');
  }

  function resetCameraUI() {
    document.getElementById('imagePreviewContainer').classList.add('d-none');
    document.getElementById('fileInput').value = '';
    document.getElementById('fileName').textContent = '';
    document.getElementById('startCamera').classList.remove('d-none');
  }

  async function analyzeImage() {
    const imageSrc = document.getElementById('imagePreview').src;
    
    bootstrap.Modal.getInstance(document.getElementById('cameraModal')).hide();
    const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
    resultModal.show();
    
    setTimeout(() => {
      document.getElementById('loadingAnalysis').classList.add('d-none');
      const resultContent = document.getElementById('resultContent');
      
      resultContent.innerHTML = `
        <div class="alert alert-success">
          <h4><i class="bi bi-check-circle"></i> Amanita muscaria</h4>
          <p>Identificado com 87% de confiança</p>
        </div>
        <div class="text-start mt-3">
          <p><strong>Características:</strong> Chapéu vermelho com manchas brancas</p>
          <p><strong>Tipo:</strong> <span class="badge bg-danger">Venenoso</span></p>
          <p class="alert alert-warning mt-3"><i class="bi bi-exclamation-triangle"></i> Este cogumelo é potencialmente perigoso. Não consuma.</p>
          <button class="btn btn-outline-success w-100 mt-2" onclick="window.location.href='#'">
            Ver detalhes completos
          </button>
        </div>
      `;
      resultContent.classList.remove('d-none');
    }, 3000);
  }

  // Inicializa a página
  renderMushrooms();

  // Verifica se o Bootstrap está carregado
  if (typeof bootstrap === 'undefined') {
    console.error('Bootstrap não carregado!');
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css';
    document.head.appendChild(link);
  }
});