<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <b-form-file
        v-model="file"
        :state="Boolean(file)"
        placeholder="Choose a file or drop it here..."
        drop-placeholder="Drop file here..."
        type="file"
        id="file"
        ref="file"
        v-on:change="handleFileUpload()"
      ></b-form-file>
      <div class="mt-3">Selected file: {{ file ? file.name : "" }}</div>
      <!--SUBMIT MODEL BUTTON-->
      <br />

      <b-button type="submit" v-on:click="submitFile()" variant="outline-info">
        Обучить модель на ваших данных
      </b-button>

      <div v-if="loaded === true">
        <h3 style="padding-top: 20px">Учим модельку...</h3>
        <div>
          <LoadComp />
        </div>
      </div>
      <div v-if="loaded === false">
        <h3 style="padding-top: 20px">Модель обучилась!</h3>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import LoadComp from "@/components/LoadingComp.vue";
export default {
  name: "FileHandler",
  data() {
    return {
      file: null,
      loaded: null,
    };
  },
  methods: {
    submitFile() {
      this.loaded = true;
      let formData = new FormData();
      formData.append("file", this.file);
      axios
        .post("http://localhost:5000/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(function () {
          console.log("SUCCESS!!");
        })
        .catch(function () {
          console.log("FAILURE!!");
        });
      this.loaded = false;
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
  },
  components: {
    LoadComp,
  },
};
</script>
