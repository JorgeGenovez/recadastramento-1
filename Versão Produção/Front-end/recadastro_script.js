const app = Vue.createApp({
    data() {
        return {
            opcoes_membros: [],
            socket: null,
            membro: {},
            guia_atual: 'tela_inicial'
        }
    },
    methods: {
        pesquisar_membros(content)
        {
            console.log(content)
            if (content == '') {
                this.opcoes_membros = []
                return
            }
            this.socket.emit("get_sugestoes", content)
        },
        async buscar_por_membro(membro)
        {
            const promise = await fetch(`http://localhost:8025/buscar_por_membro`, {
                method: 'POST',
                body: new URLSearchParams({
                    nome: membro
                }),
                headers: {
                    "Authorization": `Bearer ${localStorage.token}`,
                }
            })
            const resp = await promise.json()
            localStorage.setItem('membro', JSON.stringify(resp));
            this.membro = resp
            this.opcoes_membros = []
            window.location.href = `formulario.html`
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
            this.opcoes_membros = sugestoes
        });

        this.socket = socket
    }
})
appVM = app.mount('#conteiner')