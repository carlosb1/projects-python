<template>
<div>
    <div class="container">	                
        <div class="input-group p-4">
            <textarea id="input-box" v-model="currentTags" class="form-control" rows="1" placeholder="Tags to search..." ></textarea>
            <span class="input-group-btn">
                <button class="btn btn-secondary" type="button"  v-on:click="search()" >search</button>
            </span>
        </div>
        
        <div class="input-group">
            <div v-if="allMessages">
                <hr>
                <!--
                <div class="msg-group p-2" v-for="message in allMessages">
                        <div class="card">
                        <div class="card-header">
                            Quote
                        </div>
                        <div class="card-body">
                            <blockquote class="blockquote mb-0">
                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
                            <footer class="blockquote-footer">Someone famous in <cite title="Source Title">Source Title</cite></footer>
                            </blockquote>
                        </div>
                        </div>
                </div>
                -->
            </div> 
        </div>               
    </div>
    

</div>
</template>
<script>

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from "axios"


export default {
    data () {
        return {
            currentTags: '',
            data: [] 
        }
    },
    
    methods:
     {
        search( ) {
        const path = 'http://0.0.0.0:5001/api/news';
        axios
          .get(path, {"tags" : this.currentTags.split(" ")})
          .then(response => {
                this.data = response.data;
         })
          .catch(error => {
            console.log(error);
          });
    }
     }
}
</script>

  
