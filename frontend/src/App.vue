<template>
  <main class="min-h-screen bg-slate-900 text-white">
    <section class="mx-auto max-w-4xl px-4 py-10">
      <header class="mb-8 text-center">
        <p class="text-indigo-400 uppercase tracking-wide">Diynet Stage 1</p>
        <h1 class="text-4xl font-bold">家庭 KTV 点歌系统</h1>
        <p class="mt-2 text-slate-300">搜索歌单，立即播放</p>
      </header>

      <SearchBar
        v-model="keyword"
        :loading="loading"
        placeholder="输入歌名或歌手，比如：朋友"
        @submit="searchSongs"
      />

      <section class="mt-6 rounded-lg bg-slate-800/60 p-4 shadow-lg">
        <SongList :songs="songs" :loading="loading" @play="playSong" />
        <p v-if="error" class="mt-4 rounded bg-rose-900/40 px-3 py-2 text-rose-100">
          {{ error }}
        </p>
      </section>
    </section>
  </main>
</template>

<script setup>
import { ref } from "vue";
import SearchBar from "./components/SearchBar.vue";
import SongList from "./components/SongList.vue";
import { API_BASE_URL } from "./api/config";

const keyword = ref("");
const songs = ref([]);
const error = ref("");
const loading = ref(false);

const searchSongs = async () => {
  if (!keyword.value.trim()) {
    error.value = "请输入关键词";
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const response = await fetch(
      `${API_BASE_URL}/songs/search?keyword=${encodeURIComponent(keyword.value.trim())}`
    );

    if (!response.ok) {
      throw new Error("搜索失败，请检查后端服务");
    }

    songs.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const playSong = async (path) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/player/play?path=${encodeURIComponent(path)}`
    );

    if (!response.ok) {
      throw new Error("播放失败，请检查 MPV 或路径映射");
    }
  } catch (err) {
    error.value = err.message;
  }
};
</script>
