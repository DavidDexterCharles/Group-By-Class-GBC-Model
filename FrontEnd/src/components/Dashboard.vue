<template>
  <section id="dashboard">
   <mdb-row>
      <mdb-col md="12">
        <mdb-card cascade narrow class="mt-5">
          <mdb-view class="gradient-card-header blue darken-2">
            <h4 class="h4-responsive text-white">Classifier</h4>
            <a href="http://3.87.231.155:8082/classificationmodel" target="_blank"  class="text-white"><u><b>View Classification Model</b></u></a>
          </mdb-view>
          <mdb-card-body v-bind:key="ClassifiercomponentKey">
            <div class="input-group md-form form-sm form-2 pl-0">
              <input class="form-control my-0 py-1 lime-border" v-model="article.url" v-on:keyup.enter="classify" type="text" placeholder="Takes both TEXT and URL as input (extracts content from web page where URL provided)" aria-label="Search">
              <div class="input-group-append">
                <span v-on:click.prevent="classify" class="input-group-text lime lighten-2" id="basic-text1"><i class="fas fa-dot-circle text-grey"
                    aria-hidden="true"></i></span>
              </div>
              <div class="d-flex justify-content-center" v-if="loading">
                <div class="spinner-border center" style="width: 3rem; height: 3rem;" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
            </div>
            <!--v-if="submitted"-->
            <mdb-card class="mb-4">
                  <mdb-card-header class="text-center"> Top 3 Categories </mdb-card-header>
                  <mdb-card-body>
                      <div style="display: block">
                        <mdb-pie-chart v-bind:key="ClassifiercomponentKey" :data="pieChartData" :options="pieChartOptions" :height="200"/>
                      </div>
                  </mdb-card-body>
            </mdb-card>
            <!--<mdb-row class="mt-5">-->
                <!--<mdb-col md="9" class="mb-4">-->
                <mdb-card class="mb-4" v-if="submitted">
                    <mdb-card-header class="text-center"> All cateogries and Weightings</mdb-card-header>
                    <mdb-card-body>
                        <div style="display: block">
                          <mdb-bar-chart v-bind:key="ClassifiercomponentKey" :data="barChartData" :options="barChartOptions" :height="500"/>
                        </div>
                    </mdb-card-body>
                </mdb-card>
                <!--</mdb-col>-->
            <!--</mdb-row>-->
            <mdb-card class="card-body" style=" margin-top: 1rem;">
              <mdb-card-title>Document Content</mdb-card-title>
              <mdb-card-text>{{article.content}}</mdb-card-text>
              <div class="flex-row">
                <p>SOURCE: {{article.asource}}</p>
              </div>
            </mdb-card>
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
    <!--eslint-disable-next-line-->
   <!--</br>-->
   <!--<mdb-row>-->
   <!--  <mdb-col md="12">-->
   <!--    <mdb-card cascade narrow class="mt-5">-->
   <!--      <mdb-card-body>-->
          <!--Stress-->
   <!--      </mdb-card-body>-->
   <!--    </mdb-card>-->
   <!--  </mdb-col>-->
   <!--</mdb-row>-->
   <!--<div class="card">-->
   <!--   <h3 class="card-header text-center font-weight-bold text-uppercase py-4">Editable table</h3>-->
   <!--   <div class="card-body">-->
   <!--     <div id="table" class="table-editable">-->
   <!--       <span class="table-add float-right mb-3 mr-2"><a href="#!" class="text-success"><i-->
   <!--             class="fas fa-plus fa-2x" aria-hidden="true"></i></a></span>-->
   <!--       <table class="table table-bordered table-responsive-md table-striped text-center">-->
   <!--         <thead>-->
   <!--           <tr>-->
   <!--             <th class="text-center">Category</th>-->
   <!--             <th class="text-center">Key Word</th>-->
   <!--             <th class="text-center">Sort</th>-->
   <!--             <th class="text-center">Remove</th>-->
   <!--           </tr>-->
   <!--         </thead>-->
   <!--         <tbody>-->
   <!--           <tr>-->
   <!--             <td class="pt-3-half" contenteditable="true">Aurelia Vega</td>-->
   <!--             <td class="pt-3-half" contenteditable="true">30</td>-->
   <!--             <td class="pt-3-half">-->
   <!--               <span class="table-up"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-up"-->
   <!--                     aria-hidden="true"></i></a></span>-->
   <!--               <span class="table-down"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-down"-->
   <!--                     aria-hidden="true"></i></a></span>-->
   <!--             </td>-->
   <!--             <td>-->
   <!--               <span class="table-remove"><button type="button"-->
   <!--                   class="btn btn-danger btn-rounded btn-sm my-0">Remove</button></span>-->
   <!--             </td>-->
   <!--           </tr>-->
              <!-- This is our clonable table line -->
   <!--           <tr>-->
   <!--             <td class="pt-3-half" contenteditable="true">Guerra Cortez</td>-->
   <!--             <td class="pt-3-half" contenteditable="true">45</td>-->
   <!--             <td class="pt-3-half">-->
   <!--               <span class="table-up"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-up"-->
   <!--                     aria-hidden="true"></i></a></span>-->
   <!--               <span class="table-down"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-down"-->
   <!--                     aria-hidden="true"></i></a></span>-->
   <!--             </td>-->
   <!--             <td>-->
   <!--               <span class="table-remove"><button type="button"-->
   <!--                   class="btn btn-danger btn-rounded btn-sm my-0">Remove</button></span>-->
   <!--             </td>-->
   <!--           </tr>-->
   <!--         </tbody>-->
   <!--       </table>-->
   <!--     </div>-->
   <!--   </div>-->
   <!-- </div>-->
  </section>
