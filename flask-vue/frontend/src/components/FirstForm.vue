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

      <h3>Есть ли у вас csv-файл с данными о вашем расписании?</h3>
      <b-button
        type="submit"
        @click="onSubmit"
        variant="outline-info"
        style="margin-top: 25px"
      >
        Есть
      </b-button>
      <b-button
        type="reset"
        @click="onReset"
        variant="outline-danger"
        style="margin-top: 25px"
      >
        Нет
      </b-button>

      <transition name="fade">
        <div v-if="iscsv === true" style="margin-top: 25px">
          <h2>Загрузите сюда ваш csv!</h2>
          <!--SUBMIT MODEL BUTTON-->
          <br />

          <FileHandler />
        </div>
      </transition>
      <transition name="fade">
        <div v-if="iscsv === false" style="margin-top: 35px">
          <h2>Тогда просим вас ответить на несколько вопросов</h2>
          <div v-if="show === 0">
            <!--FORM QUESTION 1-->

            <b-form @submit="onSubmitForm" @reset="onReset" class="w-100">
              <div style="margin-top: 25px">
                <label for="range-1"
                  >Оцените свою склонность к прокрастинации от 0 до 3</label
                >
                <b-form-input
                  id="range-1"
                  v-model="value"
                  type="range"
                  min="0"
                  max="3"
                ></b-form-input>
                <div class="mt-2">Результат: {{ value }}</div>
              </div>

              <b-form inline>
                <label class="mr-sm-2" for="inline-form-custom-select-pref">
                  Выберите сферу деятельности
                </label>
                <b-form-select
                  id="inline-form-work"
                  class="mb-2 mr-sm-2 mb-sm-0 space"
                  :options="[
                    { text: '', value: null },
                    'Работа',
                    'Учеба',
                    'Оба',
                    'Ничего',
                  ]"
                  :value="null"
                  v-model="addInfo.work"
                ></b-form-select>
              </b-form>

              <b-form-group
                id="workdaysleep-group"
                label-for="form-workdaysleep-input"
                style="margin-top: 25px"
              >
                <b-form-input
                  id="workdaysleep"
                  class="space"
                  type="text"
                  v-model="addInfo.workdaysleep"
                  required
                  placeholder="Когда вы ложитесь спать в будние дни?"
                >
                </b-form-input>
              </b-form-group>

              <b-form-group
                id="weekendsleep-group"
                label-for="form-workdaysleep-input"
              >
                <b-form-input
                  id="weekendsleep"
                  class="space"
                  type="text"
                  v-model="addInfo.weekendsleep"
                  required
                  placeholder="А в выходные?"
                >
                </b-form-input>
              </b-form-group>

              <div>
                <label for="range-1"
                  >Насколько вы идеалист(ка)? (По шкале от 0 до 3)</label
                >
                <b-form-input
                  id="range-1"
                  v-model="ideal"
                  type="range"
                  min="0"
                  max="3"
                ></b-form-input>
                <div class="mt-2">Результат: {{ ideal }}</div>
              </div>

              <!--Sub and Reset button-->

              <b-button
                type="submit"
                variant="outline-info"
                @click="onSubmitForm"
                style="margin-top: 25px"
                >Submit</b-button
              >
              <b-button
                type="reset"
                variant="outline-danger"
                @click="resetForm"
                style="margin-top: 25px"
                >Reset</b-button
              >
            </b-form>
            <div v-show="showbar === true" style="width: 350px; height: 350px">
              <DataLine />
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-active {
  opacity: 0;
}

.space {
  margin-top: 50px;
  padding-top: 50px;
  padding-bottom: 10px;
}
</style>

<script>
import FileHandler from "@/components/FileHandler.vue";
import DataLine from "@/components/SecondLine.vue";
import axios from "axios";
export default {
  name: "FirstForm",
  data() {
    return {
      ideal: 0,
      value: 0,
      iscsv: null,
      file1: null,
      modeltype: null,
      show: 0,
      addInfo: {
        procrastination: "",
        work: "",
        workdaysleep: "",
        weekendsleep: "",
        ideal: "",
      },
      showbar: null,
    };
  },
  methods: {
    resetForm() {
      this.initForm();
    },
    getInfo() {
      const path = "http://localhost:5000/user_form";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.addInfo = res.data.user_data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    addModelType(payload) {
      const path = "http://localhost:5000/modeltype";
      axios
        .post(path, payload)
        .then(() => {})
        .catch((err) => {
          console.error(err);
        });
    },
    onSubmit(e) {
      this.iscsv = true;
      e.preventDefault();
    },
    onReset(e) {
      this.iscsv = false;
      e.preventDefault();
    },
    initForm() {
      (this.value = 0),
        (this.addInfo.workdaysleep = ""),
        (this.addInfo.weekendsleep = ""),
        (this.ideal = 0),
        (this.addInfo.work = "");
    },
    postInfo(payload) {
      const path = "http://localhost:5000/user_form";
      axios
        .post(path, payload)
        .then(() => {})
        .catch((err) => {
          console.error(err);
          this.getInfo();
        });
    },
    onSubmitForm(e) {
      e.preventDefault();
      const payload = {
        procrastination: this.value,
        workdaysleep: this.addInfo.workdaysleep,
        weekendsleep: this.addInfo.weekendsleep,
        ideal: this.ideal,
        work: this.addInfo.work,
      };
      this.postInfo(payload);
      this.initForm();
      this.showbar = true;
    },
  },
  created() {},
  components: {
    FileHandler,
    DataLine,
  },
};
</script>
