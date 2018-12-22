<template>
  <section class="section">
      <div class="container">
        <h1 class="title">Add images</h1>
          <hr><br><br>
          <input type="file" id="file" ref="file" class="button is-expanded" @change="handleFileUpload">
          <button type="button" @click="uploadFiles" class="button is-info is-pulled-right are-large">Upload</button>
          <br><br>
          <table class="table is-hoverable is-fullwidth">
            <thead>
              <tr>
                <th>Name image</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, key) in files">
                <td>{{ item.name }}</td>
                <td class="is-pulled-right">
                  <button type="button" @click="removeFile( key )" class="button is-danger">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  </section>
</template>
<script>
import axios from "axios";
export default {
  data: function () {
    return {
      files: [],
      randomNumber: 0,
    };
  },
  methods: {
    removeFile ( key ) {
        this.files.splice(key, 1);
    },
    handleFileUpload( ){
        this.files.push(this.$refs.file.files[0]);
    },
    uploadFiles( ) {
        console.log("Uploading files");
        let formData = new FormData();
        for( var i = 0; i < this.files.length; i++ ){
            let file = this.files[i];
            formData.append('files[' + i + ']', file);
        }
        const path = 'http://localhost:5002/api/images';
        axios
          .post(path, formData)
          .then(response => {
                this.files = [];
         })
          .catch(error => {
            console.log(error);
          });
    }
    /*
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
    */
  },
  created() {
	  //throws this trigger when it creates the webpage
  }
};
</script>
