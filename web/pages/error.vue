<template lang="pug">
v-container
  v-row.mt-md-12
    v-col.col-12.col-md-10.offset-md-1.mt-12(v-if='error.statusCode === 404')
      h1.text-center 404
      h3.text-center Page not found
      p.text-center The page you are looking for doens't exist.
    v-col.col-12.col-md-10.offset-md-1.mt-12(v-else)
      p Error
</template>

<script>
export default {
  props: ['error'],
  data () {
    return {
    }
  },
  head () {
    //const title = this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title: 'Error'
    }
  }
}
</script>