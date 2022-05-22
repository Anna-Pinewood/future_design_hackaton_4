<template>
  <div>
    <h1 style="padding-bottom: 40px">
      Здесь вы можете посмотреть свои наиболее продуктивные часы!
    </h1>
    <h3 style="padding-bottom: 40px">
      Здесь вы можете увидеть визуализацию своих наиболее эффективных часов,
      основываясь на введенных ранее данных
    </h3>
    <b-button pill variant="success" size="lg" @click="getData">
      Посмотреть
    </b-button>
    <div v-if="loaded === false">
      <h3 style="padding-top: 20px">Считаем...</h3>
      <div style="padding-left: 650px; padding-top: 20px">
        <LoadComp />
      </div>
    </div>
    <div v-if="loaded" style="display: flex; align-content: row">
      <div
        v-for="row in chartData['chart']"
        v-bind:key="row[0][0]"
        style="
          width: 1050px;
          height: 1050px;
          padding-left: 60px;
          padding-right: 50px;
        "
      >
        <h3>{{ row[2] }}</h3>
        <Bar
          :chart-data="{
            labels: row[0],
            datasets: [
              {
                data: row[1],
                label: row[2],
                backgroundColor: row[3],
                hoverBackgroundColor: row[4],
              },
            ],
          }"
          :chart-options="{ title: row[2], responsive: true }"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import "chart.js/auto";
import { Bar } from "vue-chartjs/legacy";
import LoadComp from "@/components/LoadingComp.vue";

export default {
  name: "ProdHours",
  components: { Bar, LoadComp },
  data() {
    return {
      loaded: null,
      chartData: { chart: [(0, 0), (0, 0)] },
    };
  },
  methods: {
    getData() {
      this.loaded = false;
      const path = "http://localhost:5000/productive";
      axios
        .get(path)
        .then((res) => {
          this.chartData["chart"] = res.data["data"];
          this.loaded = true;
          console.log(res.data["chart"]);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style></style>
