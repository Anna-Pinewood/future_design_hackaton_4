<template>
  <div class="hello">
    <div style="text-align: center; width: 800px">
      <h1>Добро пожаловать к Олесе!</h1>
      <div class="ok"></div>
      <h3 class="intro">
        Наша цель - помочь пользователям сервиса предотвратить выгорание,
        улучшить эмоциональное состояние за счёт лучшего тайм-менеджмента, а
        также лучше понять свои потребности и возможности.
      </h3>
      <h3 class="intro">
        Встаньте на путь к осознанности. Особенно здорово, если вы пользуетесь
        to-do приложениями, где можно скачать csv файл - здесь можно получить
        полезную статистику!
      </h3>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hello {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
.ok {
  width: 500px;
  height: 500px;
  margin-left: 160px;
  display: flex;
  background: url(ole.SVG) no-repeat;
  justify-content: center;
  align-items: center;
}
.intro {
  display: flex;
  align-items: center;
  text-align: center;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
