<template>
    <div>
      <van-grid square :gutter="10" direction="horizontal" :column-num='5' :border='true'>
        <van-grid-item @click="handlerItem(index,portItem)" class='van_grid_item' v-for="(portItem,index) in datalist.port" :key="index+portItem.chargeId" icon="" :text="String(portItem.chargeId+','+index)" >
                <div>
                  <div v-if="(portCurr==index)&portItem.state==0">选中</div>
                  <div v-else-if="portItem.state==0 && !portItem.errMsg" class="stopCharging">空闲</div>
                  <div v-else-if="portItem.state==0 && portItem.errMsg" class="offline">离线</div>
                  <div v-else-if="portItem.state==2" class="charging">
                    <div>
                      <!-- {{realPortTimeUsed (portItem.realPortTimeUsed,index)}} -->
                      <!-- <slot></slot> -->
                      <Time :time="Number(portItem.realPortTimeUsed)" ref="headerChild"></Time>
                      <!-- {{seconds[index]}} -->
                    </div>
                    充电
                  </div>
                </div>
        </van-grid-item>
      </van-grid>
      <!-- {{equipmentNo}} -->
    </div>
</template>
<script>
import axios from 'axios'
import Time from '@/components/timerUp.vue'

export default {
  data () {
    return {
      greeting: 'Hello World!',
      datalist: {},
      seconds: [],
      timeUsed: 0,
      portCurr: -1
    }
  },
  components: {
    Time
  },
  computed: {

  },
  props: {
    equipmentNo: {
      type: String,
      default: ''
    }
  },
  methods: {
    realPortTimeUsed (second, index) {
      this.seconds[index] = second
      // var second = 123
      // const days = Math.floor(second / 86400)
      var hours = Math.floor((second % 86400) / 3600)
      var minutes = Math.floor(((second % 86400) % 3600) / 60)
      var seconds = Math.floor(((second % 86400) % 3600) % 60)
      if (hours < 10) {
        hours = '0' + hours
      }
      if (minutes < 10) {
        minutes = '0' + minutes
      }
      if (seconds < 10) {
        seconds = '0' + seconds
      }
      // setInterval(() => {
      //   for (let i = 0; i < 10; i++) {
      //     this.seconds[index]--
      //     console.log(this.seconds[index])
      //     this.timeUsed++
      //   }
      // }, 1000)
      return hours + ':' + minutes + ':' + seconds
    },

    handlerItem (index, portItem) {
      console.log('点击了', portItem.state, index)
      this.portCurr = index
      if (portItem.state === 0) {
        // bus.$emit()
        // console.log('点击了', portItem.state, index)
        this.$emit('event', index, this.datalist)
      }
    },
    async getDevicePortStatus (equipmentNo) {
      console.log(this.equipmentNo, equipmentNo, 'devicePortStatu.vue 94行', equipmentNo || this.equipmentNo)
      // 不知什么原因这里的this.equipmentNo用的是上次的this.equipmentNo 所以用(equipmentNo || this.equipmentNo)解决这个问题
      await axios.get('/query?device_num=' + (equipmentNo || this.equipmentNo) + '&company_id=2')
        .then(res => { console.log(res.data.data); this.datalist = res.data.data })
      for (let index = 0; index < this.datalist.length; index++) {
        this.seconds[index] = this.datalist[index].realPortTimeUsed
        console.log(this.datalist[index].realPortTimeUsed)
      }
      console.log(this.seconds)
    }
  },
  watch: {

  },
  async mounted () {
    // fetch('/query?device_num=18201954&company_id=2')
    //   .then(res => res.json)
    //   .then(res => { console.log(res) })
    //   .catch(err => { console.log(err) })
    // await this.getDevicePortStatus()
    this.$emit('event1')
    setInterval(() => {
      this.$emit('event1')
      // this.getDevicePortStatus()
    }, 2800)
  }
}
</script>
<style scoped>
.charging{
  font-size: 10px;
  color: red;
  /* width: ; */
  /* background-color: blueviolet; */
}
.stopCharging{
  font-size: 10px;
  color: green;
  /* width: ; */
  /* background-color: blueviolet; */
}
.offline{
  font-size: 10px;
  color: #FF7F50;
}
</style>
