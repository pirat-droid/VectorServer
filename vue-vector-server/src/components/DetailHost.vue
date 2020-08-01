<template>
    <section id="intro" class="wrapper style1 fullscreen fade-up">
        <div class="inner">
            <div class="host">
                <div class="container">
                    <div class="row">
                        <div class="col-sm-10">
                            <h1>Host name: {{ host.name }}</h1>
                            <hr>
                            <br><br>
                            <alert :message=message v-if="showMessage"></alert>
                            <table>
                                <thead>
                                <tr>
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
                                    <th scope="col">serial_number Number</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
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
                                    <td>{{ host.serial_number }}</td>
                                    <td>
                                        <button type="button"
                                                class="btn btn-warning btn-sm"
                                                v-b-modal.host-update-modal
                                                @click="editHost(host)">
                                            Update
                                        </button>
                                    </td>
                                    <td>
                                        <button type="button"
                                                class="btn btn-danger btn-sm"
                                                v-b-modal.host-delete-modal
                                                @click="DeleteHost(host)">
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <h1>Host virtual machines list:</h1>
                            <hr>
                            <br><br>
                            <table>
                                <thead>
                                <tr>
                                    <th scope="col">Name</th>
                                    <th scope="col">IP Address</th>
                                    <th scope="col">Operating system</th>
                                    <th scope="col">Cores</th>
                                    <th scope="col">Threads</th>
                                    <th scope="col">Memory</th>
                                    <th scope="col">Storage size</th>
                                    <th scope="col">Description</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="(vm, index) in host.virtuals" :key="index">
                                    <td>{{ vm.name }}</td>
                                    <td>{{ vm.ip }}</td>
                                    <td>{{ vm.os }}</td>
                                    <td>{{ vm.cores }}</td>
                                    <td>{{ vm.threads }}</td>
                                    <td>{{ vm.memory }} Gb</td>
                                    <td>{{ vm.storage_size }} Gb</td>
                                    <td>{{ vm.description }}</td>
                                    <td>
                                        <button type="button"
                                                class="btn btn-warning btn-sm"
                                                v-b-modal.vm-update-modal
                                                @click="editVM(vm)">
                                            Update
                                        </button>
                                    </td>
                                    <td>
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
                            <h1>Host drive list:</h1>
                            <hr>
                            <br><br>
                            <table>
                                <thead>
                                <tr>
                                    <th scope="col">Model</th>
                                    <th scope="col">Storage volume</th>
                                    <th scope="col">Storage type</th>
                                    <th scope="col">s/n</th>
                                    <th scope="col">Date install</th>
                                    <th scope="col">Description</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="(Storage, index) in host.storage" :key="index">
                                    <td>{{ Storage.model }}</td>
                                    <td>{{ Storage.size_storage }}</td>
                                    <td>{{ Storage.type_storage }}</td>
                                    <td>{{ Storage.serial_number }}</td>
                                    <td>{{ Storage.date_install }}</td>
                                    <td>{{ Storage.description }}</td>

                                    <td>
                                        <button type="button"
                                                class="btn btn-warning btn-sm"
                                                v-b-modal.Storage-update-modal
                                                @click="editStorage(Storage)">
                                            Update
                                        </button>
                                    </td>
                                    <td>
                                        <button type="button"
                                                class="btn btn-danger btn-sm"
                                                v-b-modal.Storage-delete-modal
                                                @click="DeleteStorage(Storage)">
                                            Deletes
                                        </button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>

                        </div>
                    </div>
                </div>
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
                        <b-form-group id="form-serial_number-edit-group"
                                      label="Foreign number:"
                                      label-for="form-serial_number-edit-input">
                            <b-form-input id="form-serial_number-edit-input"
                                          type="text"
                                          v-model="editHostForm.serial_number"
                                          required
                                          placeholder="Enter foreign number">
                            </b-form-input>
                        </b-form-group>
                        <b-button type="submit" variant="primary">Update</b-button>
                        <b-button type="reset" variant="danger">Cancel</b-button>
                    </b-form>
                </b-modal>
                <b-modal ref="editVMModal"
                         id="vm-update-modal"
                         title="Update a virtual machine"
                         hide-footer>
                    <b-form @submit="SubmitUpdateVM" @reset="ResetUpdateVM" class="w-100">
                        <b-form-group id="form-vm-name-edit-group"
                                      label="Name:"
                                      label-for="form-name-input">
                            <b-form-input id="form-name-input"
                                          type="text"
                                          v-model="editVMForm.name"
                                          required
                                          placeholder="Enter name virtual machine">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-vm-ip-edit-group"
                                      label="IP address:"
                                      label-for="form-ip-input">
                            <b-form-input id="form-ip-input"
                                          type="text"
                                          v-model="editVMForm.ip"
                                          required
                                          placeholder="Enter ip address">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-vm-host-edit-group"
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
                        <b-form-group id="form-vm-os-edit-group"
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
                        <b-form-group id="form-vm-cores-edit-group"
                                      label="Cores:"
                                      label-for="form-cores-input">
                            <b-form-input id="form-cores-input"
                                          type="number"
                                          v-model="editVMForm.cores"
                                          required
                                          placeholder="Enter cores">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-vm-threads-edit-group"
                                      label="Threads:"
                                      label-for="form-threads-input">
                            <b-form-input id="form-vm-threads-input"
                                          type="number"
                                          v-model="editVMForm.threads"
                                          required
                                          placeholder="Enter threads">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-vm-storage-size-edit-group"
                                      label="Storage size:"
                                      label-for="form-storage-size-input">
                            <b-form-input id="form-vm-storage-size-input"
                                          type="number"
                                          v-model="editVMForm.storage_size"
                                          required
                                          placeholder="Enter storage size">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-vm-memory-edit-group"
                                      label="Memory:"
                                      label-for="form-memory-input">
                            <b-form-input id="form-vm-memory-input"
                                          type="number"
                                          v-model="editVMForm.memory"
                                          required
                                          placeholder="Enter memory">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-vm-description-edit-group"
                                      label="Description:"
                                      label-for="form-description-input">
                            <b-form-input id="form-vm-description-input"
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
                         title="Delete virtual machine"
                         hide-footer>
                    <b-form @submit="SubmitDeleteVM" @reset="ResetDeleteVM" class="w-100">
                        <b-button type="submit" variant="primary">Delete</b-button>
                        <b-button type="reset" variant="danger">Cancel</b-button>
                    </b-form>
                </b-modal>
                <b-modal ref="deleteStorageModal"
                         id="Storage-delete-modal"
                         title="Delete storage"
                         hide-footer>
                    <b-form @submit="SubmitStorageDelete" @reset="ResetStorageDelete" class="w-100">
                        <b-button type="submit" variant="primary">Delete</b-button>
                        <b-button type="reset" variant="danger">Cancel</b-button>
                    </b-form>
                </b-modal>
                <b-modal ref="editStorageModal"
                         id="Storage-update-modal"
                         title="Update a storage"
                         hide-footer>
                    <b-form @submit="SubmitStorageUpdate" @reset="ResetStorageUpdate" class="w-100">
                        <b-form-group id="form-storage-model-edit-group"
                                      label="Model storage:"
                                      label-for="form-model-input">
                            <b-form-input id="form-storage-model-input"
                                          type="text"
                                          v-model="editStorageForm.model"
                                          required
                                          placeholder="Enter model storage">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-storage-volume-edit-group"
                                      label="Storage volume:"
                                      label-for="form-storage volume-input">
                            <b-form-input id="form-storage-volume-input"
                                          type="number"
                                          v-model="editStorageForm.size_storage"
                                          required
                                          placeholder="Enter storage volume">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-type-storage-edit-group"
                                      label="Type storage:"
                                      label-for="form-type-storage-input">
                            <b-form-select v-model="editStorageForm.type_storage">
                                <b-form-select-option :value="null" disabled>Please select an type storage
                                </b-form-select-option>
                                <b-form-select-option v-for="type in list_type" :value="type.id">{{ type.type_storage }}
                                </b-form-select-option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-storage-serial_number-edit-group"
                                      label="serial_numberentory number:"
                                      label-for="form-storage-serial_number-input">
                            <b-form-input id="form-serial_number-input"
                                          type="text"
                                          v-model="editStorageForm.serial_number"
                                          required
                                          placeholder="Enter serial_numberentory number">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-host-edit-group"
                                      label="Host:"
                                      label-for="form-host-input">
                            <b-form-select v-model="editStorageForm.host">
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
                        <b-form-group id="form-date-install-edit-group"
                                      label="Date install:"
                                      label-for="form-date-install-input">
                            <b-form-input id="form-date-install-input"
                                          type="date"
                                          v-model="editStorageForm.date_install"
                                          required
                                          placeholder="Enter date install">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-storage-description-edit-group"
                                      label="Description:"
                                      label-for="form-description-input">
                            <b-form-input id="form-description-input"
                                          type="text"
                                          v-model="editStorageForm.description"
                                          required
                                          for="input-valid"
                                          placeholder="Enter description">
                            </b-form-input>
                        </b-form-group>
                        <b-button type="submit" variant="primary">Submit</b-button>
                        <b-button type="reset" variant="danger">Reset</b-button>
                    </b-form>
                </b-modal>
            </div>
        </div>
    </section>
