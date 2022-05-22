<template>
  <div>
    <button @click="getInfo">Узнать о себе больше</button>
    <div v-if="loaded">
      <div v-for="row in chartData['chart']" v-bind:key="row[0][0]">
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

        <BarComponent
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
import { BarComponent } from "@/components/BarComponent.vue";

export default {
  name: "ChartsOne",
  data() {
    return {
      loaded: null,
      chartData: { chart: [(0, 0), (0, 0)] },
    };
  },
  methods: {
    getInfo() {
      const path = "http://localhost:5000/user_form";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data["chart"][0]);
          this.ChartData = {
            label: "Your chart",
          };
          this.chartData["chart"] = res.data["chart"];
          this.loaded = true;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  components: { Bar, BarComponent },
};
</script>
