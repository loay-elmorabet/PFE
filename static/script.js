const saisonSelect = document.getElementById("saison-select");
const ligueSelect = document.getElementById("ligue");
const equipeSelect = document.getElementById("equipe");
const joueurSelect = document.getElementById("joueur");

saisonSelect.addEventListener("change", function () {
  const yearSelect = saisonSelect.value;
  if (yearSelect === "") {
    ligueSelect.innerHTML = '<option value="">choisir une ligue</option>';
    ligueSelect.disabled = true;
  }
  fetch(`/api/leagues?season=${yearSelect}`)
    .then((response) => response.json())
    .then((ligues) => {
      ligueSelect.innerHTML = '<option value="">choisir une ligue</option>';
      ligues.forEach((ligue) => {
        const idligue = ligue[0];
        const nomligue = ligue[1];

        const option = document.createElement("option");
        option.value = idligue;
        option.textContent = nomligue;

        ligueSelect.appendChild(option);
      });
      ligueSelect.disabled = false;
    })
    .catch((error) => console.error("erreur récupération des ligues", error));
});

ligueSelect.addEventListener("change", function () {
  const yearSelect = saisonSelect.value;
  const leagueId = ligueSelect.value;
  if (yearSelect === "" || leagueId === "") {
    equipeSelect.innerHTML = '<option value="">choisir une equipe</option>';
    equipeSelect.disabled = true;
  }
  fetch(`/api/leagues/teams?season=${yearSelect}&league=${leagueId}`)
    .then((response) => response.json())
    .then((equipes) => {
      equipeSelect.innerHTML = '<option value="">choisir une equipe</option>';
      equipes.forEach((equipe) => {
        const idequipe = equipe[0];
        const nomequipe = equipe[1];

        const option = document.createElement("option");
        option.value = idequipe;
        option.textContent = nomequipe;

        equipeSelect.appendChild(option);
      });
      equipeSelect.disabled = false;
    })
    .catch((error) => console.error("erreur récupération des equipes", error));
});

equipeSelect.addEventListener("change", function () {
  const yearSelect = saisonSelect.value;
  const leagueId = ligueSelect.value;
  const teamId = equipeSelect.value;
  if (yearSelect === "" || leagueId === "" || teamId === "") {
    joueurSelect.innerHTML = '<option value="">choisir un joueur</option>';
    joueurSelect.disabled = true;
  }
  fetch(
    `/api/leagues/teams/players?season=${yearSelect}&league=${leagueId}&team=${teamId}`,
  )
    .then((response) => response.json())
    .then((joueurs) => {
      joueurSelect.innerHTML = '<option value="">choisir un joueur</option>';
      joueurs.forEach((joueur) => {
        const idjoueur = joueur[0];
        const nomjoueur = joueur[1];

        const option = document.createElement("option");
        option.value = idjoueur;
        option.textContent = nomjoueur;

        joueurSelect.appendChild(option);
      });
      joueurSelect.disabled = false;
    })
    .catch((error) => console.error("erreur récupération des joueurs", error));
});