</template>

<script>
    import axios from "axios"
    import Alert from "./Alert";

    export default {
        name: "DetailHost",
        props: ['id'],
        data() {
            return {
                host: [],
                hosts: [],
                editHostForm: {
                    id: '',
                    name: '',
                    ip: '',
                    os: null,
                    cpu: '',
                    memory: null,
                    description: '',
                    serial_number: '',
                },
                deleteHostForm: {
                    id: '',
                },
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
                addStorageForm: {
                    model: '',
                    host: '',
                    size_storage: '',
                    type_storage: '',
                    date_install: '',
                    description: '',
                    serial_number: '',
                },
                editStorageForm: {
                    model: '',
                    host: '',
                    size_storage: '',
                    type_storage: '',
                    date_install: null,
                    description: null,
                    serial_number: '',
                },
                deleteStorageForm: {
                    id: '',
                },
                list_storage: [],
                list_type: [],
                list_os: [],
                message: '',
                showMessage: false,
            }
        },
        components: {
            alert: Alert,
        },
        created() {
            this.LoadHost()
        },
        methods: {
            async LoadHost() {
                this.host = await fetch(
                    `${this.$store.getters.getServerUrl}/host/${this.id}`
                ).then(response => response.json())
                console.log(this.host)
                console.log(this.id)
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
            initForm() {
                this.editHostForm.name = '';
                this.editHostForm.ip = '';
                this.editHostForm.os = 0;
                this.editHostForm.cpu = '';
                this.editHostForm.memory = 0;
                this.editHostForm.description = '';
                this.editHostForm.serial_number = '';
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
                    serial_number: this.editHostForm.serial_number,
                }
                this.updateHost(payload, this.editHostForm.id)
            },
            updateHost(payload, hostID) {
                const path = `${this.$store.getters.getServerUrl}/update-host/${hostID}`
                axios.put(path, payload)
                    .then(() => {
                        this.LoadHost()
                        this.message = 'Host updated!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        console.error(error)
                        this.LoadHost()
                    });
            },
            ResetUpdate(evt) {
                evt.preventDefault();
                this.$refs['editHostModal'].hide();
                this.initForm();
                this.LoadHost();
            },
            removeHost(hostID) {
                const path = `${this.$store.getters.getServerUrl}/delete-host/${hostID}`
                axios.delete(path)
                    .then(() => {
                        this.LoadHost()
                        this.message = 'Host removed!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error);
                        this.LoadHost();
                    });
            },
            DeleteHost(host) {
                this.deleteHostForm.id = host.id
                console.log(this.deleteHostForm.id)
            },
            ResetDelete(evt) {
                evt.preventDefault();
                this.$refs['deleteHostModal'].hide();
                this.LoadHost();
            },
            SubmitDelete(evt) {
                evt.preventDefault()
                this.$refs['deleteHostModal'].hide()
                this.removeHost(this.deleteHostForm.id)
            },
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
                        this.LoadHost()
                        this.message = 'Virtual machine added!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.log(error)
                        this.LoadHost()
                    });
            },
            initVMForm() {
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
                this.initVMForm();
            },
            ResetVM(evt) {
                evt.preventDefault()
                this.$refs['addVMModal'].hide()
                this.initVMForm();
            },
            editVM(vm) {
                this.editVMForm = vm
                this.getListOS()
                console.log(this.vm)
                this.getListHosts()
            },
            SubmitUpdateVM(evt) {
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
                    .then(() => {
                        this.LoadHost()
                        this.message = 'Virtual machine updated!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error)
                        this.LoadHost()
                    });
            },
            ResetUpdateVM(evt) {
                evt.preventDefault();
                this.$refs['editVMModal'].hide();
                this.initVMForm();
                this.LoadHost();
            },
            removeVM(hostID) {
                const path = `${this.$store.getters.getServerUrl}/delete-vm/${hostID}`
                axios.delete(path)
                    .then(() => {
                        this.LoadHost()
                        this.message = 'Virtual machine removed!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error);

                    });
                this.LoadHost();
            },
            DeleteVM(vm) {
                this.DeleteVMForm.id = vm.id
                console.log(this.DeleteVMForm.id)
            },
            ResetDeleteVM(evt) {
                evt.preventDefault();
                this.$refs['deleteVMModal'].hide();
                // this.initForm();
                this.LoadHost();
            },
            SubmitDeleteVM(evt) {
                evt.preventDefault()
                this.$refs['deleteVMModal'].hide()
                this.removeVM(this.DeleteVMForm.id)
            },
            getListStorage() {
                const path = `${this.$store.getters.getServerUrl}/list-storage/`
                axios.get(path).then((res) => {
                    this.list_storage = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(response)
                    })
            },
            getListType() {
                const path = `${this.$store.getters.getServerUrl}/list-type-storage/`
                axios.get(path).then((res) => {
                    this.list_type = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(response)
                    })
            },
            addStorage(payload) {
                const path = `${this.$store.getters.getServerUrl}/add-storage/`
                axios.post(path, payload)
                    .then(() => {
                        this.LoadHost()
                        this.message = 'Storage added!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.log(error)
                        this.LoadHost()
                    });
            },
            initStorageForm() {
                this.addStorageForm.model = '';
                this.addStorageForm.host = null;
                this.addStorageForm.size_storage = '';
                this.addStorageForm.date_install = null;
                this.addStorageForm.description = null;
                this.addStorageForm.serial_number = '';
                this.addStorageForm.type_storage = '';

                this.editStorageForm.model = '';
                this.editStorageForm.host = '';
                this.editStorageForm.size_storage = '';
                this.editStorageForm.date_install = '';
                this.editStorageForm.description = '';
                this.editStorageForm.serial_number = '';
                this.editStorageForm.type_storage = '';
            },
            SubmitStorage(evt) {
                evt.preventDefault()
                this.$refs['addStorageModal'].hide()
                const payload = {
                    model: this.addStorageForm.model,
                    host: this.addStorageForm.host,
                    size_storage: this.addStorageForm.size_storage,
                    date_install: this.addStorageForm.date_install,
                    description: this.addStorageForm.description,
                    serial_number: this.addStorageForm.serial_number,
                    type_storage: this.addStorageForm.type_storage,
                }
                this.addStorage(payload);
                this.initStorageForm();
            },
            ResetStorage(evt) {
                evt.preventDefault()
                this.$refs['addStorageModal'].hide()
                this.initStorageForm();
            },
            editStorage(Storage) {
                this.editStorageForm = Storage
                this.getListType()
                this.getListHosts()
                console.log(this.Storage)
            },
            SubmitStorageUpdate(evt) {
                evt.preventDefault()
                this.$refs['editStorageModal'].hide()
                const payload = {
                    model: this.editStorageForm.model,
                    host: this.editStorageForm.host,
                    size_storage: this.editStorageForm.size_storage,
                    date_install: this.editStorageForm.date_install,
                    description: this.editStorageForm.description,
                    serial_number: this.editStorageForm.serial_number,
                    type_storage: this.editStorageForm.type_storage,
                }
                this.updateStorage(payload, this.editStorageForm.id)
            },
            updateStorage(payload, StorageID) {
                const path = `${this.$store.getters.getServerUrl}/update-storage/${StorageID}`
                axios.put(path, payload)
                    //скорей свего не будет работать надо поменять get list на вызов отдельной функции
                    .then(() => {
                        this.LoadHost()
                        this.message = 'Storage updated!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error)
                        this.LoadHost()
                    });
                this.LoadHost()
            },
            ResetStorageUpdate(evt) {
                evt.preventDefault();
                this.$refs['editStorageModal'].hide();
                this.initStorageForm();
                this.LoadHost();
            },
            removeStorage(StorageID) {
                const path = `${this.$store.getters.getServerUrl}/delete-storage/${StorageID}`
                axios.delete(path)
                    .then(() => {
                        this.LoadHost()
                        this.message = 'Storage removed!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error);
                        this.LoadHost();
                    });
            },
            DeleteStorage(Storage) {
                this.deleteStorageForm.id = Storage.id
                console.log(this.deleteStorageForm.id)
            },
            ResetStorageDelete(evt) {
                evt.preventDefault();
                this.$refs['deleteStorageModal'].hide();
                // this.initForm();
                this.LoadHost();
            },
            SubmitStorageDelete(evt) {
                evt.preventDefault()
                this.$refs['deleteStorageModal'].hide()
                this.removeStorage(this.deleteStorageForm.id)
            },
        },
    }
</script>

<style scoped>
    .col-sm-10 {
        max-width: 100%;
    }

    .container {
        max-width: 100%;
    }

    .row {
        margin-left: 7%;
    }
</style>