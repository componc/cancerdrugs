<template lang="pug">
  v-app#app

    v-app-bar(app color='white' light absolute flat)

      v-container
        v-row
          v-toolbar-title
            router-link(to='/' tag='span')
              span
                v-icon(color='black') mdi-pill
                span.text--lighten-5
                |  cancer
                b drugs

          v-spacer

          v-btn.hidden-xs-only(to='/about' text) About
    
          v-btn.hidden-sm-and-up(to='/about' icon)
            v-icon mdi-information

    v-main
      v-divider
      Nuxt

    v-footer(color='light-grey' app flat absolute)
      v-container
        v-col
          v-row
            p.centered.text-center.overline
              | The data is provided as-is without any warranties.
</template>


<style>
#app {
  background-color: #fff;
}
.centered {
  margin: 0 auto;
}
</style>