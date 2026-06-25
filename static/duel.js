const saisonP1 = document.getElementById("saison-p1");
const ligueP1 = document.getElementById("ligue-p1");
const equipeP1 = document.getElementById("equipe-p1");
const joueurP1 = document.getElementById("joueur-p1");

saisonP1.addEventListener("change", function () {
  const yearSelect = saisonP1.value;
  if (yearSelect === "") {
    ligueP1.innerHTML = '<option value="">choisir une ligue</option>';
    ligueP1.disabled = true;
  }
  fetch(`/api/leagues?season=${yearSelect}`)
    .then((response) => response.json())
    .then((ligues) => {
      ligueP1.innerHTML = '<option value="">choisir une ligue</option>';
      ligues.forEach((ligue) => {
        const option = document.createElement("option");
        option.value = ligue[0];
        option.textContent = ligue[1];
        ligueP1.appendChild(option);
      });
      ligueP1.disabled = false;
    })
    .catch((error) =>
      console.error("erreur récupération des ligues J1", error),
    );
});

ligueP1.addEventListener("change", function () {
  const yearSelect = saisonP1.value;
  const leagueId = ligueP1.value;
  if (yearSelect === "" || leagueId === "") {
    equipeP1.innerHTML = '<option value="">choisir une equipe</option>';
    equipeP1.disabled = true;
  }
  fetch(`/api/leagues/teams?season=${yearSelect}&league=${leagueId}`)
    .then((response) => response.json())
    .then((equipes) => {
      equipeP1.innerHTML = '<option value="">choisir une equipe</option>';
      equipes.forEach((equipe) => {
        const option = document.createElement("option");
        option.value = equipe[0];
        option.textContent = equipe[1];
        equipeP1.appendChild(option);
      });
      equipeP1.disabled = false;
    })
    .catch((error) =>
      console.error("erreur récupération des equipes J1", error),
    );
});

equipeP1.addEventListener("change", function () {
  const yearSelect = saisonP1.value;
  const leagueId = ligueP1.value;
  const teamId = equipeP1.value;

  if (yearSelect === "" || leagueId === "" || teamId === "") {
    joueurP1.innerHTML = '<option value="">choisir un joueur</option>';
    joueurP1.disabled = true;
    return;
  }
  fetch(
    `/api/leagues/teams/players?season=${yearSelect}&league=${leagueId}&team=${teamId}`,
  )
    .then((response) => response.json())
    .then((joueurs) => {
      joueurP1.innerHTML = '<option value="">choisir un joueur</option>';
      joueurs.forEach((joueur) => {
        const option = document.createElement("option");
        option.value = joueur[0];
        option.textContent = joueur[1];
        joueurP1.appendChild(option);
      });
      joueurP1.disabled = false;
    })
    .catch((error) =>
      console.error("erreur récupération des joueurs J1", error),
    );
});
//###############################################################################""
const saisonP2 = document.getElementById("saison-p2");
const ligueP2 = document.getElementById("ligue-p2");
const equipeP2 = document.getElementById("equipe-p2");
const joueurP2 = document.getElementById("joueur-p2");

saisonP2.addEventListener("change", function () {
  const yearSelect = saisonP2.value;
  if (yearSelect === "") {
    ligueP2.innerHTML = '<option value="">choisir une ligue</option>';
    ligueP2.disabled = true;
  }
  fetch(`/api/leagues?season=${yearSelect}`)
    .then((response) => response.json())
    .then((ligues) => {
      ligueP2.innerHTML = '<option value="">choisir une ligue</option>';
      ligues.forEach((ligue) => {
        const option = document.createElement("option");
        option.value = ligue[0];
        option.textContent = ligue[1];
        ligueP2.appendChild(option);
      });
      ligueP2.disabled = false;
    })
    .catch((error) =>
      console.error("erreur récupération des ligues J2", error),
    );
});

ligueP2.addEventListener("change", function () {
  const yearSelect = saisonP2.value;
  const leagueId = ligueP2.value;
  if (yearSelect === "" || leagueId === "") {
    equipeP2.innerHTML = '<option value="">choisir une equipe</option>';
    equipeP2.disabled = true;
  }
  fetch(`/api/leagues/teams?season=${yearSelect}&league=${leagueId}`)
    .then((response) => response.json())
    .then((equipes) => {
      equipeP2.innerHTML = '<option value="">choisir une equipe</option>';
      equipes.forEach((equipe) => {
        const option = document.createElement("option");
        option.value = equipe[0];
        option.textContent = equipe[1];
        equipeP2.appendChild(option);
      });
      equipeP2.disabled = false;
    })
    .catch((error) =>
      console.error("erreur récupération des equipes J2", error),
    );
});

equipeP2.addEventListener("change", function () {
  const yearSelect = saisonP2.value;
  const leagueId = ligueP2.value;
  const teamId = equipeP2.value;

  if (yearSelect === "" || leagueId === "" || teamId === "") {
    joueurP2.innerHTML = '<option value="">choisir un joueur</option>';
    joueurP2.disabled = true;
    return;
  }
  fetch(
    `/api/leagues/teams/players?season=${yearSelect}&league=${leagueId}&team=${teamId}`,
  )
    .then((response) => response.json())
    .then((joueurs) => {
      joueurP2.innerHTML = '<option value="">choisir un joueur</option>';
      joueurs.forEach((joueur) => {
        const option = document.createElement("option");
        option.value = joueur[0];
        option.textContent = joueur[1];
        joueurP2.appendChild(option);
      });
      joueurP2.disabled = false;
    })
    .catch((error) =>
      console.error("erreur récupération des joueurs J2", error),
    );
});
