<template>
  <section id="intro" class="wrapper style1 fullscreen fade-up">
    <div class="inner">
      <div class="host">
        <div class="container">
          <div>
            <h1>Список хостов</h1>
            <hr>
            <br><br>
            <div class="left">
              <button type="button" class="btn btn-success btn-sm" v-b-modal.host-modal
                      @click="getListOS">
                Добавить хост
              </button>
            </div>
            <div class="right">
              <button type="button" class="btn btn-success btn-sm" @click="goTo(picked.id)">
                Подробно
              </button>
              <button type="button"
                      class="btn btn-warning btn-sm"
                      v-b-modal.host-update-modal
                      @click="editHost(picked)">
                Обновить
              </button>
              <button type="button"
                      class="btn btn-danger btn-sm"
                      v-b-modal.host-delete-modal
                      @click="DeleteHost(picked)">
                Удалить
              </button>
            </div>
            <br><br>
            <alert :message=message v-if="showMessage"></alert>
            <table class="table-fill">
              <thead>
              <tr>
                <th scope="col"></th>
                <th scope="col">Name</th>
                <th scope="col">IP Address</th>
                <th scope="col">Operating system</th>
                <th scope="col">CPU</th>
                <th scope="col">CPUs</th>
                <th scope="col">RAM</th>
                <th scope="col">free RAM</th>
                <th scope="col">Vol. drive</th>
                <th scope="col">free drive</th>
                <th scope="col">RAID</th>
                <th scope="col">Description</th>
                <th scope="col">Inv Number</th>
              </tr>
              </thead>
              <tbody class="table-hover">
              <tr v-for="(host, index) in hosts" :key="index">
                <td><input type="radio" name="profile" id="one" :value="host" v-model="picked"></td>
                <td>{{ host.name }}</td>
                <td>{{ host.ip }}</td>
                <td>{{ host.os }}</td>
                <td>{{ host.cpu }}</td>
                <td>{{ host.amt_cpu }}</td>
                <td>{{ host.memory }} Gb</td>
                <td>{{ host.free_memory }} Gb</td>
                <td>{{ host.total_storage }} Gb</td>
                <td>{{ host.free_storage }} Gb</td>
                <td>{{ host.raid_controller }}</td>
                <td>{{ host.description }}</td>
                <td>{{ host.inv }}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
        <b-modal ref="addHostModal"
                 id="host-modal"
                 title="Add a new host"
                 hide-footer>
          <b-form @submit="Submit" @reset="Reset" class="w-100">
            <b-form-group id="form-name-group"
                          label="Name:"
                          label-for="form-name-input">
              <b-form-input id="form-name-input"
                            type="text"
                            v-model="addHostForm.name"
                            required
                            placeholder="Enter name host">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-ip-group"
                          label="IP address:"
                          label-for="form-ip-input">
              <b-form-input id="form-ip-input"
                            type="text"
                            v-model="addHostForm.ip"
                            required
                            placeholder="Enter ip address">
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-os-group"
                          label="Operating system:"
                          label-for="form-os-input">
              <b-form-select v-model="addHostForm.os">
                <b-form-select-option :value="null" disabled>Please select an OS
                </b-form-select-option>
                <b-form-select-option v-for="os in list_os" :value="os.id">{{ os.family }} {{
                    os.os
                  }} {{ os.capacity }}
                </b-form-select-option>
              </b-form-select>
            </b-form-group>

            <b-form-group id="form-cpu-group"
                          label="CPU:"
                          label-for="form-cpu-input">
              <b-form-input id="form-cpu-input"
                            type="text"
                            v-model="addHostForm.cpu"
                            required
                            placeholder="Enter cpu">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-amt_cpu-group"
                          label="Количество процессоров:"
                          label-for="form-amt_cpu-input">
              <b-form-select v-model="addHostForm.amt_cpu">
                <b-form-select-option :value="null" disabled>Количество процессоров
                </b-form-select-option>
                <b-form-select-option v-for="amt_cpu in list_amt_cpu" :value="amt_cpu.id">{{ amt_cpu.amt_cpu }}
                </b-form-select-option>
              </b-form-select>
            </b-form-group>
            <b-form-group id="form-memory-group"
                          label="Memory:"
                          label-for="form-memory-input">
              <b-form-input id="form-memory-input"
                            type="number"
                            v-model="addHostForm.memory"
                            required
                            placeholder="Enter memory">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-raid-controller-group"
                          label="RAID контроллер:"
                          label-for="form-raid-controller-input">
              <b-form-input id="form-raid-controller-input"
                            type="text"
                            v-model="addHostForm.raid_controller"
                            required
                            placeholder="Введите название RAID контроллера">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-description-group"
                          label="Description:"
                          label-for="form-description-input">
              <b-form-input id="form-description-input"
                            type="text"
                            v-model="addHostForm.description"
                            required
                            placeholder="Enter description">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-inv-group"
                          label="Foreign number:"
                          label-for="form-inv-input">
              <b-form-input id="form-inv-input"
                            type="text"
                            v-model="addHostForm.inv"
                            required
                            placeholder="Enter foreign number">
              </b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </b-modal>

        <b-modal ref="deleteHostModal"
                 id="host-delete-modal"
                 title="Delete host"
                 hide-footer>
          <b-form @submit="SubmitDelete" @reset="ResetDelete" class="w-100">
            <b-button type="submit" variant="primary">Delete</b-button>
            <b-button type="reset" variant="danger">Cancel</b-button>
          </b-form>
        </b-modal>

        <b-modal ref="editHostModal"
                 id="host-update-modal"
                 title="Update host"
                 hide-footer>
          <b-form @submit="SubmitUpdate" @reset="ResetUpdate" class="w-100">
            <b-form-group id="form-name-edit-group"
                          label="Name:"
                          label-for="form-name-edit-input">
              <b-form-input id="form-name-edit-input"
                            type="text"
                            v-model="editHostForm.name"
                            required
                            placeholder="Enter name">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-ip-edit-group"
                          label="IP address:"
                          label-for="form-ip-edit-input">
              <b-form-input id="form-ip-edit-input"
                            type="text"
                            v-model="editHostForm.ip"
                            required
                            placeholder="Enter ip address">
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-os-edit-group"
                          label="Operating system:"
                          label-for="form-os-edit-input">
              <b-form-select v-model="editHostForm.os">
                <template v-slot:first>
                  <b-form-select-option v-model="editHostForm.os" :value="editHostForm.os.id"
                                        disabled>{{ editHostForm.os }}
                  </b-form-select-option>
                </template>
                <b-form-select-option v-for="os in list_os"
                                      :value="os.id">
                  {{ os.family }} {{ os.os }} {{ os.capacity }}
                </b-form-select-option>
              </b-form-select>
            </b-form-group>

            <b-form-group id="form-cpu-edit-group"
                          label="CPU:"
                          label-for="form-cpu-edit-input">
              <b-form-input id="form-cpu-edit-input"
                            type="text"
                            v-model="editHostForm.cpu"
                            required
                            placeholder="Enter cpu">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-amt_cpu-edit-group"
                          label="Количество процессоров:"
                          label-for="form-amt_cpu-input">
              <b-form-select v-model="editHostForm.amt_cpu">
                <b-form-select-option :value="null" disabled>Количество процессоров
                </b-form-select-option>
                <b-form-select-option v-for="amt_cpu in list_amt_cpu" :value="amt_cpu.id">{{ amt_cpu.amt_cpu }}
                </b-form-select-option>
              </b-form-select>
            </b-form-group>
            <b-form-group id="form-memory-edit-group"
                          label="Memory:"
                          label-for="form-memory-edit-input">
              <b-form-input id="form-memory-edit-input"
                            type="number"
                            v-model="editHostForm.memory"
                            required
                            placeholder="Enter memory">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-raid-controller_edit-group"
                          label="RAID контроллер:"
                          label-for="form-raid-controller-input">
              <b-form-input id="form-raid-controller-input"
                            type="text"
                            v-model="editHostForm.raid_controller"
                            required
                            placeholder="Введите название RAID контроллера">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-description-edit-group"
                          label="Description:"
                          label-for="form-description-edit-input">
              <b-form-input id="form-description-edit-input"
                            type="text"
                            v-model="editHostForm.description"
                            required
                            placeholder="Enter description">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-inv-edit-group"
                          label="Foreign number:"
                          label-for="form-inv-edit-input">
              <b-form-input id="form-inv-edit-input"
                            type="text"
                            v-model="editHostForm.inv"
                            required
                            placeholder="Enter foreign number">
              </b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Update</b-button>
            <b-button type="reset" variant="danger">Cancel</b-button>
          </b-form>
        </b-modal>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import Alert from './Alert'

