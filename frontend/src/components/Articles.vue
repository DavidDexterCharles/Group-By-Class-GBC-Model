<template>
  <section id="articles">
    <mdb-row>
      <mdb-col md="12">
        <mdb-card cascade narrow class="mt-5">
          <mdb-view class="gradient-card-header blue darken-2">
            <h4 class="h4-responsive text-white">Articles</h4>
          </mdb-view>
          <mdb-card-body class="sticky-top" style="padding-top:29px;backgroundColor:white;">
            <div class="input-group md-form form-sm form-2 pl-0">
              <input class="form-control my-0 py-1 lime-border" v-model="searchQuery" v-on:keyup.enter="classify" type="text" v-bind:placeholder="'Search by '+ searchoption" aria-label="Search">
              <!--<div class="btn-group">-->
              <!--    <button class="btn btn-danger btn-sm dropdown-toggle" type="button" data-toggle="dropdown"-->
              <!--      aria-haspopup="true" aria-expanded="false">-->
              <!--      Filter By-->
              <!--    </button>-->
              <!--    <div class="dropdown-menu">-->
              <!--      <a class="dropdown-item" href="#">Article Content</a>-->
                    <!--<div class="dropdown-divider"></div>-->
              <!--      <a class="dropdown-item" href="#">Article Category</a>-->
              <!--    </div>-->
              <!--</div>-->
               <!--<mdb-dropdown>-->
               <!--   <mdb-dropdown-toggle v-model="searchoption" class="btn btn-danger btn-sm dropdown-toggle" slot="toggle">Search By</mdb-dropdown-toggle>-->
               <!--   <mdb-dropdown-menu>-->
               <!--     <mdb-dropdown-item v-for="option in searchoptions" v-bind:key="option" v-bind:value="option" v-on:click="setsearchoption">{{option}}</mdb-dropdown-item>-->
                    <!--<div class="dropdown-divider"></div>-->
                    <!--<mdb-dropdown-item>Article Category</mdb-dropdown-item>-->
               <!--   </mdb-dropdown-menu>-->
               <!-- </mdb-dropdown>-->
                <select v-model="searchoption" class="btn btn-danger btn-sm dropdown-toggle" slot="toggle">
                  <!--<option disabled value="">Please select one</option>-->
                  <option  v-for="option in searchoptions"  v-bind:key="option" v-bind:value="option">{{option}}</option>
                </select>
            </div>
            <!--<span>Search Criteria: {{searchoption}}</span>-->
            <div><b>Total:       <span style="color:red;">{{filteredResources.length}}</span></b></div>
            <div class="input-group-append">
                <button v-on:click="addPage" class="btn btn-md btn-secondary m-0 px-3 right" type="button" id="MaterialButton-addon2">More Articles</button>
            </div>
             <div class="d-flex justify-content-center" v-if="loading">
                <div class="spinner-border center" style="width: 8rem; height: 8rem;" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
          </mdb-card-body>
        <!--</mdb-card>-->
        <!--<mdb-card cascade narrow class="mt-5">-->
           <mdb-card-body v-bind:key="ArticlescomponentKey">
              <div class="input-group md-form form-sm form-2 pl-0">
               <!--<div class="panel-body" style="max-height: 400px;overflow-y: scroll;">-->
                    <table v-if="resources.length" class="table">
                        <thead>
                            <tr>
                                <th>Articles</th>
                                <th>Content</th>
                                <th>Categories</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in filteredResources" v-bind:key="item.title">
                                <td>
                                    <a :href=item.uri target="_blank" style="color:blue;">{{item.title}}</a>
                                </td>
                                 <td>
                                    {{item.content}}
                                    <!--{{item.title}}-->
                                </td>
                                 <td>
                                   <div style="width:200px;">
                                      <mdb-pie-chart :data="item.pieChartData" :height="300" :width="300"/>
                                   </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                <!--</div>-->
              </div>
            </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
      <!--<mdb-container>-->
        <!--<mdb-card class="mb-4">-->
        <!--  <mdb-card-body>-->
                      <!--<mdb-card-text>Article Source</mdb-card-text>-->
        <!--      <div style="display: block">-->
        <!--        <mdb-pie-chart :data="pieChartData" :height="200" :width="200"/>-->
        <!--      </div>-->
        <!--  </mdb-card-body>-->
        <!--</mdb-card>-->
        <!--<mdb-row>-->
        <!--  <mdb-col col="sm">One of three columns</mdb-col>-->
        <!--  <mdb-col col="sm">-->
        <!--   <mdb-card class="mb-4">-->
        <!--          <mdb-card-header class="text-center">Article Title</mdb-card-header>-->
                  <!--<mdb-card-body>-->
                      <!--<mdb-card-text>Article Source</mdb-card-text>-->
                      <!--<div style="display: block">-->
        <!--                <mdb-pie-chart :data="pieChartData" :height="200" :width="200"/>-->
                      <!--</div>-->
                  <!--</mdb-card-body>-->
        <!--    </mdb-card>-->
        <!--  </mdb-col>-->
        <!--  <mdb-col col="sm">One of three columns</mdb-col>-->
        <!--  <mdb-col col="sm">One of three columns</mdb-col>-->
        <!--  <mdb-col col="sm">One of three columns</mdb-col>-->
        <!--  <mdb-col col="sm">One of three columns</mdb-col>-->
        <!--</mdb-row>-->
      <!--</mdb-container>-->
  </section>
