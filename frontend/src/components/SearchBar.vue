<template>
  <div class="flex flex-col gap-3 rounded-lg bg-slate-800/60 p-4 shadow">
    <label class="text-sm uppercase tracking-wide text-slate-400">搜歌</label>
    <div class="flex flex-col gap-3 sm:flex-row">
      <input
        class="w-full rounded border border-slate-600 bg-slate-900/80 px-4 py-3 text-lg text-white focus:border-indigo-400 focus:outline-none"
        :placeholder="placeholder"
        :value="modelValue"
        @input="onInput"
        @keyup.enter="emit('submit')"
      />
      <button
        class="rounded bg-indigo-500 px-6 py-3 text-lg font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:bg-slate-600"
        :disabled="loading"
        @click="emit('submit')"
      >
        {{ loading ? "搜索中..." : "搜索" }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  loading: {
    type: Boolean,
    default: false,
  },
  placeholder: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue", "submit"]);

const onInput = (event) => {
  emit("update:modelValue", event.target.value);
};
</script>