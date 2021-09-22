<template>
    <div v-show="false">
        <!-- <van-count-down :time="time" /> -->
        <!-- <div style="margin: 20px 0;"></div> -->
        <van-field
            v-model="authorization"
            rows="1"
            autosize
            label="authorization:"
            type="textarea"
            placeholder="请输入"
            />
    </div>
</template>
<script>
import axios from 'axios'

export default {
  data () {
    return {
      authorization: ''
    }
  },
  methods: {
    handlerAuth () {
      this.$emit('event', this.authorization)
    },
    async getAuth () {
      var res = ''
      await axios({
        method: 'get',
        url: '/getAuth'
        // timeout: 1000
      })
        .then(function (response) {
          console.log(response.request.response)
          res = response.request.response
        //   this.authorization = response.request.response
        })
        .catch(function (error) {
          console.log(error)
        })
      return res
    },
    async getAuthAndEmit () {
      await this.getAuth().then(res => { this.authorization = res })
      this.handlerAuth()
    }
  },
  async mounted () {
    await this.getAuth().then(res => {
      this.authorization = res
    })
    this.handlerAuth()
    // console.log('***********************************************')
    console.log(this.authorization, 'mounted')
  }
}
</script>
