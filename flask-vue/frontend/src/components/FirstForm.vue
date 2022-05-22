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
      <b-button type="submit" @click="onSubmit" variant="outline-info">
        Есть
      </b-button>
      <b-button type="reset" @click="onReset" variant="outline-danger">
        Нет
      </b-button>

      <transition name="fade">
        <div v-if="iscsv === true">
          <h2>Загрузите сюда ваш csv!</h2>
          <!--SUBMIT MODEL BUTTON-->
          <br />

          <FileHandler />
        </div>
      </transition>
      <transition name="fade">
        <div v-if="iscsv === false">
          <h2>Тогда просим вас ответить на несколько вопросов</h2>
          <div v-if="show === 0">
            <!--FORM QUESTION 1-->

            <b-form @submit="onSubmitForm" @reset="onReset" class="w-100">
              <b-form-group
                id="begin-group"
                label-for="form-procrastination-input"
              >
                <b-form-input
                  class="space"
                  type="text"
                  v-model="addInfo.procrastination"
                  required
                  placeholder="Оцените свою склонность к прокрастинации от 1 до 3"
                >
                </b-form-input>
              </b-form-group>

              <b-form inline>
                <label class="mr-sm-2" for="inline-form-custom-select-pref">
                  Выберите сферу деятельности
                </label>
                <b-form-select
                  id="inline-form-work"
                  class="mb-2 mr-sm-2 mb-sm-0 space"
                  :options="[
                    { text: '', value: null },
                    'Работаете',
                    'Учатесь',
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

              <b-form-group id="burnout-group" label-for="form-burnout-input">
                <b-form-input
                  id="burnout"
                  class="space"
                  type="text"
                  v-model="addInfo.burnout"
                  required
                  placeholder="Сколько дней вам нужно, чтобы восстановиться после выгорания?"
                >
                </b-form-input>
              </b-form-group>

              <!--Sub and Reset button-->

              <b-button type="submit" variant="outline-info">Submit</b-button>
              <b-button type="reset" variant="outline-danger" @click="resetForm"
                >Reset</b-button
              >
            </b-form>
            <div v-show="showbar === true" style="width: 350px; height: 350px">
              <ChartsOne />
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
import ChartsOne from "@/components/Charts_1.vue";
import axios from "axios";
export default {
  name: "FirstForm",
  data() {
    return {
      iscsv: null,
      file1: null,
      modeltype: null,
      show: 0,
      addInfo: {
        procrastination: "",
        work: "",
        workdaysleep: "",
        weekendsleep: "",
        burnout: "",
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
      (this.addInfo.procrastination = ""),
        (this.addInfo.workdaysleep = ""),
        (this.addInfo.weekendsleep = ""),
        (this.addInfo.burnout = ""),
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
        procrastination: this.addInfo.procrastination,
        workdaysleep: this.addInfo.workdaysleep,
        weekendsleep: this.addInfo.weekendsleep,
        burnout: this.addInfo.burnout,
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
    ChartsOne,
  },
};
</script>
