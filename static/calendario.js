// Nomes dos meses em português ja que não tem necessidade em inglês, pra mostrar no topo do calendário
const NOMES_MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

// Controla qual mês/ano está sendo exibido 
let dataAtual = new Date();
let mesExibido = dataAtual.getMonth();
let anoExibido = dataAtual.getFullYear();

function desenharCalendario() {
    const container = document.getElementById('calendario-dias');
    const titulo = document.getElementById('mes-atual');
    container.innerHTML = '';
    titulo.textContent = `${NOMES_MESES[mesExibido]} de ${anoExibido}`;

    const primeiroDiaSemana = new Date(anoExibido, mesExibido, 1).getDay();
    const totalDiasNoMes = new Date(anoExibido, mesExibido + 1, 0).getDate();

    // Espaços vazios antes do dia 1, pra alinhar com o dia da semana certo pra deixar mais "orgnizdinho"
    for (let i = 0; i < primeiroDiaSemana; i++) {
        const vazio = document.createElement('span');
        vazio.className = 'dia vazio';
        container.appendChild(vazio);
    }

    for (let dia = 1; dia <= totalDiasNoMes; dia++) {
        const celula = document.createElement('span');
        celula.className = 'dia';
        celula.textContent = dia;

        // Monta a data no formato "AAAA-MM-DD" pra comparar com o que veio do banco
        const mesFormatado = String(mesExibido + 1).padStart(2, '0');
        const diaFormatado = String(dia).padStart(2, '0');
        const dataFormatada = `${anoExibido}-${mesFormatado}-${diaFormatado}`;

        const evento = datasOcupadas.find(e => e.data === dataFormatada);
        if (evento) {
            celula.classList.add('ocupado');
            celula.title = evento.titulo; // aparece como dica ao passar o mouse
        }

        // Destaca o dia de hoje
        const hoje = new Date();
        if (dia === hoje.getDate() && mesExibido === hoje.getMonth() && anoExibido === hoje.getFullYear()) {
            celula.classList.add('hoje');
        }

        container.appendChild(celula);
    }
}

document.getElementById('mes-anterior').addEventListener('click', () => {
    mesExibido--;
    if (mesExibido < 0) {
        mesExibido = 11;
        anoExibido--;
    }
    desenharCalendario();
});

document.getElementById('mes-seguinte').addEventListener('click', () => {
    mesExibido++;
    if (mesExibido > 11) {
        mesExibido = 0;
        anoExibido++;
    }
    desenharCalendario();
});

desenharCalendario();
