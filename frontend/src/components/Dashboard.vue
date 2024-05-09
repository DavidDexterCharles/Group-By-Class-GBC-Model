<template>
  <section id="dashboard">
    <mdb-row>
      <mdb-col md="12">
        <mdb-card cascade narrow class="mt-5">
          <mdb-view class="gradient-card-header blue darken-2">
            <h4 class="h4-responsive text-white">Classifier</h4>
            <a
              href="http://3.87.231.155:8082/classificationmodel"
              target="_blank"
              class="text-white"
            >
              <u><b>View Classification Model</b></u>
            </a>
          </mdb-view>
          <mdb-card-body v-bind:key="ClassifiercomponentKey">
            <!-- Input section -->
            <div class="input-group md-form form-sm form-2 pl-0">
              <input
                class="form-control my-0 py-1 lime-border"
                v-model="article.url"
                v-on:keyup.enter="classify"
                type="text"
                placeholder="Takes both TEXT and URL as input (extracts content from web page where URL provided)"
                aria-label="Search"
              />
              <div class="input-group-append">
                <span
                  v-on:click.prevent="classify"
                  class="input-group-text lime lighten-2"
                  id="basic-text1"
                >
                  <i class="fas fa-dot-circle text-grey" aria-hidden="true"></i>
                </span>
              </div>
              <div class="d-flex justify-content-center" v-if="loading">
                <div
                  class="spinner-border center"
                  style="width: 3rem; height: 3rem;"
                  role="status"
                >
                  <span class="sr-only">Loading...</span>
                </div>
              </div>
            </div>

            <!-- Top 3 Categories -->
            <mdb-card class="mb-4" v-if="submitted">
              <mdb-card-header class="text-center"
                >Top 3 Categories</mdb-card-header
              >
              <mdb-card-body>
                <div style="display: block">
                  <mdb-pie-chart
                    v-bind:key="ClassifiercomponentKey"
                    :data="pieChartData"
                    :options="pieChartOptions"
                    :height="200"
                  />
                </div>
              </mdb-card-body>
            </mdb-card>

            <!-- All Categories and Weightings -->
            <mdb-card class="mb-4" v-if="submitted">
              <mdb-card-header class="text-center"
                >All categories and Weightings</mdb-card-header
              >
              <mdb-card-body>
                <div style="display: block">
                  <mdb-bar-chart
                    v-bind:key="ClassifiercomponentKey"
                    :data="barChartData"
                    :options="barChartOptions"
                    :height="500"
                  />
                </div>
              </mdb-card-body>
            </mdb-card>

            <!-- Document Content -->
            <mdb-card
              class="card-body"
              style=" margin-top: 1rem;"
              v-if="submitted"
            >
              <mdb-card-title>Document Content</mdb-card-title>
              <mdb-card-text>{{ article.content }}</mdb-card-text>
              <div class="flex-row">
                <p>SOURCE: {{ article.asource }}</p>
              </div>
            </mdb-card>
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
import {
  mdbRow,
  mdbCol,
  mdbCard,
  mdbView,
  mdbCardBody,
  mdbCardHeader,
  mdbCardText,
  mdbCardTitle,
  mdbPieChart,
  mdbBarChart
} from "mdbvue";

export default {
  name: "Dashboard",
  components: {
    mdbRow,
    mdbCol,
    mdbCard,
    mdbView,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText,
    mdbCardTitle,
    mdbPieChart,
    mdbBarChart
  },
  data() {
    return {
      api: "http://127.0.0.1:8084/",
      loading: false,
      ClassifiercomponentKey: 0,
      article: {
        url: "",
        content: "",
        asource: "#",
        author: ""
      },
      submitted: false,
      barChartData: {},
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              barPercentage: 1,
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)"
              }
            }
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)"
              },
              ticks: {
                beginAtZero: true
              }
            }
          ]
        }
      },
      pieChartData: {},
      allCategories: [],
      allBackgroundColor: []
    };
  },
  methods: {
    classify() {
      this.loading = true;
      this.$http
        .get(`${this.api}dummydata`)
        .then(response => {
          const data = response.data;
          this.pieChartData = data.pieChartData;
          this.barChartData = data.barChartData;
          this.submitted = true;
          this.ClassifiercomponentKey++;
          this.loading = false;
        })
        .catch(error => {
          console.error("Error fetching dummy data:", error);
          this.loading = false;
        });
    }
  }
};
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
