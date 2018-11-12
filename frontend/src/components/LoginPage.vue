<template>
    <div class="container">
        <div id="loginbox" class="mainbox col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 centered-vertically">
            <div class="panel panel-info">
                <div style="background-color: #2A3F54; color: white" class="panel-heading">
                    <div class="panel-title">Вход в систему электронных журналов</div>
                </div>

                <div style="padding-top:30px" class="panel-body">

                    <div :style="{display: errorText ? 'block' : 'none'}" id="login-alert" class="alert alert-danger col-sm-12">
                        {{errorText}}
                    </div>

                    <form id="loginform" class="form-horizontal">

                        <div style="margin-bottom: 25px" class="input-group">
                            <div class="input-group-prepend">
                                <div class="input-group-text"><i class="fa fa-user"></i></div>
                            </div>
                            <input @input="onInput" id="login-username" list="persons" type="text" class="form-control" name="username" value=""
                                   placeholder='Имя пользователя'>
                            <template>
                                <datalist id="persons">
                                    <option v-for="person in usersList" :value="person" :key="person"></option>
                                </datalist>
                            </template>
                        </div>

                        <div style="margin-bottom: 25px;" class="input-group">
                            <div class="input-group-prepend">
                                <div class="input-group-text"><i class="fa fa-lock"></i></div>
                            </div>
                            <input id="login-password" type="password" class="form-control" name="password"
                                   placeholder='Пароль'>
                        </div>


                        <div style="margin-top:10px" class="form-group">
                            <!-- Button -->

                            <div class="controls">
                                <input type="submit" class="btn" style="background-color: #26B99A; height: 36px;" value='Вход' @click.prevent="onSubmit">
                            </div>
                        </div>
                    </form>


                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import $ from 'jquery'
    import ajax from '../axios.config'

    export default {
        name: "LoginPage",
        data () {
            return {
                errorText: '',
                usersList: [],
            }
        },
        methods: {
            onSubmit () {
                let username = $('input[name="username"]').val()
                let password = $('input[name="password"]').val()
                if (username && password) {
                    this.errorText = ''
                    this.login(username, password)
                }
                else {
                    this.errorText = 'Введите все данные!'
                }
            },
            getUsers(name) {
                return ajax.get(window.HOSTNAME + `/api/bl/dicts/usernames/?name=${name}`, {
                    withCredentials: true
                })  .then((response) => {
                        // console.log(response);
                        this.usersList = response.data
                    })
                    .catch(err => {
                        console.log(err)
                    })
            },
            onInput(e) {
                this.getUsers(e.target.value);

            },
            login (username, password) {
                this.$store.dispatch('userState/login', { username, password })
                    .then((res) => {
                        if (res.non_field_errors) {
                            this.errorText = 'Данные некорректны!'
                            return
                        }
                        this.$router.push('/')
                    })
                    .then(() => {
                        this.$connect();
                    })
                    .catch(err => {
                        if (err.non_field_errors) {
                            this.errorText = 'Данные некорректны!'
                        }
                    })
            }
        }
    }
</script>

<style scoped>
    .centered-vertically {
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .panel {
        margin-bottom: 20px;
        background-color: #fff;
        border: 1px solid transparent;
        border-radius: 4px;
        -webkit-box-shadow: 0 1px 1px rgba(0,0,0,.05);
        box-shadow: 0 1px 1px rgba(0,0,0,.05);
    }
    .panel-info {
        border-color: #bce8f1;
    }
    .panel-info>.panel-heading {
        background-color: #2A3F54;
        color: white;
        border-color: #bce8f1;
    }
    .panel-heading {
        padding: 10px 15px;
        border-bottom: 1px solid transparent;
        border-top-right-radius: 3px;
        border-top-left-radius: 3px;
    }
    .panel-title {
        margin-top: 0;
        margin-bottom: 0;
        font-size: 16px;
        color: inherit;
    }
    .panel-body {
        padding: 15px;
        padding-top: 30px;
    }
    .form-control {
        border: 1px solid #ced4da;
        min-width: 0;
        line-height: 1.42857143 !important;
        height: 100%;
        min-height: 30px;
        word-break: break-word;
        background: #fff;
    }
    @media (min-width: 992px) {
        .mainbox {
            width: 30%;
        }
    }
</style>
