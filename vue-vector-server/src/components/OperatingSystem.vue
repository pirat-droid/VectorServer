<template>
    <div class="OperatingSystem">
        <div class="container">
            <div class="row">
                <div class="col-sm-10">
                    <p>
                        <router-link to="/list-vm">List VM</router-link>
                    </p>
                    <p>
                        <router-link to="/">List Hosts</router-link>
                    </p>
                    <p>
                        <router-link to="/list-storage">List storage</router-link>
                    </p>
                    <h1>List Operating system</h1>
                    <hr>
                    <br><br>
                    <button type="button" class="btn btn-success btn-sm" v-b-modal.OperatingSystem-modal
                            @click="getListCapacity">
                        Add
                        Operating system
                    </button>
                    <br><br>
                    <alert :message=message v-if="showMessage"></alert>
                    <table>
                        <thead>
                        <tr>
                            <th scope="col">Family</th>
                            <th scope="col">Name</th>
                            <th scope="col">Digit capacity</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(OperatingSystem, index) in list_OperatingSystem" :key="index">
                            <td>{{ OperatingSystem.family}}</td>
                            <td>{{ OperatingSystem.os}}</td>
                            <td>{{ OperatingSystem.capacity}}</td>
                            <td>
                                <button type="button"
                                        class="btn btn-warning btn-sm"
                                        v-b-modal.OperatingSystem-update-modal
                                        @click="editOperatingSystem(OperatingSystem)">
                                    Update
                                </button>
                                <button type="button"
                                        class="btn btn-danger btn-sm"
                                        v-b-modal.OperatingSystem-delete-modal
                                        @click="DeleteOperatingSystem(OperatingSystem)">
                                    Delete
                                </button>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <b-modal ref="addOperatingSystemModal"
                 id="OperatingSystem-modal"
                 title="Add a new OperatingSystem"
                 hide-footer>
            <b-form @submit="Submit" @reset="Reset" class="w-100">
                <b-form-group id="form-family-OperatingSystem-group"
                              label="family OperatingSystem:"
                              label-for="form-family-OperatingSystem-input">
                    <b-form-select v-model="addOperatingSystemForm.family">
                        <b-form-select-option :value="null" disabled>Please select an family Operating system
                        </b-form-select-option>
                        <b-form-select-option v-for="family in list_family" :value="family.id">{{ family.name}}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-form-group id="form-os-group"
                              label="Name operating system:"
                              label-for="form-os-input">
                    <b-form-input id="form-os-input"
                                  type="text"
                                  v-model="addOperatingSystemForm.os"
                                  required
                                  placeholder="Enter name">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-capacity-group"
                              label="capacity:"
                              label-for="form-capacity-input">
                    <b-form-select v-model="addOperatingSystemForm.capacity">
                        <b-form-select-option :value="null"
                                              disabled>
                            Please select an capacity
                        </b-form-select-option>
                        <b-form-select-option v-for="capacity in list_capacity"
                                              :value="capacity.id">
                            {{ capacity.bit }}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="deleteOperatingSystemModal"
                 id="OperatingSystem-delete-modal"
                 title="Delete OperatingSystem"
                 hide-footer>
            <b-form @submit="SubmitDelete" @reset="ResetDelete" class="w-100">
                <b-button type="submit" variant="primary">Delete</b-button>
                <b-button type="reset" variant="danger">Cancel</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="editOperatingSystemModal"
                 id="OperatingSystem-update-modal"
                 title="edit a new OperatingSystem"
                 hide-footer>
            <b-form @submit="SubmitUpdate" @reset="ResetUpdate" class="w-100">
                <b-form-group id="form-family-OperatingSystem-edit-group"
                              label="Family operating system:"
                              label-for="form-family-OperatingSystem-edit-input">
                    <b-form-select v-model="editOperatingSystemForm.family">
                        <b-form-select-option :value="null" disabled>Please select an family Operating system
                        </b-form-select-option>
                        <b-form-select-option v-for="family in list_family" :value="family.id">{{ family.name}}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-form-group id="form-os-edit-group"
                              label="Name operating system:"
                              label-for="form-name-input">
                    <b-form-input id="form-os-input"
                                  type="text"
                                  v-model="editOperatingSystemForm.os"
                                  required
                                  placeholder="Enter name">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-capacity-edit-group"
                              label="capacity:"
                              label-for="form-capacity-input">
                    <b-form-select v-model="editOperatingSystemForm.capacity">
                        <b-form-select-option :value="null"
                                              disabled>
                            Please select an capacity
                        </b-form-select-option>
                        <b-form-select-option v-for="capacity in list_capacity"
                                              :value="capacity.id">
                            {{ capacity.bit }}
                        </b-form-select-option>
                    </b-form-select>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios'
    import Alert from './Alert'

    export default {
        name: "OperatingSystem",
        data() {
            return {
                list_OperatingSystem: [],
                addOperatingSystemForm: {
                    capacity: '',
                    family: '',
                    os: '',
                },
                editOperatingSystemForm: {
                    capacity: '',
                    family: '',
                    os: '',
                },
                deleteOperatingSystemForm: {
                    id: '',
                },
                list_capacity: [],
                list_family: [],
                message: '',
                showMessage: false,
            };
        },
        components: {
            alert: Alert,
        },
        methods: {
            getListOperatingSystem() {
                const path = `${this.$store.getters.getServerUrl}/list-os/`
                axios.get(path).then((res) => {
                    this.list_OperatingSystem = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(this.list_OperatingSystem)
                    })
            },
            getListCapacity() {
                const path = `${this.$store.getters.getServerUrl}/list-capacity/`
                axios.get(path).then((res) => {
                    this.list_capacity = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(response)
                    })
                this.getListFamily()
            },
            getListFamily() {
                const path = `${this.$store.getters.getServerUrl}/list-family/`
                axios.get(path).then((res) => {
                    this.list_family = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(response)
                    })
            },
            addOperatingSystem(payload) {
                const path = `${this.$store.getters.getServerUrl}/add-os/`
                axios.post(path, payload)
                    .then(() => {
                        this.getListOperatingSystem()
                        this.message = 'Operating system added!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.log(error)
                        this.getListOperatingSystem()
                    });
            },
            initForm() {
                this.addOperatingSystemForm.family = '';
                this.addOperatingSystemForm.capacity = null;
                this.addOperatingSystemForm.os = '';

                this.editOperatingSystemForm.family = '';
                this.editOperatingSystemForm.capacity = '';
                this.editOperatingSystemForm.os = '';
            },
            Submit(evt) {
                evt.preventDefault()
                this.$refs['addOperatingSystemModal'].hide()
                const payload = {
                    capacity: this.addOperatingSystemForm.capacity,
                    os: this.addOperatingSystemForm.os,
                    family: this.addOperatingSystemForm.family,
                }
                this.addOperatingSystem(payload);
                this.initForm();
            },
            Reset(evt) {
                evt.preventDefault()
                this.$refs['addOperatingSystemModal'].hide()
                this.initForm();
            },
            editOperatingSystem(OperatingSystem) {
                this.editOperatingSystemForm = OperatingSystem
                this.getListFamily()
                this.getListCapacity()
                console.log(this.OperatingSystem)
            },
            SubmitUpdate(evt) {
                evt.preventDefault()
                this.$refs['editOperatingSystemModal'].hide()
                const payload = {
                    capacity: this.editOperatingSystemForm.capacity,
                    os: this.editOperatingSystemForm.os,
                    family: this.editOperatingSystemForm.family,
                }
                this.updateOperatingSystem(payload, this.editOperatingSystemForm.id)
            },
            updateOperatingSystem(payload, OperatingSystemID) {
                const path = `${this.$store.getters.getServerUrl}/update-os/${OperatingSystemID}`
                axios.put(path, payload)
                    //скорей свего не будет работать надо поменять get list на вызов отдельной функции
                    .then(() => {
                        this.getListOperatingSystem()
                        this.message = 'Operating system updated!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error)
                        this.getListOperatingSystem()
                    });
            },
            ResetUpdate(evt) {
                evt.preventDefault();
                this.$refs['editOperatingSystemModal'].hide();
                this.initForm();
                this.getListOperatingSystem();
            },
            removeOperatingSystem(OperatingSystemID) {
                const path = `${this.$store.getters.getServerUrl}/delete-os/${OperatingSystemID}`
                axios.delete(path)
                    .then(() => {
                        this.getListOperatingSystem()
                        this.message = 'Operating system removed!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error);
                        this.getListOperatingSystem();
                    });
            },
            DeleteOperatingSystem(OperatingSystem) {
                this.deleteOperatingSystemForm.id = OperatingSystem.id
                console.log(this.deleteOperatingSystemForm.id)
            },
            ResetDelete(evt) {
                evt.preventDefault();
                this.$refs['deleteOperatingSystemModal'].hide();
                // this.initForm();
                this.getListOperatingSystem();
            },
            SubmitDelete(evt) {
                evt.preventDefault()
                this.$refs['deleteOperatingSystemModal'].hide()
                this.removeOperatingSystem(this.deleteOperatingSystemForm.id)
            },
        },
        created() {
            this.getListOperatingSystem()
        }
    };
</script>

<style scoped>

</style>