document.addEventListener("DOMContentLoaded", async function () {
  const userId = localStorage.getItem("usuario_id");

  if (!userId) {
    alert("Usuário não logado.");
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch(`http://localhost:8000/api/usuarios/${userId}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Erro ao buscar dados.");
    }

    // Atualiza o conteúdo da página
    document.getElementById("profileName").textContent = data.nome;
    document.getElementById("profileEmail").textContent = data.email;
    document.getElementById("profileImage").textContent = data.foto;
    document.getElementById("avatarPreview").textContent = data.foto;

    // Atualizar o nível
    const ranque = data.ranque || 1;
    let nomeNivel = "Iniciante";
    let progresso = 10;

    if (ranque === 2) {
      nomeNivel = "Explorador Intermediário";
      progresso = 45;
    } else if (ranque >= 3) {
      nomeNivel = "Mestre Micólogo";
      progresso = 90;
    }

    document.getElementById("explorerLevel").textContent = nomeNivel;
    document.querySelector(".progress-bar").style.width = progresso + "%";
    document.querySelector(".progress-bar").setAttribute("aria-valuenow", progresso);

    // Exemplo de preenchimento estático das outras estatísticas
    document.getElementById("identifiedCount").textContent = "9"; // Substituir depois por dados reais

    // Se houver imagem de perfil
    if (data.foto) {
      const profileImg = document.getElementById("profileImage");
      if (profileImg) profileImg.src = `/uploads/avatars/${data.foto}`;
    }

    const preview = document.getElementById("avatarPreview");
    if (preview) {
    preview.src = `/uploads/avatars/${data.foto}`;
  }
}

    catch (err) {
    console.error(err);
    alert("Erro ao carregar o perfil.");
  }

// Abrir seletor de arquivo
document.getElementById("uploadPhotoBtn").addEventListener("click", function () {
  document.getElementById("avatarUpload").click();
});

// Mostrar preview da imagem
document.getElementById("avatarUpload").addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const preview = document.getElementById("avatarPreview");
    preview.src = URL.createObjectURL(file);
  }
});

// Salvar imagem enviada
document.getElementById("saveAvatarBtn").addEventListener("click", async function () {
  const fileInput = document.getElementById("avatarUpload");
  const file = fileInput.files[0];
  const userId = localStorage.getItem("usuario_id");

  if (!file || !userId) {
    alert("Selecione uma imagem válida.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`http://localhost:8000/api/usuarios/${userId}/foto`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById("profileImage").src = data.foto;
      document.getElementById("avatarPreview").src = data.foto;
      alert("Foto atualizada com sucesso!");
    } else {
      alert("Erro: " + (data.detail || "Erro ao enviar imagem."));
    }
  } catch (err) {
    console.error(err);
    alert("Erro ao conectar com o servidor.");
  }
});


}
);

