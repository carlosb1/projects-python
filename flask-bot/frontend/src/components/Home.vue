<template>
<div>
    <div class="container-flude">
        <div v-if="allMessages">
            <hr>
            <div class="msg-group center" v-for="message in allMessages">
                <div class="card">
                        <div class="card-body">
                            <h6 class="card-subtitle mb-2 text-muted text-left">{{ message[0] }}</h6>
                            <p class="card-text float-left">{{ message[1] }}</p>
                        </div>
                </div>
            </div>
        </div>  	                
        <div class="input-group">
            <textarea id="input-box" v-model="currentMessage" class="form-control" rows="1" placeholder="Say something..." @keyup="validate" ></textarea>
            <span class="input-group-btn">
                <button class="btn btn-secondary" type="button"  v-on:click="sendMessage()" >send</button>
            </span>
        </div>
              
    </div>
    

</div>
</template>
<script>

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export default {
    data () {
        return {
            currentMessage: '',
            allMessages: [],
            message: '',
            logs: []
        }
    },
    sockets: {
        connect: function() {
            console.log('Connected to the backend web socket server')
        },
        disconnect: function() {
            console.log('Disconnected from the backend web socket server')
        },
        event: function(data) {
            console.log('Got event: ' + data.message)
        },
        response: function(data) {
            console.log('Got response: ' + data.message)
            this.logs.push(data.message)
            this.allMessages.push(["bot", data.message])
        }
    },
    methods:
     {
        validate: function(e) {
            if(e.keyCode === 13)
            {
                console.log("enter key was pressed!")
                this.sendMessage()
            }
        }, sendMessage: function() {
                this.allMessages.push(["me", this.currentMessage])
                this.$socket.emit('event', this.currentMessage)
                this.currentMessage = ''
        }
    }
}
</script>

  
