
<template>
  <div>
	  <h1> {{ message }}</h1>
	  <input v-model="message">
	  <button v-on:click="sendMessage()">Send</button>
	  <div v-if="logs">
		  <hr>
		  <p v-for="log in logs">
		  	{{ log }}
		  </p>
	  </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
    	message: '',
	logs: []
    }
  },
  sockets: {
	 connect: function () {
	 	console.log('Connected to the backend web socket server')
	 },
	 disconnect: function () {
	 	console.log('Disconnected from the backend web socket server')
	 },
	 event: function (data) {
		 console.log('Got event: '+ data.message)
	 },
	 response: function (data) {
		 console.log('Got response: '+ data.message)
		 this.logs.push(data.message)
	 }
  },
  methods: {
    sendMessage: function () {
     	this.$socket.emit('event', this.message)
	console.log('Sent "'+ this.message + '" to the backend')
	this.message = ''
    }
  }
}
</script>
