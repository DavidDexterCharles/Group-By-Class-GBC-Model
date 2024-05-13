<template>
  <section id="articles">
    <mdb-row>
      <mdb-col md="12">
        <mdb-card cascade narrow class="mt-5">
          <mdb-view class="gradient-card-header blue darken-2">
            <h4 class="h4-responsive text-white">Articles</h4>
          </mdb-view>
          <mdb-card-body
            class="sticky-top"
            style="padding-top:29px;backgroundColor:white;"
          >
            <div class="input-group md-form form-sm form-2 pl-0">
              <input
                class="form-control my-0 py-1 lime-border"
                v-model="searchQuery"
                @input="searchData"
                type="text"
                :placeholder="'Search by ' + searchoption"
                aria-label="Search"
              />
              <!-- <input
                class="form-control my-0 py-1 lime-border"
                v-model="searchQuery"
                @keyup.enter="searchData"
                type="text"
                :placeholder="'Search by ' + searchoption"
                aria-label="Search"
              /> -->
              <select
                v-model="searchoption"
                class="btn btn-danger btn-sm dropdown-toggle"
                slot="toggle"
              >
                <option
                  v-for="option in searchoptions"
                  :key="option"
                  :value="option"
                  >{{ option }}</option
                >
              </select>
            </div>
            <div>
              <b
                >Total:
                <span style="color:red;">{{
                  // filteredResources.length
                  articles.length
                }}</span></b
              >
              <span></span>
              <b>
                <span style="color:red;">{{
                  // filteredResources.length
                  max_category
                }}</span></b
              >
            </div>
            <div class="input-group-append">
              <button
                @click="addPage"
                class="btn btn-md btn-secondary m-0 px-3 right"
                type="button"
                id="MaterialButton-addon2"
              >
                More Articles
              </button>
            </div>
            <div class="d-flex justify-content-center" v-if="loading">
              <div
                class="spinner-border center"
                style="width: 8rem; height: 8rem;"
                role="status"
              >
                <span class="sr-only">Loading...</span>
              </div>
            </div>
          </mdb-card-body>
          <mdb-card-body :key="ArticlescomponentKey">
            <div class="input-group md-form form-sm form-2 pl-0">
              <table v-if="articles.length" class="table">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Content</th>
                    <th>Categories</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="article in articles" :key="article._id">
                    <td>
                      <a
                        :href="article.source"
                        target="_blank"
                        style="color:blue;"
                        >{{ article.title }}</a
                      >
                    </td>
                    <td>{{ article.content }}</td>
                    <td>
                      <div style="width:200px;">
                        <!-- Render categories here -->
                        <span v-if="article.categories.length > 0">
                          <!-- {{ article.categories.join(", ") }} -->
                          {{ article.category_weights }}
                        </span>
                        <span v-else>No categories</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
import {
  mdbDropdown,
  mdbCard,
  mdbView,
  mdbRow,
  mdbCol,
  mdbCardBody
} from "mdbvue";
import { _ } from "vue-underscore";

export default {
  name: "Articles",
  components: { mdbDropdown, mdbCard, mdbView, mdbRow, mdbCol, mdbCardBody },
  data() {
    return {
      api: "http://127.0.0.1:8084/",
      searchoption: "Article Content",
      searchoptions: ["Article Content", "Article Category"],
      ArticlescomponentKey: 0,
      loading: false,
      articles: [],
      max_category: "",
      numarticles: 0,
      numpages: "",
      maxpages: 1,
      searchQuery: "",
      resources: []
    };
  },
  // computed: {
  //   filteredResources() {
  //     if (this.searchQuery) {
  //       return this.articles.filter(article => {
  //         const searchString = this.searchQuery.toLowerCase();
  //         if (this.searchoption === "Article Content") {
  //           return article.content.toLowerCase().includes(searchString);
  //           // const articles = await this.searchData(searchString);
  //           // return articles;
  //         } else {
  //           // Search in categories
  //           return article.categories.some(category =>
  //             category.toLowerCase().includes(searchString)
  //           );
  //         }
  //       });
  //     } else {
  //       return this.articles;
  //     }
  //   }
  // },
  created() {
    this.getData(1);
  },
  methods: {
    getData(page) {
      this.loading = true;
      this.$http.get(`${this.api}getarticles?page=${page}`).then(data => {
        console.log(data.body);
        this.articles = data.body;
        this.loading = false;
      });
    },
    async searchData() {
      this.loading = true;
      try {
        const response = await this.$http.get(
          `${this.api}getarticles_search?search_query=${this.searchQuery}`
        );
        this.articles = response.data.result;
        this.max_category = response.data.max_category;
        this.loading = false;
        console.log(this.articles);
        return this.articles;
      } catch (error) {
        console.error("Error fetching articles:", error);
        this.loading = false;
      }
    },
    addPage() {
      const page = this.maxpages + 1;
      if (this.maxpages <= this.numpages) {
        this.getData(page);
        this.maxpages = page;
        this.ArticlescomponentKey += 1;
      } else {
        alert("No More Articles");
      }
    }
  }
};
</script>

<style scoped>
.profile-card-footer {
  background-color: #f7f7f7 !important;
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
