
<template>
  <section  id="name" class="is-info is-fullheight">
    <div class="head">
            <!-- Main container -->
            <nav class="level">
              <!-- Left side -->
              <div class="level-left">
                <div class="level-item">
                  <p class="subtitle is-5">
                     File to search: 
                  </p>
                </div>
                <div class="level-item">
                  <div class="field has-addons">
                    <p class="control">
                      <input type="file" id="file" ref="file" class="button is-expanded" @change="handleFileUpload">
                    </p>
                    <p class="control">  <button @click="submit" class="button">Search </button>  </p>
                  </div>
                </div>
              </div>
              <!-- Right side -->
              <div class="level-right">                  
                <p class="level-item"> <router-link class="button is-success" to="/add">Add Images</router-link> </p>
              </div>
            </nav>   
    </div>
    <div class="body">
      <div class="container has-text-centered is-centered">
        <div class="column is-9 is-offset-2">
          <h1 class="title">Example retrieving images</h1>
          <h2 class="subtitle">Upload an image</h2> 
            <ul>
			          <li v-for="item in responses">
                    <div class="box">             
                      <div class="card">
                          <div class="card-image">
                          </div>
                          <div class="card-content">
                            <div class="media">
                              <div class="media-left">
                                <figure class="image is-128x128">
                                  <img :src="item.path" alt="Placeholder image">
                                </figure>
                              </div>
                              <div class="media-content">
                                  <div class="title is-4 has-text-right">{{item.img_id}} </div>
                                   <div class="subtitle is-6 has-text-right">{{item.rank}}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                       </div>
                </li>
		      </ul>
            </div>
        </div>
      </div>
  </section>
</template>

<script>
import axios from "axios";
export default {
  data: function () {
    return {
      file: "",
      responses: [],
    };
  },
  methods: {
    handleFileUpload( ){
        this.file = this.$refs.file.files[0];
    },
    submit() {
      let formData = new FormData();
      formData.append("file", this.file);
      const path = 'http://localhost:5002/api/analysis';
      axios
        .post(path, formData)
        .then(response => {
	            this.responses = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
	  //throws this trigger when it creates the webpage
  }
};
</script>
