(window.webpackJsonp=window.webpackJsonp||[]).push([[3],{354:function(t,e,n){var content=n(363);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(12).default)("fb74ddc6",content,!0,{sourceMap:!1})},362:function(t,e,n){"use strict";n(354)},363:function(t,e,n){(e=n(11)(!1)).push([t.i,".alignTop{vertical-align:top}.centered{margin:0 auto}a{text-decoration:none}.table4 td{vertical-align:top;padding-bottom:10px;padding-top:10px}.table4 ul{padding-left:0}.table4 ul,ul{list-style:none}ul{padding-left:0!important}",""]),t.exports=e},418:function(t,e,n){"use strict";n.r(e);n(68);var r=n(15),o={head:function(){return{title:this.drug.nciThesaurus.preferredName}},asyncData:function(t){return Object(r.a)(regeneratorRuntime.mark((function e(){var n,r,o;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return n=t.$content,r=t.params,e.next=3,n("drugs",r.drug).fetch();case 3:return o=e.sent,e.abrupt("return",{drug:o});case 5:case"end":return e.stop()}}),e)})))()}},l=(n(362),n(70)),c=n(160),d=n.n(c),v=n(330),_=n(336),f=n(319),m=n(333),h=n(361),C=n(346),x=n(412),y=n(420),T=n(415),component=Object(l.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-container",[n("h1",[t._v(t._s(t.drug.nciThesaurus.preferredName))]),n("v-tabs",{staticClass:"mt-2"},[n("v-tab",[t._v("Overview")]),n("v-tab",[t._v("Authorisation Status")]),n("v-tab-item",[n("v-container",{staticClass:"body-2"},[n("v-row",[n("v-col",{staticClass:"col-md-2 subtitle-2"},[t._v("Description")]),n("v-col",{staticClass:"text-justify"},[t._v(t._s(t.drug.nciThesaurus.definition))])],1),n("v-divider"),n("v-row",[n("v-col",{staticClass:"col-md-2 subtitle-2"},[t._v("Synonyms")]),n("v-col",[n("ul",t._l(t.drug.nciThesaurus.synonyms,(function(e){return n("li",[t._v(t._s(e))])})),0)])],1),n("v-divider"),n("v-row",[n("v-col",{staticClass:"col-md-2 subtitle-2"},[t._v("FDA UNII Code")]),n("v-col",[t._v(t._s(t.drug.nciThesaurus.fdaUniiCode))])],1),n("v-divider"),n("v-row",[n("v-col",{staticClass:"col-md-2 subtitle-2"},[t._v("Chemical Formula")]),n("v-col",[t._v(t._s(t.drug.nciThesaurus.chemicalFormula))])],1),n("v-divider"),n("v-row",[n("v-col",{staticClass:"col-md-2 subtitle-2"},[t._v("CAS-Registry")]),n("v-col",[t._v(t._s(t.drug.nciThesaurus.casRegistry)+"   ")])],1)],1)],1),n("v-tab-item",[n("v-subheader",{staticClass:"mt-4"},[t._v("Authorisation Status (EMA)")]),n("v-simple-table",{scopedSlots:t._u([{key:"default",fn:function(){return[n("thead",[n("tr",[n("th",{staticClass:"text-left"},[t._v("Medicine Name")]),n("th",{staticClass:"text-left"},[t._v("Authorisation Date")]),n("th",{staticClass:"text-left"},[t._v("Authorisation Holder")]),n("th",{staticClass:"text-left"},[t._v("Indication")])])]),n("tbody",t._l(t.drug.emaEpar,(function(e){return n("tr",[n("td",{staticClass:"alignTop"},[t._v(t._s(e.medicineName))]),n("td",{staticClass:"alignTop"},[t._v(t._s(e.marketingAuthorisationDate))]),n("td",{staticClass:"alignTop"},[t._v(t._s(e.marketingAuthorisationHolder))]),n("td",{staticClass:"alignTop text-justify"},[t._v(t._s(e.conditionIndication))])])})),0)]},proxy:!0}])}),n("v-subheader",{staticClass:"mt-4"},[t._v("Authorisation Status (FDA)")]),n("v-simple-table",{scopedSlots:t._u([{key:"default",fn:function(){return[n("thead",[n("tr",[n("th",{staticClass:"text-left"},[t._v("Brand")]),n("th",{staticClass:"text-left"},[t._v("Manufacturer")]),n("th",{staticClass:"text-left"},[t._v("Indication")])])]),n("tbody",t._l(t.drug.fdaDrugLabel,(function(e){return n("tr",[n("td",{staticClass:"alignTop"},[t._v(t._s(e.brand))]),n("td",{staticClass:"alignTop"},[t._v(t._s(e.manufacturer))]),n("td",{staticClass:"alignTop text-justify"},[t._v(t._s(e.indication))])])})),0)]},proxy:!0}])})],1)],1)],1)}),[],!1,null,null,null);e.default=component.exports;d()(component,{VCol:v.a,VContainer:_.a,VDivider:f.a,VRow:m.a,VSimpleTable:h.a,VSubheader:C.a,VTab:x.a,VTabItem:y.a,VTabs:T.a})}}]);