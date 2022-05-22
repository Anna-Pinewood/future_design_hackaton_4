<template>
  <div>
    <HelloWorld />
    <FirstForm />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import FirstForm from "@/components/FirstForm.vue";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
    FirstForm,
  },
};
</script>