</template>
<!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>-->

<script>
import { mdbRow, mdbCol, mdbBtn, mdbCard, mdbView, mdbCardBody, mdbCardHeader, mdbCardText, mdbCardTitle, mdbIcon, mdbTbl, mdbBarChart, mdbPieChart, mdbLineChart, mdbRadarChart, mdbDoughnutChart, mdbListGroup, mdbListGroupItem, mdbBadge, mdbModal, mdbModalHeader, mdbModalTitle, mdbModalBody, mdbModalFooter } from 'mdbvue'
import {_} from 'vue-underscore'
export default {
  name: 'Dashboard',
  components: {
    mdbRow,
    mdbCol,
    mdbBtn,
    mdbCard,
    mdbView,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText,
    mdbCardTitle,
    mdbIcon,
    mdbTbl,
    mdbBarChart,
    mdbPieChart,
    mdbLineChart,
    mdbRadarChart,
    mdbDoughnutChart,
    mdbListGroup,
    mdbListGroupItem,
    mdbBadge,
    mdbModal,
    mdbModalHeader,
    mdbModalTitle,
    mdbModalBody,
    mdbModalFooter
  },
  data () {
    return {
      /* eslint-disable */
    // api: 'http://gbcsystem-ice-wolf.c9users.io:8082/',
    api: 'http://3.87.231.155:8082/',
     loading: 0,
     categorykeys: [],
     ClassifiercomponentKey: 0,
     loading: 0,
     article: {
          url: '',
          title: '',
          content: '',
          asource: '#',
          author: ''
      },
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
      barChartData: {
        labels: [],
        datasets: [
          {
            label: 'Weightings Of All Categories',
            data: [12, 39, 3, 50, 2, 32, 84, 64],
            backgroundColor: 'rgba(245, 74, 85, 0.5)',
            borderWidth: 1
          }
          // , {
          //   label: '#2',
          //   data: [56, 24, 5, 16, 45, 24, 8, 64],
          //   backgroundColor: 'rgba(90, 173, 246, 0.5)',
          //   borderWidth: 1
          // }, {
          //   label: '#3',
          //   data: [12, 25, 54, 3, 15, 44, 3, 40],
          //   backgroundColor: 'rgba(245, 192, 50, 0.5)',
          //   borderWidth: 1
          // }
        ]
      },
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            barPercentage: 1,
            gridLines: {
              display: true,
              color: 'rgba(0, 0, 0, 0.1)'
            }
          }],
          yAxes: [{
            gridLines: {
              display: true,
              color: 'rgba(0, 0, 0, 0.1)'
            },
            ticks: {
              beginAtZero: true
            }
          }]
        }
      },
      pieChartData: {
        labels: [],
        datasets: [
          {
            data: [],
            backgroundColor: ['#F7464A', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360', '#ac64ad'],
            hoverBackgroundColor: ['#FF5A5E', '#5AD3D1', '#FFC870', '#A8B3C5', '#616774', '#da92db']
          }
        ]
      },
      pieChartOptions: {
        responsive: true,
        maintainAspectRatio: false
      },
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
      ]
    }
  },
  created (){
        // console.log("Test");
        this.getcategorykeys();
       
          // this.getData(page);
  },
  /* eslint-disable */
  methods: 
  {
    classify: function()
    {
      this.loading =1;
      this.$http.post(this.api+'classifydata', {
          url:this.article.url,
          headers: {
              accepts: 'application/vnd.api+json'
          },
          ContentType: "application/json"
      }).then(function(data){
          if(data.body.message)
              console.log(data.body.message);
          else
              console.log(data);
          
          
          this.article.url = "";
          var temp =  _.values(data.body.categoriestop3);
          var i,total=0;
          this.pieChartData.labels =[]
          this.pieChartData.datasets[0].data=[]
          this.pieChartData.datasets[0].backgroundColor =[]
          this.pieChartData.datasets[0].hoverBackgroundColor =[]
          for(i=0;i<temp.length;i++)
          {
            console.log(temp[i][0])
            this.pieChartData.labels.push(temp[i][0])
            this.pieChartData.datasets[0].backgroundColor.push(this.allBackgroundColor[this.allCategories.indexOf(temp[i][0])])
            this.pieChartData.datasets[0].hoverBackgroundColor.push(this.allBackgroundColor[this.allCategories.indexOf(temp[i][0])])
            total +=temp[i][1]
            this.pieChartData.datasets[0].data.push(temp[i][1])
          }
          for(i=0;i<temp.length;i++)
          {
            this.pieChartData.datasets[0].data[i]=(temp[i][1]/total)*100
          }
          // window.pieChartData.update();
          // this.$refs.$forceUpdate()
          // console.log(this.pieChartData.datasets[0].data)
          // this.pieChartData.labels =temp
          this.article.content = data.body.document;
          this.article.asource = data.body.asource;
          
          this.barChartData.labels = _.keys(data.body.categories);
          console.log(this.barChartData.datasets[0]['data'] )
          this.barChartData.datasets[0]['data'] = _.values(data.body.categories);
          this.submitted = true;
          this.ClassifiercomponentKey +=1
          this.loading =0;
          
      });
    },
    getcategorykeys: function()
    {
      this.$http.get(this.api+'categorykeywords').then
      (function(data){
        console.log(data.body[0]);
        this.categorykeys = data.body;
        
      });
      
    }
    //,
    // getmodel: function()
    // {
    //   this.$http.get('http://gbcsystem-ice-wolf.c9users.io:8082/classificationmodel').then
    //   (function(data){
    //     console.log(data.body[0]);
    //     this.categorykeys = data.body;
        
    //   });
    // }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.cascading-admin-card {
  margin: 20px 0;
}
.cascading-admin-card .admin-up {
  margin-left: 4%;
  margin-right: 4%;
  margin-top: -20px;
}
.cascading-admin-card .admin-up .fas,
.cascading-admin-card .admin-up .far {
  box-shadow: 0 2px 9px 0 rgba(0, 0, 0, 0.2), 0 2px 13px 0 rgba(0, 0, 0, 0.19);
  padding: 1.7rem;
  font-size: 2rem;
  color: #fff;
  text-align: left;
  margin-right: 1rem;
  border-radius: 3px;
}
.cascading-admin-card .admin-up .data {
  float: right;
  margin-top: 2rem;
  text-align: right;
}
.admin-up .data p {
  color: #999999;
  font-size: 12px;
}
.classic-admin-card .card-body {
  color: #fff;
  margin-bottom: 0;
  padding: 0.9rem;
}
.classic-admin-card .card-body p {
  font-size: 13px;
  opacity: 0.7;
  margin-bottom: 0;
}
.classic-admin-card .card-body h4 {
  margin-top: 10px;
}
.gradient-card-header {
  padding: 1rem 1rem;
  text-align: center;
}
.pt-3-half {
padding-top: 1.4rem;
}
</style>
