<template>
  <div id="app">
    <nav>
      <router-link to="/"> Обучение модели </router-link> |
      <router-link to="/games"> Ваши цели </router-link> |
      <router-link to="/prediction"> Предсказать выгорание </router-link> |
      <router-link to="/prod"> Показать продуктивные часы </router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
#app {
  margin-top: 60px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #48d1cc;
}

.jumbotron {
  padding: 2rem 1rem;
  margin-bottom: 2rem;
  background-color: #cd5c5c;
  border-radius: 0.3rem;
}
</style>
