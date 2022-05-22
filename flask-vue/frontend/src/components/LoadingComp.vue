<template>
  <div style="width: 800px; height: 800px">
    <div v-for="(bar, index) in bars" class="row mb-1" v-bind:key="index">
      <div class="col-sm-10 pt-1">
        <b-progress
          :value="bar.value"
          :variant="bar.variant"
          :key="bar.variant"
        ></b-progress>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoadComp",
  data() {
    return {
      bars: [
        { variant: "success", value: 75 },
        { variant: "info", value: 75 },
        { variant: "warning", value: 75 },
        { variant: "danger", value: 75 },
        { variant: "primary", value: 75 },
        { variant: "secondary", value: 75 },
        { variant: "dark", value: 75 },
      ],
      timer: null,
    };
  },
  mounted() {
    this.timer = setInterval(() => {
      this.bars.forEach((bar) => (bar.value = 25 + Math.random() * 75));
    }, 650);
  },
  beforeDestroy() {
    clearInterval(this.timer);
    this.timer = null;
  },
};
</script>
