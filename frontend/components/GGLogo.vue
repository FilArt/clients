<template>
  <img class="GGLogo" alt="Vuetify Logo" src="/gg_logo_white.png" />
</template>
<script>
export default {
  name: 'GGLogo'
}
</script>
<style>
.GGLogo {
  height: 200px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

@keyframes turn {
  100% {
    transform: rotateY(0deg);
  }
}
</style>