export default {
  name: "Host",
  data() {
    return {
      picked: {},
      hosts: [],
      addHostForm: {
        name: '',
        ip: '',
        os: null,
        cpu: '',
        memory: null,
        description: '',
        inv: '',
        raid_controller: '',
        amt_cpu: '',
      },
      editHostForm: {
        id: '',
        name: '',
        ip: '',
        os: null,
        cpu: '',
        memory: null,
        description: '',
        inv: '',
        raid_controller: '',
        amt_cpu: '',
      },
      deleteHostForm: {
        id: '',
      },
      list_os: [],
      list_amt_cpu: [],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getListHosts() {
      const path = `${this.$store.getters.getServerUrl}/list-host/`
      axios.get(path).then((res) => {
        this.hosts = res.data
      }).catch((error) => {
        console.error(error)
      })
          .then((response,) => {
            console.log(response)
          })
      this.getListCPU()
    },
    getListOS() {
      const path = `${this.$store.getters.getServerUrl}/list-os/`
      axios.get(path).then((res) => {
        this.list_os = res.data
      }).catch((error) => {
        console.error(error)
      })
          .then((response,) => {
            console.log(response)
          })
    },
    getListCPU() {
      const path = `${this.$store.getters.getServerUrl}/list-cpu/`
      axios.get(path).then((res) => {
        this.list_amt_cpu = res.data
      }).catch((error) => {
        console.error(error)
      })
          .then((response,) => {
            console.log(response)
          })
    },
    addHost(payload) {
      const path = `${this.$store.getters.getServerUrl}/add-host/`
      axios.post(path, payload)
          .then(() => {
            this.getListHosts()
            this.message = 'Host added!'
            this.showMessage = true
          })
          .catch((error) => {
            // eslint-отключение следующей строки
            console.log(error)
            this.getListHosts()
          });
    },
    initForm() {
      this.addHostForm.name = '';
      this.addHostForm.ip = '';
      this.addHostForm.os = 0;
      this.addHostForm.cpu = '';
      this.addHostForm.memory = 0;
      this.addHostForm.description = '';
      this.addHostForm.inv = '';
      this.addHostForm.raid_controller = '';
      this.addHostForm.amt_cpu = '';
      this.editHostForm.name = '';
      this.editHostForm.ip = '';
      this.editHostForm.os = 0;
      this.editHostForm.cpu = '';
      this.editHostForm.memory = 0;
      this.editHostForm.description = '';
      this.editHostForm.inv = '';
      this.editHostForm.raid_controller = '';
      this.editHostForm.amt_cpu = '';
    },
    Submit(evt) {
      evt.preventDefault()
      this.$refs['addHostModal'].hide()
      const payload = {
        name: this.addHostForm.name,
        ip: this.addHostForm.ip,
        os: this.addHostForm.os,
        cpu: this.addHostForm.cpu,
        memory: this.addHostForm.memory,
        description: this.addHostForm.description,
        inv: this.addHostForm.inv,
        raid_controller: this.addHostForm.raid_controller,
        amt_cpu: this.addHostForm.amt_cpu,
      }
      this.addHost(payload);
      this.initForm();
    },
    Reset(evt) {
      evt.preventDefault()
      this.$refs['addHostModal'].hide()
      this.initForm();
    },
    editHost(host) {
      this.editHostForm = host
      this.getListOS()
      console.log(this.host)
    },
    SubmitUpdate(evt) {
      evt.preventDefault()
      this.$refs['editHostModal'].hide()
      const payload = {
        name: this.editHostForm.name,
        ip: this.editHostForm.ip,
        os: this.editHostForm.os,
        cpu: this.editHostForm.cpu,
        memory: this.editHostForm.memory,
        description: this.editHostForm.description,
        inv: this.editHostForm.inv,
        raid_controller: this.editHostForm.raid_controller,
        amt_cpu: this.editHostForm.amt_cpu,
      }
      this.updateHost(payload, this.editHostForm.id)
    },
    updateHost(payload, hostID) {
      const path = `${this.$store.getters.getServerUrl}/update-host/${hostID}`
      axios.put(path, payload)
          //скорей свего не будет работать надо поменять get list на вызов отдельной функции
          .then(() => {
            this.getListHosts()
            this.message = 'Host updated!'
            this.showMessage = true
          })
          .catch((error) => {
            // eslint-отключение следующей строки
            console.error(error)
            this.getListHosts()
          });
    },
    ResetUpdate(evt) {
      evt.preventDefault();
      this.$refs['editHostModal'].hide();
      this.initForm();
      this.getListHosts();
    },
    removeHost(hostID) {
      const path = `${this.$store.getters.getServerUrl}/delete-host/${hostID}`
      axios.delete(path)
          .then(() => {
            this.getListHosts()
            this.message = 'Host removed!'
            this.showMessage = true
          })
          .catch((error) => {
            // eslint-отключение следующей строки
            console.error(error);
            this.getListHosts();
          });
    },
    DeleteHost(host) {
      this.deleteHostForm.id = host.id
      console.log(this.deleteHostForm.id)
    },
    ResetDelete(evt) {
      evt.preventDefault();
      this.$refs['deleteHostModal'].hide();
      // this.initForm();
      this.getListHosts();
    },
    SubmitDelete(evt) {
      evt.preventDefault()
      this.$refs['deleteHostModal'].hide()
      this.removeHost(this.deleteHostForm.id)
    },
    goTo(id) {
      this.$router.push({
        name: 'DetailHost',
        params: {id: id}
      })
    },
  },
  created() {
    this.getListHosts()
  }
};
</script>

<style scoped>
/*.col-sm-10 {*/
/*  max-width: 100%;*/
/*}*/

.container {
  max-width: 100%;
}

/*.row {*/
/*  margin-left: 7%;*/
/*}*/
</style>