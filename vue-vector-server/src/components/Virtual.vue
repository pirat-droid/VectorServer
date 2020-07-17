<template>
    <div class="host">
        <div class="container">
            <div class="row">
                <div class="col-sm-10">
                    <p>
                        <router-link to="/">List Host</router-link>
                    </p>
                    <p>
                        <router-link to="/list-storage">List Storage</router-link>
                    </p>
                    <p>
                        <router-link to="/list-operating-system">List Operating system</router-link>
                    </p>
                    <h1>List VM</h1>
                    <hr>
                    <br><br>
                    <button type="button" class="btn btn-success btn-sm" v-b-modal.vm-modal @click="getListOS">Add
                        VM
                    </button>
                    <br><br>
                    <alert :message=message v-if="showMessage"></alert>
                    <table>
                        <thead>
                        <tr>
                            <th scope="col">Name</th>
                            <th scope="col">IP Address</th>
                            <th scope="col">Host</th>
                            <th scope="col">Operating system</th>
                            <th scope="col">Cores</th>
                            <th scope="col">Threads</th>
                            <th scope="col">Storage size</th>
                            <th scope="col">Memory</th>
                            <th scope="col">Description</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(vm, index) in virtuals" :key="index">
                            <td>{{ vm.name }}</td>
                            <td>{{ vm.ip }}</td>
                            <td>{{ vm.host }}</td>
                            <td>{{ vm.os }}</td>
                            <td>{{ vm.cores }}</td>
                            <td>{{ vm.threads }}</td>
                            <td>{{ vm.storage_size }} Gb</td>
                            <td>{{ vm.memory }} Gb</td>
                            <td>{{ vm.description }}</td>
                            <td>
                                <button type="button"
                                        class="btn btn-warning btn-sm"
                                        v-b-modal.vm-update-modal
                                        @click="editVM(vm)">
                                    Update
                                </button>
                                <button type="button"
                                        class="btn btn-danger btn-sm"
                                        v-b-modal.vm-delete-modal
                                        @click="DeleteVM(vm)">
                                    Delete
                                </button>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <b-modal ref="addVMModal"
                 id="vm-modal"
                 title="Update a new virtual machine"
                 hide-footer>
            <b-form @submit="Submit" @reset="Reset" class="w-100">
                <b-form-group id="form-name-group"
                              label="Name:"
                              label-for="form-name-input">
                    <b-form-input id="form-name-input"
                                  type="text"
                                  v-model="addVMForm.name"
                                  required
                                  placeholder="Enter name virtual machine">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-ip-group"
                              label="IP address:"
                              label-for="form-ip-input">
                    <b-form-input id="form-ip-input"
                                  type="text"
                                  v-model="addVMForm.ip"
                                  required
                                  placeholder="Enter ip address">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-host-group"
                              label="Host:"
                              label-for="form-host-input">
                    <b-form-select v-model="addVMForm.host">
                        <b-form-select-option :value="null"
                                              disabled>
                            Please select an host
                        </b-form-select-option>
                        <b-form-select-option v-for="host in hosts"
                                              :value="host.id">
                            {{ host.name }} - {{ host.os }} - {{ host.ip}}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-form-group id="form-os-group"
                              label="Operating system:"
                              label-for="form-os-input">
                    <b-form-select v-model="addVMForm.os">
                        <template v-slot:first>
                            <b-form-select-option :value="null"
                                                  disabled>
                                Please select an OS
                            </b-form-select-option>
                        </template>
                        <b-form-select-option v-for="os in list_os"
                                              :value="os.id">
                            {{ os.family }} {{ os.os }} {{ os.capacity }}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-form-group id="form-cores-group"
                              label="Cores:"
                              label-for="form-cores-input">
                    <b-form-input id="form-cores-input"
                                  type="number"
                                  v-model="addVMForm.cores"
                                  required
                                  placeholder="Enter cores">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-threads-group"
                              label="Threads:"
                              label-for="form-threads-input">
                    <b-form-input id="form-threads-input"
                                  type="number"
                                  v-model="addVMForm.threads"
                                  required
                                  placeholder="Enter threads">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-storage-size-group"
                              label="Storage size:"
                              label-for="form-storage-size-input">
                    <b-form-input id="form-storage-size-input"
                                  type="number"
                                  v-model="addVMForm.storage_size"
                                  required
                                  placeholder="Enter storage size">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-memory-group"
                              label="Memory:"
                              label-for="form-memory-input">
                    <b-form-input id="form-memory-input"
                                  type="number"
                                  v-model="addVMForm.memory"
                                  required
                                  placeholder="Enter memory">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-description-group"
                              label="Description:"
                              label-for="form-description-input">
                    <b-form-input id="form-description-input"
                                  type="text"
                                  v-model="addVMForm.description"
                                  required
                                  placeholder="Enter description">
                    </b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="editVMModal"
                 id="vm-update-modal"
                 title="Update a new virtual machine"
                 hide-footer>
            <b-form @submit="SubmitUpdate" @reset="ResetUpdate" class="w-100">
                <b-form-group id="form-name-edit-group"
                              label="Name:"
                              label-for="form-name-input">
                    <b-form-input id="form-name-input"
                                  type="text"
                                  v-model="editVMForm.name"
                                  required
                                  placeholder="Enter name virtual machine">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-ip-edit-group"
                              label="IP address:"
                              label-for="form-ip-input">
                    <b-form-input id="form-ip-input"
                                  type="text"
                                  v-model="editVMForm.ip"
                                  required
                                  placeholder="Enter ip address">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-host-edit-group"
                              label="Host:"
                              label-for="form-host-input">
                    <b-form-select v-model="editVMForm.host">
                        <b-form-select-option :value="null"
                                              disabled>
                            Please select an host
                        </b-form-select-option>
                        <b-form-select-option v-for="host in hosts"
                                              :value="host.id">
                            {{ host.name }} - {{ host.os }} - {{ host.ip}}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-form-group id="form-os-edit-group"
                              label="Operating system:"
                              label-for="form-os-input">
                    <b-form-select v-model="editVMForm.os">
                        <template v-slot:first>
                            <b-form-select-option :value="null"
                                                  disabled>
                                Please select an OS
                            </b-form-select-option>
                        </template>
                        <b-form-select-option v-for="os in list_os"
                                              :value="os.id">
                            {{ os.family }} {{ os.os }} {{ os.capacity }}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-form-group id="form-cores-edit-group"
                              label="Cores:"
                              label-for="form-cores-input">
                    <b-form-input id="form-cores-input"
                                  type="number"
                                  v-model="editVMForm.cores"
                                  required
                                  placeholder="Enter cores">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-threads-edit-group"
                              label="Threads:"
                              label-for="form-threads-input">
                    <b-form-input id="form-threads-input"
                                  type="number"
                                  v-model="editVMForm.threads"
                                  required
                                  placeholder="Enter threads">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-storage-size-edit-group"
                              label="Storage size:"
                              label-for="form-storage-size-input">
                    <b-form-input id="form-storage-size-input"
                                  type="number"
                                  v-model="editVMForm.storage_size"
                                  required
                                  placeholder="Enter storage size">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-memory-edit-group"
                              label="Memory:"
                              label-for="form-memory-input">
                    <b-form-input id="form-memory-input"
                                  type="number"
                                  v-model="editVMForm.memory"
                                  required
                                  placeholder="Enter memory">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-description-edit-group"
                              label="Description:"
                              label-for="form-description-input">
                    <b-form-input id="form-description-input"
                                  type="text"
                                  v-model="editVMForm.description"
                                  required
                                  placeholder="Enter description">
                    </b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="deleteVMModal"
                 id="vm-delete-modal"
                 title="Delete host"
                 hide-footer>
            <b-form @submit="SubmitDelete" @reset="ResetDelete" class="w-100">
                <b-button type="submit" variant="primary">Delete</b-button>
                <b-button type="reset" variant="danger">Cancel</b-button>
            </b-form>
        </b-modal>

    </div>
