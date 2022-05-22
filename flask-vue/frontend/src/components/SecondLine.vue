<template>
  <div style="margin-top: 25px; margin-left: 150px">
    <b-button style="margin-top: 25px; margin-left: 150px" @click="getInfo()">
      Посмотреть статистику
    </b-button>
    <div v-if="loaded" style="width: 800px; height: 700px">
      <div style="margin-top: 30px">
        <LineCo
          :chart-data="{
            labels: chartData['chart'][0][0],
            datasets: [
              {
                data: chartData['chart'][0][1],
                label: chartData['chart'][0][2],
                backgroundColor: chartData['chart'][0][3],
                hoverBackgroundColor: chartData['chart'][0][4],
                borderColor: chartData['chart'][0][3][0],
              },
              {
                data: chartData['chart'][1][1],
                label: chartData['chart'][1][2],
                backgroundColor: chartData['chart'][1][3],
                hoverBackgroundColor: chartData['chart'][1][4],
                borderColor: chartData['chart'][1][3][0],
              },
              {
                data: chartData['chart'][2][1],
                label: chartData['chart'][2][2],
                backgroundColor: chartData['chart'][2][3],
                hoverBackgroundColor: chartData['chart'][2][4],
                borderColor: chartData['chart'][2][3][0],
              },
              {
                data: chartData['chart'][3][1],
                label: chartData['chart'][3][2],
                backgroundColor: chartData['chart'][3][3],
                hoverBackgroundColor: chartData['chart'][3][4],
                borderColor: chartData['chart'][3][3][0],
              },
              {
                data: chartData['chart'][4][1],
                label: chartData['chart'][4][2],
                backgroundColor: chartData['chart'][4][3],
                hoverBackgroundColor: chartData['chart'][4][4],
                borderColor: chartData['chart'][4][3][0],
              },
            ],
          }"
          :chart-options="{ title: ['chart'][0][2], responsive: true }"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import "chart.js/auto";
import { Line as LineCo } from "vue-chartjs/legacy";
export default {
  name: "DataLine",
  data() {
    return {
      loaded: null,
      chartData: { chart: [(0, 0), (0, 0)] },
    };
  },
  methods: {
    getInfo() {
      const path = "http://localhost:5000/chart";
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
  components: { LineCo },
};
</script>
