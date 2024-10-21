const app = Vue.createApp({
    data() {
        return {
            usuario: '',
            senha: '',
            acesso_negado: false
        }
    },
    methods: {
        async handle_submit_login()
        {
            const promise = await fetch('http://delport.com.br:8025/login', {
                method: 'POST',
                body: new URLSearchParams({
                    usuario: this.usuario,
                    senha: this.senha,
                })
            })
            const resp = await promise.json()
            console.log(resp)
            if (resp.status == 'error') {
                this.acesso_negado = true
                return
            }
            localStorage.setItem('token', resp.token)
            window.location.href = `https://cadastro.pibpavuna.com.br/opcoes.html`
        }   
    }
})

const appVM = app.mount('#conteiner')