</template>

<script>
    import axios from 'axios'
    import Alert from './Alert'

    export default {
        name: "Virtual",
        data() {
            return {
                virtuals: [],
                addVMForm: {
                    name: '',
                    ip: '',
                    os: null,
                    cors: '',
                    threads: '',
                    memory: '',
                    description: '',
                    host: null,
                    storage_size: '',
                },
                editVMForm: {
                    id: '',
                    name: '',
                    ip: '',
                    os: null,
                    cores: '',
                    memory: '',
                    description: '',
                    host: null,
                    threads: '',
                    storage_size: '',
                },
                DeleteVMForm: {
                    id: '',
                },
                list_os: [],
                hosts: [],
                message: '',
                showMessage: false,
            };
        },
        components: {
            alert: Alert,
        },
        methods: {
            getListVM() {
                const path = `${this.$store.getters.getServerUrl}/list-vm/`
                axios.get(path).then((res) => {
                    this.virtuals = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(response)
                    })
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
                this.getListHosts()
            },
            getListHosts() {
                const path = `${this.$store.getters.getServerUrl}/list-select-host/`
                axios.get(path).then((res) => {
                    this.hosts = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(response)
                    })
            },
            addVM(payload) {
                const path = `${this.$store.getters.getServerUrl}/add-vm/`
                axios.post(path, payload)
                    .then(() => {
                        this.getListVM()
                        this.message = 'Virtual machine added!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.log(error)
                        this.getListVM()
                    });
            },
            initForm() {
                this.addVMForm.name = '';
                this.addVMForm.ip = '';
                this.addVMForm.os = '';
                this.addVMForm.cores = '';
                this.addVMForm.memory = '';
                this.addVMForm.description = '';
                this.addVMForm.host = '';
                this.addVMForm.threads = '';
                this.addVMForm.storage_size = '';
                this.editVMForm.name = '';
                this.editVMForm.ip = '';
                this.editVMForm.os = '';
                this.editVMForm.cores = '';
                this.editVMForm.threads = '';
                this.editVMForm.memory = '';
                this.editVMForm.description = '';
                this.editVMForm.host = '';
                this.editVMForm.storage_size = '';
            },
            Submit(evt) {
                evt.preventDefault()
                this.$refs['addVMModal'].hide()
                const payload = {
                    name: this.addVMForm.name,
                    ip: this.addVMForm.ip,
                    os: this.addVMForm.os,
                    cores: this.addVMForm.cores,
                    memory: this.addVMForm.memory,
                    description: this.addVMForm.description,
                    threads: this.addVMForm.threads,
                    host: this.addVMForm.host,
                    storage_size: this.addVMForm.storage_size,
                }
                this.addVM(payload);
                this.initForm();
            },
            Reset(evt) {
                evt.preventDefault()
                this.$refs['addVMModal'].hide()
                this.initForm();
            },
            editVM(vm) {
                this.editVMForm = vm
                this.getListOS()
                console.log(this.vm)
            },
            SubmitUpdate(evt) {
                evt.preventDefault()
                this.$refs['editVMModal'].hide()
                const payload = {
                    name: this.editVMForm.name,
                    ip: this.editVMForm.ip,
                    os: this.editVMForm.os,
                    cores: this.editVMForm.cores,
                    memory: this.editVMForm.memory,
                    description: this.editVMForm.description,
                    threads: this.editVMForm.threads,
                    host: this.editVMForm.host,
                    storage_size: this.editVMForm.storage_size,
                }
                this.updateVM(payload, this.editVMForm.id)
            },
            updateVM(payload, VMID) {
                const path = `${this.$store.getters.getServerUrl}/update-vm/${VMID}`
                axios.put(path, payload)
                    //скорей свего не будет работать надо поменять get list на вызов отдельной функции
                    .then(() => {
                        this.getListVM()
                        this.message = 'Virtual machine updated!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error)
                        this.getListVM()
                    });
            },
            ResetUpdate(evt) {
                evt.preventDefault();
                this.$refs['editVMModal'].hide();
                this.initForm();
                this.getListVM();
            },
            removeVM(hostID) {
                const path = `${this.$store.getters.getServerUrl}/delete-vm/${hostID}`
                axios.delete(path)
                    .then(() => {
                        this.getListVM()
                        this.message = 'Virtual machine removed!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error);
                        this.getListVM();
                    });
            },
            DeleteVM(vm) {
                this.DeleteVMForm.id = vm.id
                console.log(this.DeleteVMForm.id)
            },
            ResetDelete(evt) {
                evt.preventDefault();
                this.$refs['deleteVMModal'].hide();
                // this.initForm();
                this.getListVM();
            },
            SubmitDelete(evt) {
                evt.preventDefault()
                this.$refs['deleteVMModal'].hide()
                this.removeVM(this.DeleteVMForm.id)
            },
        },
        created() {
            this.getListVM()
        }
    };
</script>

<style scoped>

</style>