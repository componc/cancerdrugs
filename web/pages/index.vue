<template lang="pug">
v-container
  v-row.mt-md-12
    v-col.col-12.col-md-10.offset-md-1.mt-12
      v-autocomplete(label='Search drug' single-line
      prepend-inner-icon='mdi-magnify' outlined :items='index.drugs' item-text='preferredName'
      item-value='id' @change='updateRoute')
        template(v-slot:item='{ item }')
          v-list-item-avatar(color='grey') {{ item.preferredName.charAt(0) }}
          v-list-item-content
            v-list-item-title(v-text='item.preferredName')
            v-list-item-subtitle(v-text='item.synonyms.join(", ")')
</template>

<script>
export default {
  head() {
    return {
      title: 'Home'
    }
  },
  async asyncData ({ $content }) {
    const index = await $content('index')
    .fetch()
    return { index }
  },
  methods: {
    updateRoute (value) {
      this.$router.push('/drugs/' + value)
    }
  }
}
</script>