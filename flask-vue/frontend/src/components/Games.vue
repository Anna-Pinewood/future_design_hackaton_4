<template>
  <div
    style="background: transparent !important"
    class="jumbotron vertical-center"
  >
    <div class="container">
      <!-- bootswatch CDN -->
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css"
        integrity="sha384-enpDwFISL6M3ZGZ50Tjo8m65q06uLVnyvkFO3rsoW0UC15ATBFz3QEhr3hmxpYsn"
        crossorigin="anonymous"
      />
      <div class="row">
        <div class="col-sm-12">
          <h1>Today's activities</h1>
          <hr />
          <br />
          <!-- Alert Message -->

          <button
            type="button"
            class="btn btn-success brn-sm"
            v-b-modal.todo-modal
          >
            Add a thing
          </button>
          <br /><br />

          <table class="table table-hover">
            <thead>
              <tr>
                <!--table hrader cells-->
                <th scope="col">Time</th>
                <th scope="col">Activity</th>
                <th scope="col">Done?</th>
                <th scope="col">To do</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(thing, index) in things"
                v-bind:key="index"
                v-b-modal.hi-modal
              >
                <td>{{ thing.time }}</td>
                <td>{{ thing.name }}</td>
                <td>
                  <span v-if="thing.done"> YES </span>
                  <span v-else> NO </span>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-info btn-sm">
                      Change
                    </button>
                    <button type="button" class="btn btn-danger btn-sm">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <b-modal
        ref="addTodoModal"
        id="todo-modal"
        title="Add new activity"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group
            id="form-name-group"
            label="Name:"
            label-for="form-name-input"
          >
            <b-form-input
              id="form-title-input"
              type="text"
              v-model="addTodoForm.name"
              required
              placeholder="Enter todo"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-time-group"
            label="Time:"
            label-for="form-time-input"
          >
            <b-form-input
              id="form-time-input"
              type="text"
              v-model="addTodoForm.time"
              required
              placeholder="Enter time"
            >
            </b-form-input>
          </b-form-group>

          <!--Checkbox-->

          <b-form-group id="form-done-group">
            <b-form-checkbox-group v-model="addTodoForm.done" id="form-checks">
              <b-form-checkbox value="true"> Done? </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <!--Sub and Reset button-->

          <b-button type="submit" variant="outline-info">Submit</b-button>
          <b-button type="reset" variant="outline-danger">Reset</b-button>
        </b-form>
      </b-modal>

      <!--TEST MODAL FOR EVERY TASK!!!!! JUST SAYS TEST-->

      <b-modal
        ref="addTodoModal"
        id="hi-modal"
        title="Add new activity"
        hide-backdrop
        hide-footer
      >
        <h1>idk man</h1>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "GamesLib",
  data() {
    return {
      things: [],
      addTodoForm: {
        name: "",
        time: "",
        done: [],
      },
    };
  },
  methods: {
    getThings() {
      const path = "http://localhost:5000/things";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.things = res.data.things;
        })
        .catch((err) => {
          console.error(err);
        });
    },

    addThings(payload) {
      const path = "http://localhost:5000/things";
      axios
        .post(path, payload)
        .then(() => {
          this.getThings();
        })
        .catch((err) => {
          console.error(err);
          this.getThings();
        });
    },

    initForm() {
      (this.addTodoForm.name = ""),
        (this.addTodoForm.time = ""),
        (this.addTodoForm.done = []);
    },

    onSubmit(e) {
      e.preventDefault();
      this.$refs.addTodoModal.hide();
      let done = false;
      if (this.addTodoForm.done[0]) done = true;
      const payload = {
        name: this.addTodoForm.name,
        time: this.addTodoForm.time,
        done,
      };
      this.addThings(payload);
      this.initForm();
    },
    onReset(e) {
      e.preventDefault();
      this.$refs.addTodoModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getThings();
  },
};
</script>
