<template>
<div>
    <div class="container">	                
        <div class="input-group p-4">
            <label class="h6" for="basic-url">URL to analyse</label>
            <div class="input-group mb-3">
            <div class="input-group-prepend">
                <span class="input-group-text" id="basic-addon3">HTTP://</span>
            </div>
            <input v-model="currentURL" type="text" class="form-control" id="basic-url" aria-describedby="basic-addon3">
            </div>
            <span class="input-group-btn">
                <button class="btn btn-primary" type="button"  v-on:click="addURL()" >add!!</button>
            </span>
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
            currentURL: '',
            URLs: []
        }
    },
    methods:
     {
        addURL: function() {
            this.URLs = []
            this.URLs.push(this.currentURL)       
            const path = 'http://0.0.0.0:5001/api/news';
            axios
            .post(path, {
                    "urls": this.URLs,
                })
            .then(response => {
                    this.currentURL='';
            })
            .catch(error => {
                console.log(error);
            });
            }
    }
}
</script>

  