</template>

<script>
// https://stackoverflow.com/questions/52558770/vuejs-search-filter
import { mdbDropdown, mdbDropdownItem, mdbDropdownMenu, mdbDropdownToggle, mdbCardHeader, mdbPieChart, mdbContainer, mdbRow, mdbCol, mdbCard, mdbCardBody, mdbView, mdbMask, mdbCardTitle, mdbCardText, mdbCardFooter, mdbIcon, mdbBtn, mdbPagination, mdbPageNav, mdbPageItem } from 'mdbvue'
import {_} from 'vue-underscore'
// var api = "http://gbcsystem-ice-wolf.c9users.io:8082/";
// var api = "http://3.85.235.141:8082/";
export default {
  name: 'Articles',
  components: {
    mdbDropdown,
    mdbDropdownItem,
    mdbDropdownMenu,
    mdbDropdownToggle,
    mdbCardHeader,
    mdbPieChart,
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbCard,
    mdbCardBody,
    mdbView,
    mdbMask,
    mdbCardTitle,
    mdbCardText,
    mdbCardFooter,
    mdbIcon,
    mdbBtn,
    mdbPagination,
    mdbPageNav,
    mdbPageItem
  },
  data () {
    return {
      api: 'http://3.87.231.155:8082/',
      searchoption: 'Article Content',
      searchoptions: ['Article Content', 'Article Category'],
      ArticlescomponentKey: 0,
      loading: 0,
      articles: [],
      numarticles: 0,
      numpages: '',
      maxpages: 1,
      submitted: false,
      showFrameModalTop: false,
      showFrameModalBottom: false,
      showSideModalTopRight: false,
      showSideModalTopLeft: false,
      showSideModalBottomRight: false,
      showSideModalBottomLeft: false,
      showCentralModalSmall: false,
      showCentralModalMedium: false,
      showCentralModalLarge: false,
      showCentralModalFluid: false,
      showFluidModalRight: false,
      showFluidModalLeft: false,
      showFluidModalTop: false,
      showFluidModalBottom: false,
      pieChartData: {
        labels: ['aaaaaaaaaaaaaaaaaaaaa', 'bbbbbbbbbbbbbbbbbb', 'cccccccccccccccccccccc'],
        datasets: [
          {
            data: [12, 44, 20],
            backgroundColor: ['#F7464A', '#46BFBD', '#FDB45C'],
            hoverBackgroundColor: ['#FF5A5E', '#5AD3D1', '#FFC870']
          }
        ]
      },
      pieChartOptions: {
        responsive: true,
        maintainAspectRatio: false
      },
      /* eslint-disable */
      searchQuery:'',
      searchQuery2:'',
      allCategories:[
        'Art and Culture',
        'Conflicts and War',
        'Crime',
        'Disaster and Accidents',
        'Economy',
        'Education',
        'Environment',
        'Health',
        'Human Interest',
        'Labor',
        'Lifestyle and Leisure',
        'Politics',
        'Religion and Belief',
        'Science and Technology',
        'Society',
        'Sport',
        'Weather'
      ],
      allBackgroundColor: [
        '#00FFFF',
        '#7FFFD4',
        '#000000',
        '#0000FF',
        '#FFFF00',
        '#A52A2A',
        '#DEB887',
        '#5F9EA0',
        '#7FFF00',
        '#D2691E',
        '#DC143C',
        '#FF8C00',
        '#9932CC',
        '#8FBC8F',
        '#FF1493',
        '#FF00FF',
        '#8A2BE2'
      ],
      resources:[
        // {
        //   title:"", 
        //   uri:"", 
        //   content:"",
        //   pieChartData: {
        //     labels:[],
        //     datasets: [
        //       {
        //         data: [],
        //         backgroundColor: [],
        //         hoverBackgroundColor: []
        //       }
        //     ]
        //   },
        //   pieChartOptions: {
        //     responsive: true,
        //     maintainAspectRatio: false
        //   }
        // }
      ]
    }
  },
  /* eslint-disable */
  computed: 
  {
      filteredResources ()
      {
            if(this.searchQuery){
              // console.log("Test1")
            return this.resources.filter((item)=>{
              var result;
              if(this.searchoption=="Article Content")
                result = item.content.toLowerCase().includes(this.searchQuery.toLowerCase());
              else{
                
                result = item.pieChartData.labels.join().toLowerCase().includes(this.searchQuery.toLowerCase());
              }
              // console.log(this.resources.length);
              return result;
            })
            }
            else{
              // console.log(this.resources.length);
              // this.numarticles = this.resources.length;
              return this.resources;
            }
      }
   },
   created (){
        // console.log("Test");
        this.getData(1);
       
          // this.getData(page);
    },
    methods:{
       
       setsearchoption: function(){
         console.log("Apples");
        // this.searchoption = option;
         
       },
      
       getData: function(page){
            this.loading=1;
            this.$http.get(this.api+'article?page='+page).then(
              function(data){
                // if(data.body.message)
                //     console.log(data.body.message);
                // else
                //     console.log("TEST DATA");
                // this.submitted = true;
                this.numpages = data.body.total_pages;
                this.articles.push(...data.body.data);//data.body.data;;
                var i,k,cdata,categorylabel;
                var title, uri,content, categorylabels,categoryvalues,categorycolors,catgorydata;
                var tempresource;
                this.resources=[];
                for(i=0;i<this.articles.length;i++){
                  categorylabel =[]
                  categoryvalues =[]
                  categorycolors = []
                  cdata = _.values(this.articles[i].articlecategories)
                  categorylabel  .push(cdata[0][0])
                  categorylabel  .push(cdata[1][0])
                  categorylabel  .push(cdata[2][0])
                  var ctot = cdata[0][1] + cdata[1][1] +cdata[2][1]
                  categoryvalues .push((cdata[0][1]/ctot)*100)
                  categoryvalues .push((cdata[1][1]/ctot)*100)
                  categoryvalues .push((cdata[2][1]/ctot)*100)
                  for(k=0;k<categorylabel.length;k++)
                    categorycolors.push(this.allBackgroundColor[this.allCategories.indexOf(categorylabel[k])])
                  // console.log(categorylabel)
                  // console.log(categoryvalues)
                  // console.log(categorycolors)
                  // console.log(title)
                  tempresource={
                    title:this.articles[i].TITLE, 
                    uri:this.articles[i].SOURCE, 
                    content:this.articles[i].CONTENT,
                    pieChartData: {
                      labels:categorylabel,
                      datasets: [
                        {
                          data: categoryvalues,
                          backgroundColor: categorycolors,
                          hoverBackgroundColor: []
                        }
                      ]
                    },
                    pieChartOptions: {
                      responsive: true,
                      maintainAspectRatio: false
                    }
                  };
                  // console.log(tempresource)
                  this.resources.push(tempresource)
                }
               
                var i;
                for(i=0;i<this.articles.length;i++)
                          console.log(this.articles[i].TITLE)
                
                this.numarticles = this.articles.length;
                // var page;
                // for(page=2;page<=this.numpages;page++)
                
                //     console.log("Test")
                // // this.article.content = data.body.CONTENT;
                // console.log(this.numpages)
               this.loading=0;
                // return this.resources;
            });
        },
        addPage: function()
        {
            var page = this.maxpages+1
            if(this.maxpages<=this.numpages)
            {
              this.getData(page);
              this.maxpages=page;
              this.ArticlescomponentKey += 1;
              console.log(this.maxpages)
            }
            else
            alert("No More Articles")
        }
    }
}
</script>

<style scoped>
.profile-card-footer {
  background-color: #F7F7F7 !important;
  padding: 1.25rem;
}
.card.card-cascade .view {
  box-shadow: 0 3px 10px 0 rgba(0, 0, 0, 0.15), 0 3px 12px 0 rgba(0, 0, 0, 0.15);
}
.gradient-card-header {
  padding: 1rem 1rem;
  text-align: center;
}
.action {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}
</style>
