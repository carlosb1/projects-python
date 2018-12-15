
<template>
  <section class="is-info is-fullheight">
    <div class="head">
      <nav class="navbar">
        <div class="container"></div>
      </nav>
    </div>

    <div class="body">
      <div class="container has-text-centered">
        <div class="column is-6 is-offset-3">
          <h1 class="title">Example retrieving images</h1>
          <h2 class="subtitle">Upload an image</h2>
          <form class="box">
            <div class="field is-grouped">
              <label>
                File:
                <input
                  type="file"
                  id="file"
                  ref="file"
                  class="button is-expanded"
                  @change="handleFileUpload"
                >
              </label>
              <p class="control">
                <button @click="submit" class="button is-info">Upload</button>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      randomNumber: 0,
      file: ""
    };
  },
  methods: {
    handleFileUpload( ){
        this.file = this.$refs.file.files[0];
    },
    submit() {
      let formData = new FormData();
      formData.append("file", this.file);
      const path = `http://localhost:5002/api/images/analysis`;
      axios
        .post(path, formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          console.log("SUCCESS!!");
        })
        .catch(error => {
          console.log(error);
        });
    },
    getRandomInt(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    getRandom() {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.randomNumber = this.getRandomFromBackend();
    },
    getRandomFromBackend() {
      const path = `http://localhost:5002/api/random`;
      axios
        .get(path)
        .then(response => {
          this.randomNumber = response.data.randomNumber;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.getRandom();
  }
};
</script>
<style lang="scss">
@import "../../node_modules/bulma/bulma.sass";
</style>
