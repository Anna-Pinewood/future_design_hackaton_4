<!--Extra one just in case-->

<template>
  <Bar :chart-data="chartData" :chart-options="chartOptions" />
</template>

<script>
// DataPage.vue
import { Bar } from "vue-chartjs/legacy";

export default {
  name: "BarComponent",
  components: { Bar },
};
</script>
