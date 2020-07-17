<template>
    <div class="host">
        <div class="container">
            <div class="row">
                <div class="col-sm-10">
                    <p>
                        <router-link to="/list-vm">List VM</router-link>
                    </p>
                    <p>
                        <router-link to="/list-storage">List Storage</router-link>
                    </p>
                    <p>
                        <router-link to="/list-operating-system">List Operating system</router-link>
                    </p>
                    <h1>List HOST</h1>
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
                            <th scope="col">Memory</th>
                            <th scope="col">Description</th>
                            <th scope="col">Inv Number</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>{{ host.name }}</td>
                            <td>{{ host.ip }}</td>
                            <td>{{ host.os }}</td>
                            <td>{{ host.cpu }}</td>
                            <td>{{ host.memory }}</td>
                            <td>{{ host.description }}</td>
                            <td>{{ host.inv }}</td>
                            <td>
                                <button type="button"
                                        class="btn btn-warning btn-sm"
                                        v-b-modal.host-update-modal
                                        @click="editHost(host)">
                                    Update
                                </button>
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
</template>

<script>
    import axios from "axios"

    export default {
        name: "DetailHost",
        props: ['id'],
        data() {
            return {
                host: {},
                editHostForm: {
                    id: '',
                    name: '',
                    ip: '',
                    os: null,
                    cpu: '',
                    memory: null,
                    description: '',
                    inv: '',
                },
                deleteHostForm: {
                    id: '',
                },
                list_os: [],
                message: '',
                showMessage: false,
            }
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
                this.editHostForm.inv = '';
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
        },
    }
</script>

<style scoped>

</style>