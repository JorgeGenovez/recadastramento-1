function convertToBase64() {
    const fileInput = document.getElementById('fileInput').files[0];
    
    if (!fileInput) {
        alert("Por favor, selecione uma imagem primeiro.");
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = function(event) {
        const base64String = event.target.result;
        document.getElementById('output').value = base64String;
    };
    
    reader.readAsDataURL(fileInput);
}
const app = Vue.createApp({
    data() {
        return {
            opcoes_membros: [],
            socket: null,
            membro: {},
            guia_atual: 'formulario'
        }
    },
    methods: {
        voltaropcao(){
            window.location.href = `opcoes.html`
        },
        carregarMembro() {
            const membroData = localStorage.getItem('membro');
            if (membroData) {
                this.membro = JSON.parse(membroData);
                console.log(this.membro);
            }
        },
        async salvar_membro() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];

            if (!file) {
                alert("Por favor, selecione uma foto.");
                return;
            }

            const formData = new FormData();
            formData.append("foto", file);
            formData.append("matricula", document.getElementsByName('matricula')[0].value);
            formData.append("nome_completo", document.getElementsByName('nome_completo')[0].value);
            formData.append("data_de_nascimento", document.getElementsByName('data_de_nascimento')[0].value)
            formData.append("tipo_sanguineo", document.getElementsByName('tipo_sanguineo')[0].value)
            formData.append("naturalidade", document.getElementsByName('naturalidade')[0].value)
            formData.append("nacionalidade", document.getElementsByName('nacionalidade')[0].value)
            formData.append("cargo_atual", document.getElementsByName('cargo_atual')[0].value)
            formData.append("email", document.getElementsByName('email')[0].value)
            formData.append("telefone_residencial", document.getElementsByName('telefone_residencial')[0].value)
            formData.append("telefone_celular", document.getElementsByName('telefone_celular')[0].value)
            formData.append("cep", document.getElementsByName('cep')[0].value)
            formData.append("estado", document.getElementsByName('estado')[0].value)
            formData.append("cidade", document.getElementsByName('cidade')[0].value)
            formData.append("bairro", document.getElementsByName('bairro')[0].value)
            formData.append("rua", document.getElementsByName('rua')[0].value)
            formData.append("complemento", document.getElementsByName('complemento')[0].value)
            formData.append("data_de_batismo", document.getElementsByName('data_de_batismo')[0].value)
            formData.append("igreja_de_batismo", document.getElementsByName('igreja_de_batismo')[0].value)
            formData.append("bairro_da_igreja_de_batismo", document.getElementsByName('bairro_da_igreja_de_batismo')[0].value)
            formData.append("data_em_que_virou_membro", document.getElementsByName('data_em_que_virou_membro')[0].value)
            formData.append("modo", document.getElementsByName('modo')[0].value)
            formData.append("pai_eh_membro", document.getElementsByName('pai_eh_membro')[0].value)
            formData.append("nome_do_pai", document.getElementsByName('nome_do_pai')[0].value)
            formData.append("mae_eh_membro", document.getElementsByName('mae_eh_membro')[0].value)
            formData.append("nome_mae", document.getElementsByName('nome_mae')[0].value)
            formData.append("estado_civil", document.getElementsByName('estado_civil')[0].value)
            formData.append("conjuge_eh_membro", document.getElementsByName('conjuge_eh_membro')[0].value)
            formData.append("nome_conjuge", document.getElementsByName('nome_conjuge')[0].value)
            formData.append("data_de_nascimento_do_conjuge", document.getElementsByName('data_de_nascimento_do_conjuge')[0].value)
            formData.append("data_de_casamento", document.getElementsByName('data_de_casamento')[0].value)
            formData.append("nome_do_filho1", document.getElementsByName('nome_do_filho1')[0].value)
            formData.append("filho1_eh_membro", document.getElementsByName('filho1_eh_membro')[0].value)
            formData.append("data_de_nascimento_do_filho1", document.getElementsByName('data_de_nascimento_do_filho1')[0].value)
            formData.append("nome_do_filho2", document.getElementsByName('nome_do_filho2')[0].value)
            formData.append("filho2_eh_membro", document.getElementsByName('filho2_eh_membro')[0].value)
            formData.append("data_de_nascimento_do_filho2", document.getElementsByName('data_de_nascimento_do_filho2')[0].value)
            formData.append("nome_do_filho3", document.getElementsByName('nome_do_filho3')[0].value)
            formData.append("filho3_eh_membro", document.getElementsByName('filho3_eh_membro')[0].value)
            formData.append("data_de_nascimento_do_filho3", document.getElementsByName('data_de_nascimento_do_filho3')[0].value)
            formData.append("nome_do_filho4", document.getElementsByName('nome_do_filho4')[0].value)
            formData.append("filho4_eh_membro", document.getElementsByName('filho4_eh_membro')[0].value)
            formData.append("data_de_nascimento_do_filho4", document.getElementsByName('data_de_nascimento_do_filho4')[0].value)
            formData.append("nome_do_filho5", document.getElementsByName('nome_do_filho5')[0].value)
            formData.append("filho5_eh_membro", document.getElementsByName('filho5_eh_membro')[0].value)
            formData.append("data_de_nascimento_do_filho5", document.getElementsByName('data_de_nascimento_do_filho5')[0].value)

            this.guia_atual = 'tela_de_load'
            const promise = await fetch('http://localhost:8025/salvar_membro', {
                method: 'POST',
                body: formData,
                headers: {
                    "Authorization": `Bearer ${localStorage.token}`,
                }
            });
            const response = await promise.json()
            this.formData = response
            window.location.href = `opcoes.html`
        },
        async consultar_cep()
        {
            const promise = await fetch(`http://localhost:8025/consultar_cep`, {
                method: 'POST',
                body: new URLSearchParams({
                    cep: document.getElementsByName('cep')[0].value
                }),
                headers: {
                    "Authorization": `Bearer ${localStorage.token}`,
                }
            })
            const resp = await promise.json()
            "cep", document.getElementsByName('cep')[0].value = resp.cep
            "estado", document.getElementsByName('estado')[0].value = resp.estado
            "cidade", document.getElementsByName('cidade')[0].value = resp.localidade
            "bairro", document.getElementsByName('bairro')[0].value = resp.bairro
            "rua", document.getElementsByName('rua')[0].value = resp.logradouro
            console.log(resp)
        }
    },
    mounted() {
        const socket = io("http://localhost:8025", {
            query: { token: localStorage.token }
        });

        socket.on("connect", () => {
            console.log("Conexão estabelecida com sucesso.");
        });

        socket.on("sugestoes", (sugestoes) => {
            this.opcoes_membros = sugestoes;
        });

        this.socket = socket;

        // Carregar dados do membro ao montar o componente
        //this.carregarMembro();
    },
    
});

const appVM = app.mount('#conteiner');