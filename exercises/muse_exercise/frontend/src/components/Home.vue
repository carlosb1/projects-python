<template>
<div>
    <div style="background:transparent !important" class="jumbotron text-center text-info">
        <h1>Demo Video Silencer</h1>
        <p>Web app to silence videos</p>
        <label id="upload_button" class="btn-lg btn-info">
         Upload video <input type="file" id="file" ref="file" hidden @change="handleFileUpload">
        </label>
    </div>
    
    <div class="container">	
        <div class="card m-2  border-info">
          <div style="background:transparent !important" class="card-header  border-info">
                <h5 class="text-info">Analysed videos</h5>
          </div>
                <div class="card-body">
                    <div class="row mt-2">
                        <table class="table is-hoverable is-fullwidth">
                            <thead>
                            <tr>
                                <th>Name video</th>
                                <th>Id</th>
                                <th>Date</th>
                                <th class="is-pulled-right">Status</th>
                                <th class="is-pulled-right"></th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="(item, key) in videos">
                                <td>{{ item.namefile }}</td>
                                <td> {{ item.id }} </td>
                                <td> {{ item.last_modified }} </td>
                                <td class="is-pulled-right">                                    
                                    <button type="button" class="btn btn-block  btn-warning" v-if="item.status == 'PENDING'"> PENDING </button>
                                    <button type="button" class="btn btn-block  btn-success" v-if="item.status == 'SUCCESS'"> SUCCESS </button>
                                    <button type="button" class="btn btn-block  btn-danger" v-if="item.status == 'ERROR'"> ERROR </button>
                                </td>
                                <td class="is-pulled-right">
                                    <a role="button" class="btn btn-block btn-secondary" v-if="item.status == 'SUCCESS'" :href="item.download_link"> Download </a>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <input type="button" class="btn btn-lg btn-block btn-outline-success" id="download_map" @click="updateVideos()" value="Refresh"/>
                    </div>
                </div>
            </div>             
    </div>
    <div id="warning_connection" class="alert alert-warning" role="alert" hidden>
        <strong>Warning!</strong> Problems connecting to the backend server...
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
            videos: [],
            timer: ''
        }
    },
    created () {
        this.fetchEvents();
        this.timer = setInterval(this.fetchEvents, 10000);
    },
    beforeDestroy() {
        clearInterval(this.timer);
    },
    methods:
    {
        fetchEvents() {
            this.updateVideos();
            console.log("Getting updated list")
        },   
        showMessageError() {
                document.getElementById("warning_connection").hidden = false;
                function hide_popup() {
                    document.getElementById("warning_connection").hidden = true;
                };
                window.setTimeout(hide_popup, 3000);
        },
        downloadVideo(id) {
                console.log("Download video id: "+id);
        },     
        updateVideos() {
            console.log("Getting videos information");
                    const path = 'http://0.0.0.0:5002/v1/api/videos';
            axios
            .get(path)
                .then(response => {
                        this.videos = response.data.data;
                })
                .catch(error => {
                    console.log(error);
                    this.showMessageError();
                });
        },
        handleFileUpload( ){
            console.log("Uploading videos");
            var videos_to_upload = this.$refs.file.files[0];
            document.getElementById("file").value = "";
            let formData = new FormData();
            formData.append('files[0]', videos_to_upload);
            const path = 'http://0.0.0.0:5002/v1/api/videos';
            axios
            .post(path, formData)
            .then(response => {
                if (!("ids" in response.data) || response.data['ids'].length < 1) {
                    this.showMessageError();
                    return;
                }
                this.updateVideos();
            })
            .catch(error => {
                console.log(error);
                this.showMessageError();
            });
        }
     }
}
</script>

  
