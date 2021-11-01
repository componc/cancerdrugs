<template lang="pug">
v-container
  h1 {{ drug.nciThesaurus.preferredName }}

  v-tabs.mt-2
    v-tab Overview
    v-tab Authorisation Status

    v-tab-item
      v-container.body-2 
        v-row
          v-col.col-md-2.subtitle-2 Description
          v-col.text-justify {{ drug.nciThesaurus.definition }}
        v-divider
        v-row
          v-col.col-md-2.subtitle-2 Synonyms
          v-col
            ul
              li(v-for='item in drug.nciThesaurus.synonyms') {{ item }}
        v-divider
        v-row
          v-col.col-md-2.subtitle-2 FDA UNII Code
          v-col {{ drug.nciThesaurus.fdaUniiCode }}
        v-divider
        v-row
          v-col.col-md-2.subtitle-2 Chemical Formula
          v-col {{ drug.nciThesaurus.chemicalFormula }}
        v-divider
        v-row
          v-col.col-md-2.subtitle-2 CAS-Registry
          v-col {{ drug.nciThesaurus.casRegistry }}   

    v-tab-item
      v-subheader.mt-4 Authorisation Status (EMA)
      v-simple-table
        template(v-slot:default='')
          thead
            tr
              th.text-left Medicine Name
              th.text-left Authorisation Date
              th.text-left Authorisation Holder
              th.text-left Indication
          tbody
            tr(v-for='item in drug.emaEpar')
              td.alignTop {{ item.medicineName }}
              td.alignTop {{ item.marketingAuthorisationDate }}
              td.alignTop {{ item.marketingAuthorisationHolder }}
              td.alignTop.text-justify {{ item.conditionIndication }}

      v-subheader.mt-4 Authorisation Status (FDA)
      v-simple-table
        template(v-slot:default='')
          thead
            tr
              th.text-left Brand
              th.text-left Manufacturer
              th.text-left Indication
          tbody
            tr(v-for='item in drug.fdaDrugLabel')
              td.alignTop {{ item.brand }}
              td.alignTop {{ item.manufacturer }}
              td.alignTop.text-justify {{ item.indication }}
</template>

<script>
export default {
  head() {
    return {
      title: this.drug.nciThesaurus.preferredName
    }
  },
  async asyncData ({ $content, params }) {
    const drug = await $content('drugs', params.drug).fetch()
    return { drug }
  }
}
</script>

<style>
.alignTop {
  vertical-align: top
}
.centered {
  margin: 0 auto;
}
a {  
  text-decoration: none;
}
.table4 td {
  vertical-align: top;
  padding-bottom: 10px;
  padding-top: 10px;
}
.table4 ul {
  list-style: none;
  padding-left: 0;
}
ul {
  list-style: none;
  padding-left: 0!important;
}
</style>
