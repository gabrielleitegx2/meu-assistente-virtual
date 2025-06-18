async function enviarPergunta() {
    const input = document.getElementById('user-input');
    const mensagem = input.value.trim();
    if (!mensagem) return;

    adicionarMensagem('user', mensagem);
    input.value = '';

    try {
        const resposta = await fetch('http://127.0.0.1:8000/perguntar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mensagem })
        });

        const dados = await resposta.json();
        adicionarMensagem('bot', dados.resposta);
    } catch (erro) {
        adicionarMensagem('bot', 'Erro ao se comunicar com o servidor.');
    }
}

function adicionarMensagem(remetente, texto) {
    const log = document.getElementById('chat-log');
    const div = document.createElement('div');
    div.className = 'message ' + remetente;
    div.textContent = texto;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
}
