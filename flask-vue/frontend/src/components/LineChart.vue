<template>
  <div>
    <b-button
      style="margin-top: 25px"
      @click="
        getInfo();
        getAdvice();
      "
      >Узнать больше❤</b-button
    >
    <div
      v-if="loaded"
      style="width: 800px; height: 700px display: flex; margin-left: 700px; margin-top: 25px flex-direction: row"
    >
      <div style="margin-top: 30px">
        <LineCo
          :chart-data="{
            labels: [1, 2, 3, 4, 5, 6],
            datasets: [
              {
                data: [12, 35, 56, null, null],
                label: chartData['chart'][0][2],
                backgroundColor: chartData['chart'][0][3][0],
                hoverBackgroundColor: chartData['chart'][0][4],
                borderColor: chartData['chart'][1][3][0],
              },
              {
                data: [null, null, 56, 65, 76],
                label: chartData['chart'][1][2],
                borderColor: '#dc143c',
                borderJoinStyle: chartData['chart'][1][3][0],
                hoverBackgroundColor: chartData['chart'][1][4],
              },
            ],
          }"
          :chart-options="{ title: ['chart'][0][2], responsive: true }"
        />
        <h3 style="margin-top: 30px">
          Совет на основе обработки ваших данных:
        </h3>
        <h2 style="margin-top: 30px">{{ advice }} 💗</h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import "chart.js/auto";
import { Line as LineCo } from "vue-chartjs/legacy";
export default {
  name: "LinesCom",
  data() {
    return {
      loaded: null,
      chartData: { chart: [(0, 0), (0, 0)] },
      advice: "",
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
    getAdvice() {
      const path = "http://localhost:5000/advice";
      axios
        .get(path)
        .then((res) => {
          console.log(res);
          this.advice = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  components: { LineCo },
};
</script>
