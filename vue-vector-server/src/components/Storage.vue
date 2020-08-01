<template>
    <section id="intro" class="wrapper style1 fullscreen fade-up">
        <div class="inner">
            <div class="Storage">
                <div class="container">
                    <div class="row">
                        <div class="col-sm-10">
                            <h1>List storages</h1>
                            <hr>
                            <br><br>
                            <button type="button" class="btn btn-success btn-sm" v-b-modal.Storage-modal
                                    @click="getListHost">
                                Add
                                storage
                            </button>
                            <br><br>
                            <alert :message=message v-if="showMessage"></alert>
                            <table>
                                <thead>
                                <tr>
                                    <th scope="col">Model</th>
                                    <th scope="col">Storage volume</th>
                                    <th scope="col">Storage type</th>
                                    <th scope="col">s/n</th>
                                    <th scope="col">host</th>
                                    <th scope="col">Date install</th>
                                    <th scope="col">Description</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="(Storage, index) in list_storage" :key="index">
                                    <td>{{ Storage.model }}</td>
                                    <td>{{ Storage.size_storage }}</td>
                                    <td>{{ Storage.type_storage }}</td>
                                    <td>{{ Storage.serial_number }}</td>
                                    <td>{{ Storage.host }}</td>
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
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <b-modal ref="addStorageModal"
                         id="Storage-modal"
                         title="Add a new storage"
                         hide-footer
                         content-class="shadow">
                    <b-form @submit="Submit" @reset="Reset" class="w-100">
                        <b-form-group id="form-model-group"
                                      label="Model storage:"
                                      label-for="form-model-input">
                            <b-form-input id="form-model-input"
                                          type="text"
                                          v-model="addStorageForm.model"
                                          required
                                          placeholder="Enter model storage">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-storage-volume-group"
                                      label="Storage volume:"
                                      label-for="form-storage volume-input">
                            <b-form-input id="form-storage-volume-input"
                                          type="number"
                                          v-model="addStorageForm.size_storage"
                                          required
                                          placeholder="Enter storage volume">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-type-storage-group"
                                      label="Type storage:"
                                      label-for="form-type-storage-input">
                            <b-form-select v-model="addStorageForm.type_storage">
                                <b-form-select-option :value="null" disabled>Please select an type storage
                                </b-form-select-option>
                                <b-form-select-option v-for="type in list_type" :value="type.id">{{ type.type_storage }}
                                </b-form-select-option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-sssserial_number-group"
                                      label="sssserial_numberentory number:"
                                      label-for="nvform-sssserial_number-input">
                            <b-form-input id="form-sssserial_number-input"
                                          type="text"
                                          v-model="addStorageForm.sssserial_number"
                                          required
                                          placeholder="Enter sssserial_numberentory number">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-host-group"
                                      label="Host:"
                                      label-for="form-host-input">
                            <b-form-select v-model="addStorageForm.host">
                                <b-form-select-option :value="null"
                                                      disabled>
                                    Please select an host
                                </b-form-select-option>
                                <b-form-select-option v-for="host in list_host"
                                                      :value="host.id">
                                    {{ host.name }} - {{ host.os }} - {{ host.ip}}
                                </b-form-select-option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-date-install-group"
                                      label="Date install:"
                                      label-for="form-date-install-input">
                            <b-form-input id="form-date-install-input"
                                          type="date"
                                          v-model="addStorageForm.date_install"
                                          required
                                          placeholder="Enter date install">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-description-group"
                                      label="Description:"
                                      label-for="form-description-input">
                            <b-form-input id="form-description-input"
                                          type="text"
                                          v-model="addStorageForm.description"
                                          required
                                          for="input-valid"
                                          placeholder="Enter description">
                            </b-form-input>
                        </b-form-group>
                        <b-button type="submit" variant="primary">Submit</b-button>
                        <b-button type="reset" variant="danger">Reset</b-button>
                    </b-form>
                </b-modal>
                <b-modal ref="deleteStorageModal"
                         id="Storage-delete-modal"
                         title="Delete storage"
                         hide-footer>
                    <b-form @submit="SubmitDelete" @reset="ResetDelete" class="w-100">
                        <b-button type="submit" variant="primary">Delete</b-button>
                        <b-button type="reset" variant="danger">Cancel</b-button>
                    </b-form>
                </b-modal>
                <b-modal ref="editStorageModal"
                         id="Storage-update-modal"
                         title="Update a storage"
                         hide-footer>
                    <b-form @submit="SubmitUpdate" @reset="ResetUpdate" class="w-100">
                        <b-form-group id="form-model-edit-group"
                                      label="Model storage:"
                                      label-for="form-model-input">
                            <b-form-input id="form-model-input"
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
                        <b-form-group id="form-sssserial_number-edit-group"
                                      label="sssserial_numberentory number:"
                                      label-for="nvform-sssserial_number-input">
                            <b-form-input id="form-sssserial_number-input"
                                          type="text"
                                          v-model="editStorageForm.sssserial_number"
                                          required
                                          placeholder="Enter sssserial_numberentory number">
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
                                <b-form-select-option v-for="host in list_host"
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
                        <b-form-group id="form-description-edit-group"
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
    import axios from 'axios'
    import Alert from './Alert'

    export default {
        name: "Storage",
        data() {
            return {
                list_storage: [],
                addStorageForm: {
                    model: '',
                    host: '',
                    size_storage: '',
                    type_storage: '',
                    date_install: '',
                    description: '',
                    sssserial_number: '',
                },
                editStorageForm: {
                    model: '',
                    host: '',
                    size_storage: '',
                    type_storage: '',
                    date_install: null,
                    description: null,
                    sssserial_number: '',
                },
                deleteStorageForm: {
                    id: '',
                },
                list_host: [],
                list_type: [],
                message: '',
                showMessage: false,
            };
        },
        components: {
            alert: Alert,
        },
        methods: {
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
            getListHost() {
                const path = `${this.$store.getters.getServerUrl}/list-host/`
                axios.get(path).then((res) => {
                    this.list_host = res.data
                }).catch((error) => {
                    console.error(error)
                })
                    .then((response,) => {
                        console.log(response)
                    })
                this.getListType()
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
                        this.getListStorage()
                        this.message = 'Storage added!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.log(error)
                        this.getListStorage()
                    });
            },
            initForm() {
                this.addStorageForm.model = '';
                this.addStorageForm.host = null;
                this.addStorageForm.size_storage = '';
                this.addStorageForm.date_install = null;
                this.addStorageForm.description = null;
                this.addStorageForm.sssserial_number = '';
                this.addStorageForm.type_storage = '';

                this.editStorageForm.model = '';
                this.editStorageForm.host = '';
                this.editStorageForm.size_storage = '';
                this.editStorageForm.date_install = '';
                this.editStorageForm.description = '';
                this.editStorageForm.sssserial_number = '';
                this.editStorageForm.type_storage = '';
            },
            Submit(evt) {
                evt.preventDefault()
                this.$refs['addStorageModal'].hide()
                const payload = {
                    model: this.addStorageForm.model,
                    host: this.addStorageForm.host,
                    size_storage: this.addStorageForm.size_storage,
                    date_install: this.addStorageForm.date_install,
                    description: this.addStorageForm.description,
                    sssserial_number: this.addStorageForm.sssserial_number,
                    type_storage: this.addStorageForm.type_storage,
                }
                this.addStorage(payload);
                this.initForm();
            },
            Reset(evt) {
                evt.preventDefault()
                this.$refs['addStorageModal'].hide()
                this.initForm();
            },
            editStorage(Storage) {
                this.editStorageForm = Storage
                this.getListType()
                this.getListHost()
                console.log(this.Storage)
            },
            SubmitUpdate(evt) {
                evt.preventDefault()
                this.$refs['editStorageModal'].hide()
                const payload = {
                    model: this.editStorageForm.model,
                    host: this.editStorageForm.host,
                    size_storage: this.editStorageForm.size_storage,
                    date_install: this.editStorageForm.date_install,
                    description: this.editStorageForm.description,
                    sssserial_number: this.editStorageForm.sssserial_number,
                    type_storage: this.editStorageForm.type_storage,
                }
                this.updateStorage(payload, this.editStorageForm.id)
            },
            updateStorage(payload, StorageID) {
                const path = `${this.$store.getters.getServerUrl}/update-storage/${StorageID}`
                axios.put(path, payload)
                    //скорей свего не будет работать надо поменять get list на вызов отдельной функции
                    .then(() => {
                        this.getListStorage()
                        this.message = 'Storage updated!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error)
                        this.getListStorage()
                    });
            },
            ResetUpdate(evt) {
                evt.preventDefault();
                this.$refs['editStorageModal'].hide();
                this.initForm();
                this.getListStorage();
            },
            removeStorage(StorageID) {
                const path = `${this.$store.getters.getServerUrl}/delete-storage/${StorageID}`
                axios.delete(path)
                    .then(() => {
                        this.getListStorage()
                        this.message = 'Storage removed!'
                        this.showMessage = true
                    })
                    .catch((error) => {
                        // eslint-отключение следующей строки
                        console.error(error);
                        this.getListStorage();
                    });
            },
            DeleteStorage(Storage) {
                this.deleteStorageForm.id = Storage.id
                console.log(this.deleteStorageForm.id)
            },
            ResetDelete(evt) {
                evt.preventDefault();
                this.$refs['deleteStorageModal'].hide();
                // this.initForm();
                this.getListStorage();
            },
            SubmitDelete(evt) {
                evt.preventDefault()
                this.$refs['deleteStorageModal'].hide()
                this.removeStorage(this.deleteStorageForm.id)
            },
        },
        created() {
            this.getListStorage()
        }
    };
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