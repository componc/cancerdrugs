<template lang="pug">
v-container
  v-row
    v-col
      h1 About
      p cancerdrugs is a drug-centric precision oncology database that aggregates curated 
        | and publically available drug data. cancerdrugs is developed by the Computational Oncology Group at the 
        | Department of Medicine, Hematology/Oncology at the Goethe University Hospital in Frankfurt Germany.
      p The cancerdrugs database was developed as part of MIRACUM Use Case 3 (Support for Molecular Tumor Boards).
        | The MIRACUM research consortia is supported by the medical informatics initiative of the German Federal Ministry of 
        | Education and Research (BMBF).
  v-row
    v-col
      p The data sources are listed below:
      v-simple-table
        template(v-slot:default='')
          thead
            tr
              th.text-left Name
              th.text-left URL
          tbody
            tr
              td NCI Thesaurus
              td 
                a(href='https://ncithesaurus.nci.nih.gov/' target='_blank') 
                  | https://ncithesaurus.nci.nih.gov/
            tr
              td EMA
              td 
                a(href='https://www.ema.europa.eu/en/medicines/download-medicine-data' target='_blank')
                  | https://www.ema.europa.eu/en/medicines/download-medicine-data
            tr
              td FDA
              td 
                a(href='https://open.fda.gov/apis/' target='_blank')
                  | https://open.fda.gov/apis/
</template>


<script>
export default {
  head() {
    return {
      title: 'About'
    }
  }
}
</script>