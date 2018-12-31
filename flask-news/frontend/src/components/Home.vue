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
            <div v-if="results">
                <hr>
                <div class="msg-group p-2" v-for="result in results">
                        <div class="card">
                        <div class="card-header">
				{{ result._source.title }}
                        </div>
                        <div class="card-body">
                            <blockquote class="blockquote mb-0">
				    <p>{{ result._source.summary }}</p>
				    <footer class="blockquote-footer"> {{ result._source.timestamp  }} extracted from: <a v-bind:href="result._source.url"><cite title="Source Title">link</cite></a></footer>
                            </blockquote>
                        </div>
                        </div>
                </div>
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
            results: [] 
        }
    },
    
    methods:
     {
        search( ) {
        const path = 'http://0.0.0.0:5002/api/news';
        axios
	.get(path, {params: {"tags" : this.currentTags.split(" ")}})
          .then(response => {
                this.results = response.data['results'];
         })
          .catch(error => {
            console.log(error);
          });
    }
     }
}
</script>

  
