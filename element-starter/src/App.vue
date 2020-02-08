<template>
<div id="app">
	<div>
		<el-row type="flex" justify="center"><el-col :xs="8" :sm="12" :md="16" :lg="14" :xl="20">
			<el-input 
  placeholder="Please input your keywords"
  v-model="search_words"
  clearable>
</el-input>
</el-col>
<el-col :xs="8" :sm="6" :md="4" :lg="3" :xl="1"><el-button @click="startHacking">Search</el-button></el-col>
		</el-row>
	<el-row>
    <el-radio-group row v-model="data_source_sel">
            <el-radio-button disabled label="Data Source"></el-radio-button>
      <el-radio-button label="US Financial News"></el-radio-button>
      <el-radio-button label="Japanese Wiki"></el-radio-button>
    </el-radio-group>
        <el-radio-group :disabled="isDisabled" v-model="field">
            <el-radio-button disabled label="Field"></el-radio-button>
      <el-radio-button label="Title"></el-radio-button>
      <el-radio-button label="Content"></el-radio-button>
    </el-radio-group>

        <el-radio-group v-model="engine_sel">
            <el-radio-button disabled label="Engine"></el-radio-button>
      <el-radio-button label="Python"></el-radio-button>
      <el-radio-button label="GETA"></el-radio-button>
    </el-radio-group>
	</el-row>
  <el-row>

        <el-radio-group :disabled="isDisabled" v-model="algorithm">
            <el-radio-button disabled label="Algorithm"></el-radio-button>
      <el-radio-button label="BM25F"></el-radio-button>
      <el-radio-button label="TF-IDF"></el-radio-button>
      <el-radio-button label="Frequency"></el-radio-button>
    </el-radio-group> Max results(Top N): 
    <el-input-number v-model="limit" :step="5"></el-input-number>

	</el-row>
    <el-row>           
      <table v-cloak class="table">
                  <thead class="thead-light">
                  <th>Title</th>
                  <th>Score</th>
                  <th>URL</th>
                  <th>UUID</th>
                  </thead>
                  <tbody>
                  <tr v-for="(result,i) in search_results" :key="i">
                      <td>
    <el-link :disabled="isDisabled" type="primary" @click="open(result)"><font color="#4C8FDF">{{result.title}}</font></el-link></td>
                      <td>{{result.score}}</td>
                      <td><a :href="result.url">{{result.url}}</a></td>
                      <td>{{result.uuid}}</td>
                  </tr>
                  </tbody>
              </table></el-row>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      limit:5,
      search_time:"",
      hits:"",
      response_data:null,
      search_results:null,
      engine_sel: "",
      data_source_sel: "",
      field: "",
	  algorithm: "",
	  search_words:""
    };
  },
  computed: {
    isDisabled() {
      if (this.engine_sel === "GETA") {
        return true;
      } else {
        return false;
      }
    }
  },
  created(){
  },
  methods: {
          open(context) {
        this.$alert(context.content, context.title, {
          confirmButtonText: 'Dismiss'
        });
      },
    startHacking() {
      this.$axios.get("data.json", {
    params: {
      search_engine:this.engine_sel,
      data_source:this.data_source_sel,
      key_words:this.search_words,
      limit:this.limit,
      search_algorithm:this.algorithm,
      fields:this.field
    }
  }).then(response => {
        self.response_data = response.data;
                this.hits = response_data.hits;
        this.search_time = response_data.runtime;
        this.search_results = response_data.search_results;
              this.$notify({
        title: "Search successful!",
        type: "success",
        message:
          "Got "+this.hits+" hits in "+this.search_time+"s",
        duration: 5000
      });
      });



    }
  }
};
</script>

<style>

[v-cloak] {
  display: none;
}

.el-input-number{
  margin-left: 10px;
}
.el-radio-group{
  margin-right: 30px;
}
.el-message-box{
  width:800px;
}
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 2px;
  }
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}

</style>
