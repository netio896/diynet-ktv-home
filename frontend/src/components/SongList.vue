<template>
  <div>
    <div v-if="loading" class="py-10 text-center text-slate-300">加载中...</div>

    <div v-else>
      <div v-if="songs.length === 0" class="py-10 text-center text-slate-500">
        输入关键词开始搜索
      </div>

      <ul v-else class="space-y-3">
        <li
          v-for="song in songs"
          :key="song.id"
          class="flex flex-col justify-between gap-3 rounded-lg border border-slate-700 bg-slate-900/40 p-4 sm:flex-row sm:items-center"
        >
          <div>
            <p class="text-lg font-semibold">{{ song.title }}</p>
            <p class="text-sm text-slate-400">{{ song.artist }}</p>
            <p class="text-xs text-slate-500">{{ song.path }}</p>
          </div>
          <button
            class="rounded bg-emerald-500 px-4 py-2 text-white transition hover:bg-emerald-400"
            @click="$emit('play', song.path)"
          >
            播放
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  songs: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
</script>